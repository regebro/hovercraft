Making presentations
====================

A note on terminology
---------------------

Traditionally a presentation is made up of slides. Calling them "slides" is
not really relevant in an impress.js context, as they can overlap and doesn't
necessarily slide. The name "steps" is better, but it's also more ambiguous.
Hence impress.js uses the terms "slide" and "step" as meaning the same thing,
and so does Hovercraft!


Hovercraft! syntax
------------------

Presentations are reStructuredText files. If you are reading this
documentation from the source code, then you are looking at a
reStructuredText document already.

It's fairly simple, you underline headings to mark them as headings::


    This becomes a h1
    =================

    And this a h2
    -------------


The different ways of underlining them doesn't mean anything, instead the
order of them is relevant, so the first type of underline encountered in the
file will make a level 1 heading, the second type a level 2 heading and so
on. In this file = is used for level 1, and - for level 2.

You can also mark text as *italic* or **bold**, with ``*single asterixes*``
or ``**double asterixes**`` respectively.

You can also have bullet lists::

    * Bullet 1

      * Bullet 1.1

    * Bullet 2

    * Bullet 3

And numbered lists::

    1. Item 1

        1.1. Item 1.1

    2. Item 2

    3. Item 3


You can include images::

    .. image:: path/to/image.png
        :height: 600px
        :width: 800px

As you see you can also specify height and width and loads of other parameters_, but they
are all optional.

And you can mark text as being preformatted. You do that by ending the
previous row with double colons, or have a row of double colons by itself::

    ::

        This code here will be preformatted
         and shown with a  monospaced font
        and    all    spaces     preserved.

If you want to add source code, you can use the ``code`` directive, and get
syntax highlighting::

    .. code:: python

        def some_example_code(foo):
            return foo * foo

The syntax highlighting is done by Pygments_ and supports lots and lots of
languages_.

You are also likely to want to put a title on the presentation. You do that
by having a ``.. title::`` statement before the first slide::

    .. title:: This is the presentation title

That is the most important things you'll need to know about reStructuredText for
making presentations. There is a lot more to know, and a lot of advanced features
like links, footnotes, and more. It is in fact advanced enough so you can write a
whole book_ in it, but for all that you need to read the documentation_.


External files
--------------

Any image file referenced in the presentation by a relative path will be
copied to the target directory, keeping it's relative path to the
presentation. The same goes for images or fonts referenced in any
CSS files used by the presentation or the template.

Images or fonts referenced by absolute paths or URI's will not be copied.


Styling your Presentation
-------------------------

The css that is included by the default template are three files.

* ``impressConsole.css`` contains the CSS needed for the presenter console to work,

* ``highlight.css`` contains a default style for code syntax highlighting, as
  that otherwise would be a lot of work. If you don't like the default colors
  or styles in the highlighting, this is the file you should copy and modify.

* ``hovercraft.css``, which only includes the bare minimum: It hides the
  impress.js fallback message, the presenter notes, and sets up a useful
  default of having a step width be 1000 pixels wide.

For this reason you want to include your own CSS to style your slides. To
include a CSS file you add a ``:css:``-field at the top of the presentation::

    :css: css/presentation.css

You can also optionally specify that the css should be only valid for certain
CSS media::

    :css-screen,projection: css/presentation.css
    :css-print: css/print.css

You can specify any number of css files in this way.
You can also add one extra CSS-file via a command-line parameter:

    hovercraft --extra-css=my_extra.css presentationfile.rst outdir/


Styling a specific slide
........................

If you want to have specific styling for a specific slide, it is a good
idea to give that slide a unique ID::

    :id: the-slide-id

You can then style that slide specifically with::

    div#the-slide-id {
        /* Custom CSS here */
    }

If you don't give it a specific ID, it will get an ID based on its sequence
number. And that means the slide's ID will change if you insert or remove
slides that came before it, and in that case your custom stylings of that
slide will stop working.

Portable presentations
......................

Since Hovercraft! generates HTML5 presentations, you can use any computer
that has a modern browser installed to view or show the presentation. This
allows you both to put up the presentation online and to use a borrowed
computer for your conference or customer presentation.

When you travel you don't know what equipment you have to use when you show
your presentaton, and it's surprisingly common to encounter a projector that
refuses to talk to your computer. It is also very easy to forget your dongle
if you have a MacBook, and there have even been cases of computers going
completely black and dead when you connect them to a projector, even though
all other computers seem to work fine.

The main way of making sure your presentation is portable is to try it on
different browsers and different computers. But the latter can be unfeasible,
not everyone has both Windows, Linux and OS X computers at home. To help make
your presentations portable it is a good idea to define your own @font-face's
and use them, so you are sure that the target browser will use the same fonts
as you do. Hovercraft! will automatically find @font-face definitions and
copy the font files to the target directory.


impress.js fields
-----------------

The documentation on impress.js is contained as comments in the `demo html
file <https://github.com/bartaz/impress.js/blob/master/index.html>`_. It is
not always very clear, so here comes a short summary for convenience.

The different data fields that impress.js will use in 0.5.3, which is the
current version, are the following:

* **data-transition-duration**: The time it will take to move from one slide to
  another. Defaults to 1000 (1 second). This is only valid on the presentation
  as a whole.

* **data-perspective**: Controls the "perspective" in the 3d effects. It
  defaults to 500. Setting it to 0 disables 3D effects.

* **data-x**: The horizontal position of a slide in pixels. Can be negative.

* **data-y**: The vertical position of a slide in pixels. Can be negative.

* **data-scale**: Sets the scale of a slide, which is what creates the zoom.
  Defaults to 1. A value of 4 means the slide is four times larger. In short:
  Lower means zooming in, higher means zooming out.

* **data-rotate-z**: The rotation of a slide in the x-axis, in degrees. This
  will cause the slide to be rotated clockwise or counter-clockwise.

* **data-rotate**: The same as **data-rotate-z**.

* **data-rotate-x**: The rotation of a slide in the x-axis, in degrees. This
  means you are moving the slide in a third dimension compared with other
  slides. This is generally cool effect, if used right.

* **data-rotate-y**: The rotation of a slide in the x-axis, in degrees.

* **data-z**: This controls the position of the slide on the z-axis. Setting
  this value to -3000 means it's positioned -3000 pixels away. This is only
  useful when you use **data-rotate-x** or **data-rotate-y**, otherwise it will
  only give the impression that the slide is made smaller, which isn't really
  useful.


Hovercraft! specialities
------------------------

Hovercraft! has some specific ways it uses reStructuredText. First of all, the
reStructuredText "transition" is used to mark the separation between
different slides or steps. A transition is simply a line with four or more
dashes::

    ----

You don't have to use dashes, you can use any of the characters used to
underline headings, ``= - ` : . ' " ~ ^ _ * + #``. And just as width
headings, using different characters indicates different "levels". In this
way you can make a hierarchical presentation, with steps and substeps.
However, impress.js does not support that, so this is only useful
if you make your own templates that uses another Javascript library, for
example Reveal.js_. If you have more than one transition level with
the templates included with Hovercraft, the resulting presentation may
behave strangely.

All reStructuredText fields are converted into attributes on the current tag.
Most of these will typically be ignored by the rendering to HTML, but there
is two places where the tags will make a difference, and that is by putting
them first in the document, or first on a slide.

Any fields you put first in a document will be rendered into attributes on
the main impress.js ``<div>``. The only ones that Hovercraft! will use are
``data-transition-duration``, ``skip-help`` and ``auto-console``.

Any fields you put first in a slide will be rendered into attributes on the
slide ``<div>``. This is used primarily to set the position/zoom/rotation of
the slide, either with the ``data-x``, ``data-y`` and other impress.js
settings, or the ``hovercraft-path`` setting, more on that later.

Hovercraft! will start making the first slide when it first encounters either
a transition or a header. Everything that comes before that will belong to the
presentation as a whole.

A presentation can therefore look something like this::


    :data-transition-duration: 2000
    :skip-help: true

    .. title: Presentation Title

    ----

    This is the first slide
    =======================

    Here comes some text.

    ----

    :data-x: 300
    :data-y: 2000

    This is the second slide
    ========================

    #. Here we have

    #. A numbered list

    #. It will get correct

    #. Numbers automatically


Relative positioning
--------------------

Hovercraft! gives you the ability to position slides relative to each other.
You do this by starting the coordinates with "r". This will position the
slide 500 pixels to the right and a thousand pixels above the previous slide::

    :data-x: r500
    :data-y: r-1000

Relative paths allow you to insert and remove slides and have other slides
adjust automatically. It's generally the most useful way of positioning.


Automatic positioning
---------------------

If you don't specify an attribute, the slide settings
will be the same as the previous slide. This means that if you used
relative positioning, the next slide will move the same distance.

This gives a linear movement, and your slides will end up in a straight line.

By default the movement is 1600 pixels to the right, which means that if you
don't position any slides at all, you get a standard presentation where the
slides will simply slide from right to left.


SVG Paths
---------

Hovercraft! supports positioning slides along an SVG path. This is handy, as
you can create a drawing in a software that supports SVG, and then copy-paste
that drawings path into your presentation.

You specify the SVG path with the ``:hovercraft-path:`` field. For example::

    :hovercraft-path: m275,175 v-150 a150,150 0 0,0 -150,150 z

Every following slide that does not have any explicit positioning will be
placed on this path.

There are some things you need to be careful about when using SVG paths.

Relative and absolute coordinates
.................................

SVG coordinates can either be absolute, with a reference to the page
origin; or relative, which is in reference to the last point. Hovercraft! can
handle both, but what it can not handle very well is a mixture of them.

Specifically, if you take an SVG path that starts with a relative movement
and extract that from the SVG document, you will lose the context. All
coordinates later must then also be relative. If you have an absolute
coordinate you then suddenly regain the context, and everything after the
first absolute coordinate will be misplaced compared to the points that come
before.

Most notable, the open source software "Inkscape" will mix absolute and
relative coordinates, if you allow it to use relative coordinates. You
therefore need to go into it's settings and uncheck the checkbox that allows
you to use relative coordinates. This forces Inkscape to save all coordinates
as absolute, which will work fine.

Start position
..............

By default the start position of the path, and hence the start position of
the first slide, will be whatever the start position would have been if the
slide had no positioning at all. If you want to change this position then
just include ``:data-x:`` or ``:data-y:`` fields. Both relative and absolute
positioning will work here.

In all cases, the first ``m`` or ``M`` command of the SVG path is effectively
ignored, but you have to include it anyway.

SVG transforms
..............

SVG allows you to draw up path and then transform it. Hovercraft! has no
support for these transforms, so before you extract the path you should make
sure the SVG software doesn't use transforms. In Inkscape you can do this by
the "Simplify" command.

Other SVG shapes
................

Hovercraft! doesn't support other SVG shapes, just the path. This is because
organising slides in squares, etc, is quite simple anyway, and the shapes can
be made into paths. Usually in the software you will have to select the shape
and tell your software to make it into a path. In Inkscape, transforming an
object into a path will generally mean that the whole path is made of
CubicBezier curves, which are unnecessarily complex. Using the "Simplify"
command in Inkscape is usually enough to make the shapes into paths.

Shape-scaling
.............

Hovercraft! will scale the path so that all the slides that need to fit into
the path will fit into the path. If you therefore have several paths in your
presentation, they will **not** keep their relative sizes, but will be
resized so the slides fit. If you need to have the shapes keep their relative
sizes, you need to combine them into one path.

Examples
--------

To see how to use Hovercraft! in practice, there are three example presentations
included with Hovercraft!

    hovercraft.rst_
        The demo presentation you can see at http://regebro.github.com/hovercraft

    tutorial.rst_
        A step by step guide to the features of Hovercraft!

    positions.rst_
        An explanation of how to use the positioning features.


.. _documentation: http://docutils.sourceforge.net/docs/index.html
.. _parameters: http://docutils.sourceforge.net/docs/ref/rst/directives.html#images
.. _book: http://python3porting.com/
.. _Pygments: http://pygments.org/
.. _languages: http://pygments.org/docs/lexers/
.. _hovercraft.rst: ./_sources/examples/hovercraft.txt
.. _tutorial.rst: ./_sources/examples/tutorial.txt
.. _positions.rst: ./_sources/examples/positions.txt
.. _Reveal.js: http://lab.hakim.se/reveal-js/
