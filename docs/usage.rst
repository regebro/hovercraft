Using Hovercraft!
=================

You can either use Hovercraft! to generate the presentation as HTML in a
target directory, or you can let Hovercraft! serve the presentation from
its builtin webserver.

The latter have several benefits. One is that most webbrowsers will be very
reluctant to open popup-windows from pages served from the file system.
This is a security measure which can be changed, but it's easier to
just point the browser to http://localhost:8000 instead.

The second benefit is that Hovercraft! will monitor the source files for the
presentation, and if they are modified Hovercraft! will generate the
presentation again automatically. That way you don't have to run Hovercraft!
everytime you save a file, you only need to refresh the browser.


Parameters
----------

``hovercraft [-h] [-t TEMPLATE] [-c CSS] [-j JS] [-a] [-s] [-n] [-p PORT] <presentation> [<targetdir>]``

Positional arguments:

    ``<presentation>``
        The path to the reStructuredText presentation file.

    ``<targetdir>``
        The directory where the presentation is saved. Will be created if it
        does not exist. If you do not specify a targetdir Hovercraft! will
        instead start a webserver and serve the presentation from that server.

Optional arguments:

    ``-h, --help``
        Show this help.

    ``-t TEMPLATE, --template TEMPLATE``
        Specify a template. Must be a .cfg file, or a directory with
        a ``template.cfg`` file. If not given it will use a default template.

    ``-c CSS, --css CSS``
        An additional CSS file for the presentation to use.
        See also the ``:css:`` settings of the presentation.

    ``-j JS, --js JS``
        An additional Javascript file for the presentation to use.
        Added as a js-body script.
        See also the ``:js-body:`` settings of the presentation.

    ``-a, --auto-console``
        Open the presenter console automatically. This is useful when you are
        rehearsing and making sure the presenter notes are correct.
        You can also set this by having ``:auto-console: true`` first in the
        presentation.

    ``-s, --skip-help``
        Do not show the initial help popup. You can also set
        this by having ``:skip-help: true`` first in the presentation.

    ``-n, --skip-notes``
        Do not include presenter notes in the output.

    ``-p PORT, --port PORT``
        The address and port that the server uses. Ex 8080 or
        127.0.0.1:9000. Defaults to 0.0.0.0:8000.

    ``--mathjax MATHJAX``
        The URL to the mathjax library. (It will only be used
        if you have rST ``math::`` in your document)

    ``-N, --slide-numbers``
        Show the current slide number on the slide itself and in the presenter
        console. You can also set this by having ``slide-numbers: true`` in
        the presentation preamble.

    ``-v, --version``
        Show program's version number and exit

Presenter Console
-----------------

The presenter console feature is designed for showing an annotated version of
the presentation on the local laptop display, while showing the presentation
itself on a projector.

To use this feature, open the presentation in a browser, and press `p`. A new
browser tab will be created, and the browser focus will switch to that tab
automatically. At this point, the two tabs are linked, and the slide
navigation controls will affect both tabs.

Now, you'll need to move the presenter console tab into its own browser
window. With Firefox, right-click on the tab title, and click on Move Tab -->
Move to New Window. With Chromium, drag the tab title down and the tab will be
moved into a new browser window.

Finally, drag the presentation window onto the projector's part of the
desktop, and press `F11` to make the presentation fullscreen.

Built in templates
------------------

There are two templates that come with Hovercraft! One is called ``default``
and will be used unless you specify a template. This is the template you will
use most of the time.

The second is called ``simple`` and right now it only lacks the Goto function.
You can ignore it.
