Hovercraft manual
=================


Usage
-----

hovercraft <presentation.rst> <outdirectory>

QQQ: Support a directory of rst-files? index.rst? What does sphinx do?
Outdirectory has to be a directory. css and js files *will* be copied. 

Parameters: 

  --template, -t         Select a template. Must be a directory with a 
                         template.cfg file, or a .cfg file, or the name of
                         a built-in template (currently only "default").
                         
  --css                  Specify and additional css file to be added to the 
                         presentation, with "screen,print,projection" as media.

  --auto-console, -a     Pop up the presenter console automatically when 
                         opening the presentation.

Presentations
-------------

For information on how to make presentations with Hovercraft, see presentations.rst.


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
                 will get included in the final file with "screen, print, 
                 projection" as the media specification.
                 
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