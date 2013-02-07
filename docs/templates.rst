Templates
=========

Templates are directories with a configuration file, a template xsl file,
and any number of css, js and other resource files. You can specify the
template either with the name of the configuration file, or the name of the
directory.

The template configuration file
-------------------------------

The configuration file is normally called template.cfg, but if you have
several configuration files in one template directory, you can specify which
one by specifying the full path to the configuration file. However, if you
just specify the template directory, ``template.cfg`` will be used.

Template files are in configparser format, which is an extended ini-style
format. They are very simple, and have only one section, [hovercraft]. Any
other sections will be ignored. Many of the parameters are lists that often
do not fit on one line. In that case you can split the line up over several
lines, but indenting the lines. The amount of indentation doesn't make any
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
                 
An example::

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


