import os
import configparser
import shutil
from pkg_resources import resource_string, resource_filename

from lxml import etree

RESOURCE_TYPES = range(3)
CSS_RESOURCE, JS_RESOURCE, OTHER_RESOURCE = RESOURCE_TYPES

JS_POSITIONS = range(2)
JS_POSITION_HEADER, JS_POSITION_BODY = JS_POSITIONS


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
        config = configparser.ConfigParser()
        if self.builtin_template:
            cfg_string = resource_string(__name__, self.template + 'template.cfg').decode('UTF-8')
            config.read_string(cfg_string)
            self.template_root = self.template
        else:
            if os.path.isdir(self.template):
                self.template_root = self.template
                config_file = os.path.join(self.template, 'template.cfg')
            else:
                self.template_root = os.path.split(self.template)[0]
                config_file = self.template
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

            # Other files:
            elif key == 'resources':
                for filename in self.config[key].split():
                    self.add_resource(filename, OTHER_RESOURCE, is_in_template=True)

            # And finally the optional doctype:
            elif key == 'doctype':
                self.doctype = self.config['doctype'].encode()

    def _load_template_xsl(self):
        xsl_template = self.config['template']

        # The template
        if self.builtin_template:
            self.xsl = resource_string(__name__, self.template + xsl_template)
        else:
            with open(os.path.join(self.template_root, xsl_template), 'rb') as xslfile:
                self.xsl = xslfile.read()

    def get_source_path(self, resource):
        # Non-template resource (extra css)
        if not resource.is_in_template:
            return os.path.abspath(resource.filepath)

        # In template
        if self.builtin_template:
            resource_name = self.template + resource.filepath
            # Note that this will raise NotImplementedError if Hovercraft! is
            # installed as zip-file.
            return resource_filename(__name__, resource_name)

        # External template
        return os.path.join(self.template_root, resource.filepath)

    def read_data(self, resource):
        try:
            source_path = self.get_source_path(resource)
            with open(source_path, 'rb') as infile:
                return infile.read()
        except NotImplementedError:
            # Zip file! Read the data as binary and write out to the outfile.
            return resource_string(__name__, self.template + file)

    def copy_resource(self, resource, targetdir):
        """Copies a resource file and returns the source path for monitoring"""
        final_path = resource.final_path()
        if final_path[0] == '/' or ':' in final_path:
            # Absolute path or URI: Do nothing
            return None

        target_path = os.path.join(targetdir, final_path)
        directory_name, filename = os.path.split(target_path)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        try:
            source_path = self.get_source_path(resource)
        except NotImplementedError:
            # The template is in a zipped package!
            # Read the data as binary and write out to the outfile.
            with open(target_path, 'wb') as outfile:
                outfile.write(self.read_data(resource))
            # Done!
            return None  # Although copied, we do not monitor zip-files.

        if (os.path.exists(target_path) and
            os.path.getmtime(source_path) <= os.path.getmtime(target_path)):
            # File has not changed since last copy, so skip.
            return source_path  # This file should be monitored for changes

        shutil.copy2(source_path, target_path)
        return source_path  # This file should be monitored for changes

    def copy_resources(self, targetdir):
        for resource in self.resources:
            yield self.copy_resource(resource, targetdir)

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
