import os
import configparser
import shutil
import glob

from lxml import etree

RESOURCE_TYPES = range(4)
CSS_RESOURCE, JS_RESOURCE, DIRECTORY_RESOURCE, OTHER_RESOURCE = RESOURCE_TYPES

JS_POSITIONS = range(2)
JS_POSITION_HEADER, JS_POSITION_BODY = JS_POSITIONS

HOVERCRAFT_DIR = os.path.split(__file__)[0]


class Resource(object):

    def __init__(self, filepath, resource_type, target=None, extra_info=None, is_in_template=False):
        self.filepath = filepath
        assert resource_type in RESOURCE_TYPES
        self.resource_type = resource_type
        if resource_type == JS_RESOURCE:
            assert extra_info in JS_POSITIONS

        self.target = target
        self.extra_info = extra_info
        self.is_in_template = is_in_template

    def final_path(self):
        if self.target is None:
            self.target = self.filepath
        if self.target.startswith('..'):
            # A path above the current path was given. Treat this as an
            # absolute path, unless it's a part of the template.
            if self.is_in_template:
                return self.target
            return os.path.abspath(self.target)

        return self.target


class Template(object):

    def __init__(self, template=None):
        self.doctype = b'<!DOCTYPE html>'
        self.resources = []

        if template is None or template in ('default', 'simple'):
            self.builtin_template = True
            if template is None:
                template = 'default'
            self.template = '/templates/%s/' % template
        else:
            self.builtin_template = False
            self.template = os.path.abspath(template)

        self._load_template_config()
        self._load_template_xsl()
        self._load_template_files()

    def add_resource(self, filepath, resource_type, target=None, extra_info=None,
                     is_in_template=False):
        self.resources.append(Resource(filepath, resource_type, target=target,
                                       extra_info=extra_info, is_in_template=is_in_template))

    def _load_template_config(self):
        if self.builtin_template:
            self.template_root = os.path.join(HOVERCRAFT_DIR, self.template.strip('/'))
        else:
            self.template_root = self.template

        if os.path.isdir(self.template_root):
            config_file = os.path.join(self.template_root, 'template.cfg')
        else:
            config_file = self.template_root
            self.template_root = os.path.split(self.template)[0]

        config = configparser.ConfigParser()
        config.read(config_file)
        self.config = config['hovercraft']

    def _load_template_files(self):

        for key, files in self.config.items():
            # CSS files:
            if key.startswith('css'):
                # This is a css_file. The media can be specified, and defaults to 'all':
                if '-' in key:
                    css, media = key.split('-')
                else:
                    media = 'all'
                for filename in files.split():
                    self.add_resource(filename, CSS_RESOURCE, extra_info=media,
                                      is_in_template=True)

            # JS files:
            elif key == 'js-header':
                for filename in files.split():
                    self.add_resource(filename, JS_RESOURCE, extra_info=JS_POSITION_HEADER,
                                      is_in_template=True)

            elif key == 'js-body':
                for filename in files.split():
                    self.add_resource(filename, JS_RESOURCE, extra_info=JS_POSITION_BODY,
                                      is_in_template=True)

            elif key == 'resource-directories':
                for filename in self.config[key].split():
                    self.add_resource(filename, DIRECTORY_RESOURCE, is_in_template=True)

            # Other files:
            elif key == 'resources':
                for filename in self.config[key].split():
                    self.add_resource(filename, OTHER_RESOURCE, is_in_template=True)

            # And finally the optional doctype:
            elif key == 'doctype':
                self.doctype = self.config['doctype'].encode()

    def _load_template_xsl(self):
        xsl_template = self.config['template']
        with open(os.path.join(self.template_root, xsl_template), 'rb') as xslfile:
            self.xsl = xslfile.read()

    def get_source_path(self, resource):
        # Non-template resource (extra css)
        if not resource.is_in_template:
            return os.path.abspath(resource.filepath)

        # In template
        if self.builtin_template:
            return os.path.join(HOVERCRAFT_DIR, self.template.strip('/'), resource.filepath)

        # External template
        return os.path.join(self.template_root, resource.filepath)

    def read_data(self, resource):
        source_path = self.get_source_path(resource)
        with open(source_path, 'rb') as infile:
            return infile.read()

    def copy_resource(self, resource, targetdir):
        """Copies a resource file and returns the source path for monitoring"""
        final_path = resource.final_path()
        if final_path[0] == '/' or (':' in final_path) or ('?' in final_path):
            # Absolute path or URI: Do nothing
            return

        source_path = self.get_source_path(resource)

        if resource.resource_type == DIRECTORY_RESOURCE:
            for file_path in glob.iglob(os.path.join(source_path, '**'), recursive=True):
                if os.path.isdir(file_path):
                    continue
                rest_target_path = file_path[len(source_path)+1:]
                target_path = os.path.join(targetdir, final_path, rest_target_path)
                # Don't yield the result, we don't monitor these.
                self._copy_file(file_path, target_path)
        else:
            target_path = os.path.join(targetdir, final_path)
            yield self._copy_file(source_path, target_path)

    def _copy_file(self, source_path, target_path):
        directory_name, filename = os.path.split(target_path)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        if (os.path.exists(target_path) and
            os.path.getmtime(source_path) <= os.path.getmtime(target_path)):
            # File has not changed since last copy, so skip.
            return source_path  # This file should be monitored for changes

        shutil.copy2(source_path, target_path)
        return source_path  # This file should be monitored for changes

    def copy_resources(self, targetdir):
        for resource in self.resources:
            yield from self.copy_resource(resource, targetdir)

    def xml_node(self):
        node = etree.Element('templateinfo')
        header = etree.Element('header')
        node.append(header)
        body = etree.Element('body')
        node.append(body)

        for resource in self.resources:
            if resource.resource_type == CSS_RESOURCE:
                header.append(etree.Element('css', attrib={'href': resource.final_path(),
                                                           'media': resource.extra_info}))
            elif resource.resource_type == JS_RESOURCE:
                js_element = etree.Element('js', attrib={'src': resource.final_path()})
                if resource.extra_info == JS_POSITION_BODY:
                    body.append(js_element)
                else:
                    header.append(js_element)
        return node
