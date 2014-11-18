def main():

    # That the argparse default strings are lowercase is ugly.

    import gettext

    def my_gettext(s):
        return s.capitalize()
    gettext.gettext = my_gettext


    import os
    import re
    import argparse

    from lxml import html

    from hovercraft.generate import rst2html, copy_resource
    from hovercraft.template import Template, CSS_RESOURCE, OTHER_RESOURCE

    parser = argparse.ArgumentParser(
        description='Create impress.js presentations with reStructuredText',
        add_help=False)
    parser.add_argument(
        'presentation',
        metavar='<presentation>',
        help='The path to the reStructuredText presentation file.')
    parser.add_argument(
        'targetdir',
        metavar='<targetdir>',
        help=('The directory where the presentation is written. '
             'Will be created if it does not exist.'))
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help.')
    parser.add_argument(
        '-t',
        '--template',
        help=('Specify a template. Must be a .cfg file, or a directory with a '
             'template.cfg file. If not given it will use a default template.'))
    parser.add_argument(
        '-c',
        '--css',
        help='An additional css file for the presentation to use.')
    parser.add_argument(
        '-a',
        '--auto-console',
        action='store_true',
        help=('Pop up the console automatically. This is useful when you are '
             'rehearsing and making sure the presenter notes are correct.'))
    parser.add_argument(
        '-s',
        '--skip-help',
        action='store_true',
        help=('Do not show the initial help popup.'))
    parser.add_argument(
        '-n',
        '--skip-notes',
        action='store_true',
        help=('Do not include presenter notes in the output.'))

    args = parser.parse_args()

    # Parse the template info
    template_info = Template(args.template)
    if args.css:
        presentation_dir = os.path.split(args.presentation)[0]
        target_path = os.path.relpath(args.css, presentation_dir)
        template_info.add_resource(args.css, CSS_RESOURCE, target=target_path, extra_info='all')


    # Make the resulting HTML
    htmldata = rst2html(args.presentation, template_info, args.auto_console, args.skip_help, args.skip_notes)

    # Write the HTML out
    if not os.path.exists(args.targetdir):
        os.makedirs(args.targetdir)
    with open(os.path.join(args.targetdir, 'index.html'), 'wb') as outfile:
        outfile.write(htmldata)

    # Copy supporting files
    template_info.copy_resources(args.targetdir)

    # Copy images from the source:
    sourcedir = os.path.split(os.path.abspath(args.presentation))[0]
    tree = html.fromstring(htmldata)
    for image in tree.iterdescendants('img'):
        filename = image.attrib['src']
        copy_resource(filename, sourcedir, args.targetdir)

    RE_CSS_URL = re.compile(br"""url\(['"]?(.*?)['"]?[\)\?\#]""")

    # Copy any files referenced by url() in the css-files:
    for resource in template_info.resources:
        if resource.resource_type != CSS_RESOURCE:
            continue
        # path in CSS is relative to CSS file; construct source/dest accordingly
        css_base = template_info.template if resource.is_in_template else sourcedir
        css_sourcedir = os.path.dirname(os.path.join(css_base, resource.filepath))
        css_targetdir = os.path.dirname(os.path.join(args.targetdir, resource.final_path()))
        uris = RE_CSS_URL.findall(template_info.read_data(resource))
        uris = [uri.decode() for uri in uris]
        if resource.is_in_template and template_info.builtin_template:
            for filename in uris:
                template_info.add_resource(filename, OTHER_RESOURCE, target=css_targetdir, is_in_template=True)
        else:
            for filename in uris:
                copy_resource(filename, css_sourcedir, css_targetdir)

    # All done!
