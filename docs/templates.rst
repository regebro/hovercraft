Templates
=========

Luckily, for most cases you don't need to create your own template, as the
default template is very simple and most things you need to do is doable with
css. However, I don't want Hovercraft! to set up a wall where it isn't
flexible enough for your needs, so I added support to make your own templates.

You need to create your own template if you are unsatisfied with the HTML
that Hovercraft! generates, for example if you need to use another version of
HTML or if the reStructuredText you are using isn't being rendered in a way
that is useful for you. Although if you aren't happy with the HTML generated
from the reStructuredText that could very well be a bug, so open an issue on
`Github`_ for discussion.

Hovercraft! generates presentations by converting the reStructuredText into
XML and then using XSLT to translate the XML into HTML.

Templates are directories with a configuration file, a template XSL file,
and any number of CSS, JS and other resource files.


The template configuration file
-------------------------------

The configuration file is normally called template.cfg, but if you have
several configuration files in one template directory, you can specify which
one to use by specifying the full path to the configuration file. However, if
you just specify the template directory, ``template.cfg`` will be used.

Template files are in configparser format, which is an extended ini-style
format. They are very simple, and have only one section, ``[hovercraft]``. Any
other sections will be ignored. Many of the parameters are lists that often
do not fit on one line. In that case you can split the line up over several
lines, but indenting the lines. The amount of indentation doesn't make any
difference, except aesthetically.

The parameters in the ``[hovercraft]`` section are:

  * ``template``
    The name of the xsl template.

  * ``css``
    A list of CSS filenames separated by whitespace. These files
    will get included in the final file with "all" as the media
    specification.

  * ``css-<media>``
    A list of CSS filenames separated by whitespace. These files
    will get included in the final file with the media given in
    the parameter. So the files listed for the parameter
    "css-print" will get "print" as their media specification
    and a key like "css-screen,print" will return media
    "screen,print".

  * ``js-header``
    A list of filenames separated by whitespace. These files
    will get included in the target file as header script links.

  * ``js-body``
    A list of filenames separated by whitespace. These files
    will get included in the target file as script links at the
    end of the file. The files impress.js, impressConsole.js and
    hovercraft.js typically need to be included here.

  * ``resource``
    A list of filenames separated by whitespace that will be
    copied to the target directory, but nothing else is done
    with them. Images and fonts used by CSS will be copied
    anyway, but other resources may be added here.

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


The template file
-----------------

The file specified with the ``template`` parameters is the actual XSLT
template that will perform the translation from XML to HTML.

Most of the time you can just copy the default template file in
``hovercraft/templates/default/template.xsl`` and modify it. XSLT is very
complex, but modifying the templates HTML is quite straightforward as long as
you don't have to touch any of the ``<xsl:...>`` tags.

Also, the HTML that is generated is XHTML compatible and quite
straightforward, so for the most case all you would need to generate another
version of HTML, for example strict XHTML, would be to change the doctype.

But if you need to add or change the main generated HTML you can add and
change HTML statements in this main file as you like. See for example how the
little help-popup is added to the bottom of the HTML.

If you want to change the way the reStructuredText is rendered things get
slightly more complex. The XSLT rules that convert the reStructuredText XML
into HTML are contained in a separate file, ``reST.xsl``. For the most part
you can just include it in the template file with the following code::

    <xsl:import href="resource:templates/reST.xsl" />

The ``resource:`` part here is not a part of XSLT, but a part of Hovercraft!
It tells the XSLT translation that the file specified should not be looked
up on the file system, but as a Python package resource. Currently the
``templates/reST.xsl`` file is the only XSLT resource import available.

If you need to change the way reStructuredText is rendered you need to make a
copy of that file and modify it. You then need to make a copy of the main
template and change the reference in it to your modified XSLT file.

None of the XSLT files need to be copied to the target, and should not be
listed as a resource in the template configuration file.


.. _Github: https://github.com/regebro/hovercraft
