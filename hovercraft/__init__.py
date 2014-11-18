import argparse
import gettext
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from tempfile import TemporaryDirectory
from watchdog.observers import Observer
from .generate import generate

def main():

    # That the argparse default strings are lowercase is ugly.


    def my_gettext(s):
        return s.capitalize()
    gettext.gettext = my_gettext

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
        nargs='?',
        help=('The directory where the presentation is saved. Will be created '
             'if it does not exist. If you do not specify a targetdir '
             'Hovecraft will instead start a webserver and serve the'
             'presentation from that server.'))
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

    if args.targetdir:
        # Generate the presentation
        generate(args)
    else:
        # Server mode. Start a server that serves a temporary directory.

        with TemporaryDirectory() as targetdir:
            args.targetdir = targetdir
            generate(args)

            # Set up watchdog to regenerate presentation if saved.
            observer = Observer()

            os.chdir(targetdir)
            bind, port = ('0.0.0.0',8000)
            server = HTTPServer((bind, port), SimpleHTTPRequestHandler)

            print("Serving HTTP on", bind, "port", port, "...")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")
                server.server_close()
                sys.exit(0)
