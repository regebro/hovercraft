
def main():

    import os
    import argparse
    from hovercraft.generate import rst2html, copy_files
    from hovercraft.template import get_template_info
    
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
        help='The directory where the presentation is written. '\
             'Will be created if it does not exist.')
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help.')
    parser.add_argument(
        '-t',
        '--template',
        help='Specify a template. Must be a .cfg file, or a directory with a '\
             'template.cfg file. If not given it will use a default template.')
    parser.add_argument(
        '-c',
        '--css',
        help='An additional css file for the presentation to use.')
    parser.add_argument(
        '-a',
        '--auto-console',
        action='store_true',
        help='Pop up the console automatically. This is useful when you are '\
             'rehearsing and making sure the presenter notes are correct.')
    
    args = parser.parse_args()

    # not used yet: args.auto_console

    # Parse the template info
    template_info = get_template_info(args.template, args.css)

    # Read the infile
    with open(args.presentation, 'rb') as infile:
        rst = infile.read()

    # Make the resulting HTML
    html = rst2html(rst, template_info)
    
    # Write the HTML out
    if not os.path.exists(args.targetdir):
        os.makedirs(args.targetdir)
    with open(os.path.join(args.targetdir, 'index.html'), 'wb') as outfile:
        outfile.write(html)
        
    # Copy supporting files
    copy_files(template_info, args.targetdir)
    