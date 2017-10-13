import os
import re
import shutil
from lxml import etree, html
from pkg_resources import resource_string

from .parse import rst2xml, SlideMaker
from .position import position_slides
from .template import (Template, CSS_RESOURCE, JS_RESOURCE, JS_POSITION_HEADER,
                       JS_POSITION_BODY, OTHER_RESOURCE, DIRECTORY_RESOURCE)


class ResourceResolver(etree.Resolver):

    def resolve(self, url, pubid, context):
        if url.startswith('resource:'):
            prefix, filename = url.split(':', 1)
            return self.resolve_string(resource_string(__name__, filename), context)


def rst2html(filepath, template_info, auto_console=False, skip_help=False, skip_notes=False, mathjax=False, slide_numbers=False):
    # Read the infile
    with open(filepath, 'rb') as infile:
        rststring = infile.read()

    presentation_dir = os.path.split(filepath)[0]

    # First convert reST to XML
    xml, dependencies = rst2xml(rststring, filepath)
    tree = etree.fromstring(xml)

    # Fix up the resulting XML so it makes sense
    sm = SlideMaker(tree, skip_notes=skip_notes)
    tree = sm.walk()

    # Pick up CSS information from the tree:
    for attrib in tree.attrib:
        if attrib.startswith('css'):
            if '-' in attrib:
                dummy, media = attrib.split('-', 1)
            else:
                media = 'screen,projection'
            css_files = tree.attrib[attrib].split()
            for css_file in css_files:
                template_info.add_resource(
                    os.path.abspath(os.path.join(presentation_dir, css_file)),
                    CSS_RESOURCE,
                    target=css_file,
                    extra_info=media)
        if attrib.startswith('js'):
            if attrib == 'js-header':
                media = JS_POSITION_HEADER
            else:
                # Put javascript in body tag as default.
                media = JS_POSITION_BODY
            js_files = tree.attrib[attrib].split()
            for js_file in js_files:
                template_info.add_resource(
                    os.path.abspath(os.path.join(presentation_dir, js_file)),
                    JS_RESOURCE,
                    target=js_file,
                    extra_info=media)

    if sm.need_mathjax and mathjax:
        if mathjax.startswith('http'):
            template_info.add_resource(None, JS_RESOURCE,
                                       target=mathjax,
                                       extra_info=JS_POSITION_HEADER)
        else:
            # Local copy
            template_info.add_resource(mathjax, DIRECTORY_RESOURCE,
                                       target='mathjax')
            template_info.add_resource(None, JS_RESOURCE,
                                       target='mathjax/MathJax.js?config=TeX-MML-AM_CHTML',
                                       extra_info=JS_POSITION_HEADER)

    # Position all slides
    position_slides(tree)

    # Add the template info to the tree:
    tree.append(template_info.xml_node())

    # If the console-should open automatically, set an attribute on the document:
    if auto_console:
        tree.attrib['auto-console'] = 'True'

    # If the console-should open automatically, set an attribute on the document:
    if skip_help:
        tree.attrib['skip-help'] = 'True'

    # If the slide numbers should be displayed, set an attribute on the document:
    if slide_numbers:
        tree.attrib['slide-numbers'] = 'True'

    # We need to set up a resolver for resources, so we can include the
    # reST.xsl file if so desired.
    parser = etree.XMLParser()
    parser.resolvers.add(ResourceResolver())

    # Transform the tree to HTML
    xsl_tree = etree.fromstring(template_info.xsl, parser)
    transformer = etree.XSLT(xsl_tree)
    tree = transformer(tree)
    result = html.tostring(tree)

    return template_info.doctype + result, dependencies


def copy_resource(filename, sourcedir, targetdir):
    if filename[0] == '/' or ':' in filename:
        # Absolute path or URI: Do nothing
        return None  # No monitoring needed
    sourcepath = os.path.join(sourcedir, filename)
    targetpath = os.path.join(targetdir, filename)

    if (os.path.exists(targetpath) and
        os.path.getmtime(sourcepath) <= os.path.getmtime(targetpath)):
        # File has not changed since last copy, so skip.
        return sourcepath  # Monitor this file

    targetdir = os.path.split(targetpath)[0]
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)

    shutil.copy2(sourcepath, targetpath)
    return sourcepath  # Monitor this file


def generate(args):
    """Generates the presentation and returns a list of files used"""

    source_files = {args.presentation}

    # Parse the template info
    template_info = Template(args.template)
    if args.css:
        presentation_dir = os.path.split(args.presentation)[0]
        target_path = os.path.relpath(args.css, presentation_dir)
        template_info.add_resource(args.css, CSS_RESOURCE, target=target_path, extra_info='all')
        source_files.add(args.css)
    if args.js:
        presentation_dir = os.path.split(args.presentation)[0]
        target_path = os.path.relpath(args.js, presentation_dir)
        template_info.add_resource(args.js, JS_RESOURCE, target=target_path, extra_info=JS_POSITION_BODY)
        source_files.add(args.js)

    # Make the resulting HTML
    htmldata, dependencies = rst2html(args.presentation, template_info,
                                      args.auto_console, args.skip_help,
                                      args.skip_notes, args.mathjax,
                                      args.slide_numbers)
    source_files.update(dependencies)

    # Write the HTML out
    if not os.path.exists(args.targetdir):
        os.makedirs(args.targetdir)
    with open(os.path.join(args.targetdir, 'index.html'), 'wb') as outfile:
        outfile.write(htmldata)

    # Copy supporting files
    source_files.update(template_info.copy_resources(args.targetdir))

    # Copy images from the source:
    sourcedir = os.path.split(os.path.abspath(args.presentation))[0]
    tree = html.fromstring(htmldata)
    for image in tree.iterdescendants('img'):
        filename = image.attrib['src']
        source_files.add(copy_resource(filename, sourcedir, args.targetdir))

    RE_CSS_URL = re.compile(br"""url\(['"]?(.*?)['"]?[\)\?\#]""")

    # Copy any files referenced by url() in the css-files:
    for resource in template_info.resources:
        if resource.resource_type != CSS_RESOURCE:
            continue
        # path in CSS is relative to CSS file; construct source/dest accordingly
        css_base = template_info.template_root if resource.is_in_template else sourcedir
        css_sourcedir = os.path.dirname(os.path.join(css_base, resource.filepath))
        css_targetdir = os.path.dirname(os.path.join(args.targetdir, resource.final_path()))
        uris = RE_CSS_URL.findall(template_info.read_data(resource))
        uris = [uri.decode() for uri in uris]
        if resource.is_in_template and template_info.builtin_template:
            for filename in uris:
                template_info.add_resource(filename, OTHER_RESOURCE, target=css_targetdir,
                                           is_in_template=True)
        else:
            for filename in uris:
                source_files.add(copy_resource(filename, css_sourcedir, css_targetdir))

    # All done!

    return {os.path.abspath(f) for f in source_files if f}
