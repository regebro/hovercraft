Using Hovercraft!
=================

Parameters
----------

``hovercraft [-h] [-t TEMPLATE] [-c CSS] [-a] <presentation> [<targetdir>]``

Required arguments:

    ``<presentation>``
        The path to the reStructuredText presentation file.

    ``<targetdir>``
        The directory where the presentation is saved. Will be created if it
        does not exist. If you do not specify a targetdir Hovecraft will
        instead start a webserver and serve the presentation from that server.

Optional arguments:

    ``-h, --help``
        Show this help.

    ``-t TEMPLATE, --template``
        TEMPLATE Specify a template. Must be a .cfg file, or a directory with
        a ``template.cfg file``. If not given it will use a default template.

    ``-c CSS, --css CSS``
        An additional CSS file for the presentation to use.
        See also the ``:css:`` settings of the presentation.

    ``-a, --auto-console``
        Pop up the console automatically. This is useful when you are
        rehearsing and making sure the presenter notes are correct.
        You can also set this by having ``:auto-console: true`` first in the
        presentation.

    ``-s, --skip-help``
        Pop up the console automatically. This is useful when you are
        rehearsing and making sure the presenter notes are correct.
        You can also set this by having ``:skip-help: true`` first in the
        presentation.

    ``--n, --skip-notes``
        Do not include presenter notes in the output.


Built in templates
------------------

There are two templates that come with Hovercraft! One is called ``default``
and will be used unless you specify a template. This is the template you will
use most of the time.

The second is called ``simple`` and it doesn't have a presenter console. This
template is especially useful if you combine it with the ``--skip-notes``
parameter to prepare a version of your presentation to be put online.
