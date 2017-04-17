#!/usr/bin/env python
import aionotify
import argparse
import asyncio
import gettext
import os

from aiohttp import web, WSMessage, WSMsgType
from functools import partial
from pkgutil import get_data
from tempfile import TemporaryDirectory

from hovercraft.generate import generate


async def index(request):
    body = get_data('hovercraft', 'index.html')
    return web.Response(body=body, content_type='text/html', charset='utf8')


async def websocket_sender(queue, ws):
    while True:
        msg = await queue.get()
        print("Queue", msg)
        ws.send_str(msg)


async def websocket_handler(queue, request):
    ws = web.WebSocketResponse()
    try:
        await ws.prepare(request)
        ws.send_str('start')

        task = request.app.loop.create_task(websocket_sender(queue, ws))

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    ws.send_str(msg.data + '/answer')
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
    finally:
        task.cancel()
        await ws.close()
        print('websocket connection closed')

    return ws


async def rebuilder(args, loop, queue):
    old_files = set()
    try:
        watcher = aionotify.Watcher()
        await watcher.setup(loop)

        while True:
            print("Generating presentation...", end="")
            new_files = generate(args)
            print("Done!")
            await queue.put("reload")

            for path in new_files - old_files:
                watcher.watch(path=path, flags=(aionotify.Flags.MODIFY |
                                                aionotify.Flags.CREATE |
                                                aionotify.Flags.MOVED_TO))
            for path in old_files - new_files:
                watcher.unwatch(alias=path)

            old_files = new_files
            event = await watcher.get_event()
    finally:
        watcher.close()


def run():
    """Main Hovercraft process"""

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
        '-j',
        '--js',
        help=('An additional javascript file for the presentation to use. Added as a js-body script.'
              'See also the ``:js-body:`` settings of the presentation.'))
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
    parser.add_argument(
        '--mathjax',
        default=os.environ.get('HOVERCRAFT_MATHJAX', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML'),
        help=('The URL to the mathjax library.'
              ' (It will only be used if you have rST ``math::`` in your document)'))
    parser.add_argument(
        '-N',
        '--slide-numbers',
        action='store_true',
        help=('Show slide numbers during the presentation.'))

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

            # Start an event loop
            loop = asyncio.get_event_loop()
            queue = asyncio.Queue(loop=loop)

            # Attach the rebuilder task
            asyncio.ensure_future(rebuilder(args, loop, queue))

            # And add the webapp
            app = web.Application()
            app.router.add_get('/', index)
            app.router.add_get('/ws', partial(websocket_handler, queue))
            app.router.add_static('/presentation', targetdir)

            if ':' in args.port:
                host, port = args.port.split(':')
            else:
                host, port = '127.0.0.1', args.port
            port = int(port)

            web.run_app(app, host=host, port=port, loop=loop)

if __name__ == '__main__':
    run()
