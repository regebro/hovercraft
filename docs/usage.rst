Using Hovercraft!
=================

Parameters
----------

``hovercraft [-h] [-t TEMPLATE] [-c CSS] [-a] <presentation> <targetdir>``

Required arguments:

    ``<presentation>``
        The path to the reStructuredText presentation file.

    ``<targetdir>``
        The directory where the presentation is written. Will
        be created if it does not exist.

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
