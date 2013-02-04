
def main():

    import os
    import re
    import argparse
    import shutil
    
    from lxml import html
    
    from hovercraft.generate import rst2html, copy_files
    from hovercraft.template import get_template_info

    def copy_resource(filename, sourcedir, targetdir):
        if filename[0] == '/' or ':' in filename:
            # Absolute path or URI: Do nothing
            return
        sourcepath = os.path.join(sourcedir, filename)
        targetpath = os.path.join(targetdir, filename)
        targetdir = os.path.split(targetpath)[0]
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)
        
        shutil.copy2(sourcepath, targetpath)
    
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
    
    args = parser.parse_args()

    # Parse the template info
    template_info = get_template_info(args.template, args.css)

    # Read the infile
    with open(args.presentation, 'rb') as infile:
        rst = infile.read()

    # Make the resulting HTML
    htmldata = rst2html(rst, template_info, args.auto_console)
    
    # Write the HTML out
    if not os.path.exists(args.targetdir):
        os.makedirs(args.targetdir)
    with open(os.path.join(args.targetdir, 'index.html'), 'wb') as outfile:
        outfile.write(htmldata)
        
    # Copy supporting files
    copy_files(template_info, args.targetdir)

    # Copy images from the source:
    sourcedir = os.path.split(os.path.abspath(args.presentation))[0]
    tree = html.fromstring(htmldata)
    for image in tree.iterdescendants('img'):
        filename = image.attrib['src']
        copy_resource(filename, sourcedir, args.targetdir)

    RE_CSS_URL = re.compile(br"""url\(['"]?(.*?)['"]?[\)\?\#]""")
    
    # Copy any files referenced by url() in the css-files:
    for file, target in template_info['css']:
        uris = RE_CSS_URL.findall(template_info['files'][file])        
        uris = [uri.decode() for uri in uris]
        for filename in uris:
            copy_resource(filename, sourcedir, args.targetdir)
    
    # All done!