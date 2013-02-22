Hovercraft! manual
==================


Usage
-----

hovercraft [-h] [-t TEMPLATE] [-c CSS] [-a] <presentation> <targetdir>

Required arguments:

    ``<presentation>``
        The path to the reStructuredText presentation file.

    ``<targetdir>``
        The directory where the presentation is written. Will
        be created if it does not exist.

Optional arguments:

    -h, --help
        Show this help.
        
    -t TEMPLATE, --template TEMPLATE
        Specify a template. Must be a .cfg file, or a
        directory with a template.cfg file. If not given it
        will use a default template.
          
    -c CSS, --css CSS
        An additional css file for the presentation to use.
    
    -a, --auto-console
        Pop up the console automatically. This is useful when
        you are rehearsing and making sure the presenter notes
        are correct.

    -s, --skip-help
        Do not show the initial help popup.
        
    -n, --skip-notes
        Do not include presenter notes in the output.


Presentations
-------------

For information on how to make presentations with Hovercraft!, see presentations.rst.


Templates
---------

Templates are directories with a configuration file, a template xsl file,
and any number of css, js and other resource files. You can specify the
template either with the name of the configuration file, or the name of the
directory. If you specify the directory, the default name for the
configuration file is template.cfg.

Template files are in configparser format, which is an extended ini-style
format. They are very simple, and have only one section, [hovercraft]. Any
other sections will be ignored. Many of the parameters are lists that often
do not fit on one line. In that case you can split the line up over several
lines, but indenting the lines. The amount of indentation doens't make any
difference, except aestethically.

The parameters in the [hovercraft] section are:

    template     The name of the xsl template.
    
    css          A list of css filenames separated by whitespace. These files
                 will get included in the final file with "all" as the media 
                 specification.
                 
    css-<media>  A list of css filenames separated by whitespace. These files
                 will get included in the final file with the media given in
                 the parameter. So the files listed for the parameter 
                 "css-print"  will get "print" as their media specification and
                 a key like "css-screen,print" will return media "screen,print".
                 
    js-header    A list of filenames separated by whitespace. These files will
                 get included in the target file as header script links.

    js-body    A list of filenames separated by whitespace. These files will
                 get included in the target file as script links at the end of
                 the file. The files impress.js, impressConsole.js and
                 hovercraft.js typically need to be included here.
                 
    resource     A list of filenames separated by whitespace that will be 
                 copied to the target directory, but nothing else is done
                 with them. This is useful for images used by the css.
                 
An example:

    [hovercraft]
    template = template.xsl

    css = css/screen.css
          css/impressConsole.css

    css-print = css/print.css

    js-header = js/dateinput.js
    
    js-body = js/impress.js
              js/impressConsole.js
              js/hovercraft.js

    resource = images/back.png
               images/forward.png
               images/up.png
               images/down.png



The xsl template
++++++++++++++++

TODO add instructions for how to make your own XSLT templates.
Specifically mention the resource:reST.xml include.