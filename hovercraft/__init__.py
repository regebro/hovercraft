import argparse
import gettext
import os
import sys
import threading
import time
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from tempfile import TemporaryDirectory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .generate import generate


class HovercraftEventHandler(FileSystemEventHandler):
    def __init__(self, filelist):
        self.filelist = filelist
        self.quit = False
        super().__init__()

    def on_modified(self, event):
        self._update(event.src_path)

    def on_moved(self, event):
        self._update(event.dest_path)

    def _update(self, src_path):
        if src_path in self.filelist:
            print("File %s modified, update presentation" % src_path)
            self.quit = True


def generate_and_observe(args, event):
    while event.isSet():
        # Generate the presentation
        monitor_list = generate(args)
        print("Presentation generated.")

        # Make a list of involved directories
        directories = defaultdict(list)
        for file in monitor_list:
            directory, filename = os.path.split(file)
            directories[directory].append(filename)

        observer = Observer()
        handler = HovercraftEventHandler(monitor_list)
        for directory, files in directories.items():
            observer.schedule(handler, directory, recursive=False)

        observer.start()
        while event.wait(1):
            time.sleep(0.05)
            if handler.quit:
                break

        observer.stop()
        observer.join()


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
              'Hovercraft! will instead start a webserver and serve the '
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
        help=('An additional css file for the presentation to use. '
              'See also the ``:css:`` settings of the presentation.'))
    parser.add_argument(
        '-a',
        '--auto-console',
        action='store_true',
        help=('Open the presenter console automatically. This is useful when '
              'you are rehearsing and making sure the presenter notes are '
              'correct. You can also set this by having ``:auto-console: '
              'true`` first in the presentation.'))
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
    parser.add_argument(
        '-p',
        '--port',
        default='0.0.0.0:8000',
        help=('The address and port that the server uses. '
              'Ex 8080 or 127.0.0.1:9000. Defaults to 0.0.0.0:8000.'))

    args = parser.parse_args()

    # XXX Bit of a hack, clean this up, I check for this twice, also in the template.
    if args.template and args.template not in ('simple', 'default'):
        args.template = os.path.abspath(args.template)

    if args.targetdir:
        # Generate the presentation
        generate(args)
    else:
        # Server mode. Start a server that serves a temporary directory.

        with TemporaryDirectory() as targetdir:
            args.targetdir = targetdir
            args.presentation = os.path.abspath(args.presentation)

            # Set up watchdog to regenerate presentation if saved.
            event = threading.Event()
            event.set()
            thread = threading.Thread(target=generate_and_observe, args=(args, event))
            try:
                # Serve presentation
                if ':' in args.port:
                    bind, port = args.port.split(':')
                else:
                    bind, port = '0.0.0.0', args.port
                port = int(port)

                # First create the server. This checks that we can connect to
                # the port we want to.
                os.chdir(targetdir)
                server = HTTPServer((bind, port), SimpleHTTPRequestHandler)
                print("Serving HTTP on", bind, "port", port, "...")

                try:
                    # Now generate the presentation
                    thread.start()

                    try:
                        # All is good, start the server
                        server.serve_forever()
                    except KeyboardInterrupt:
                        print("\nKeyboard interrupt received, exiting.")
                    finally:
                        # Server exited
                        server.server_close()

                finally:
                    # Stop the generation thread
                    event.clear()
                    # Wait for it to end
                    thread.join()

            except PermissionError:
                print("Can't bind to port %s:%s: No permission" % (bind, port))
            except OSError as e:
                if e.errno == 98:
                    print("Can't bind to port %s:%s: port already in use" % (bind, port))
                else:
                    raise
