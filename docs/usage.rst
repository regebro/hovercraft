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

``hovercraft [-h] [-t TEMPLATE] [-c CSS] [-a] [-s] [-n] [-p PORT] <presentation> [<targetdir>]``

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

    ``-a, --auto-console``
        Open the presenter console automatically. This is useful when you are
        rehearsing and making sure the presenter notes are correct.
        You can also set this by having ``:auto-console: true`` first in the
        presentation.

    ``-s, --skip-help`` Do not show the initial help popup. You can also set
        this by having ``:skip-help: true`` first in the presentation.


    ``-n, --skip-notes``
        Do not include presenter notes in the output.

    ``-p PORT, --port PORT``
        The address and port that the server uses. Ex 8080 or
        127.0.0.1:9000. Defaults to 0.0.0.0:8000.


Built in templates
------------------

There are two templates that come with Hovercraft! One is called ``default``
and will be used unless you specify a template. This is the template you will
use most of the time.

The second is called ``simple`` and it doesn't have a presenter console. This
template is especially useful if you combine it with the ``--skip-notes``
parameter to prepare a version of your presentation to be put online.
