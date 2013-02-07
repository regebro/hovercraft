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
        a template.cfg file. If not given it will use a default template.
          
    ``-c CSS, --css CSS``
        An additional css file for the presentation to use.
    
    ``-a, --auto-console``
        Pop up the console automatically. This is useful when you are
        rehearsing and making sure the presenter notes are correct.

       
External files
--------------

Any image file referenced in the presentation by a relative path will be
copied to the target directory, keeping it's relative path to the
presentation. The same goes for images or fonts referenced in the CSS.

Images or fonts referenced by absolute paths or URI's will not be copied.
