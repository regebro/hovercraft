Presentations
=============

A note on terminology
---------------------

Traditionally a presentation is made up of slides. Calling them "slides" is
not really relevant in an impress.js context, as they can overlap and doesn't
necessarily slide. The name "steps" is better, but it's also more ambigiouos.
Hence Impress.js uses the terms "slide" and "step" as meaning the same thing,
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

You can also mark text as *italic* or **bold**, and you can have bullet lists::

    * Bullet 1
    
      * Bullet 1.1
    
    * Bullet 2
    
    * Bullet 3

You can include images::

    .. image:: path/to/image.png
        :height: 600px
        :width: 800px
   
As you see you can also specify height and width and loads of other parameters_, but they
are all optional.

And you can mark text as being preformatted, for example when adding example source code::

    ::
    
        # This code here will be preformatted.
        def some_example_code(foo):
            return foo * foo

That is the most important things you'll need to know about reStructuredText for
making presentations. There is a lot more to know, and a lot of advanced features
like links, footnotes, and more. It is in fact advanced enough so you can write a
whole book_ in it, but for all that you need to read the documentation_.


Hovercraft! specialities
------------------------

Hovercraft! has some specific ways it uses reStructuredText. First of all, the
reStructuredText "transition" is used to mark the separation between
different slides or steps. A transition is simply a line with four or more
dashes::

    ----

All reStructuredText fields are converted into attributes on the current tag.
Most of these will typically be ignored by the rendering to HTML, but there
is two places where the tags will make a difference, and that is by putting
them first in the document, or first on a slide.

Any fields you put first in a document will be rendered into attributes on
the main impress.js div. This is currently only used to set the
transition-duration with ``data-transition-duration``.

Any fields you put first in a slide will be rendered into attributes on the
slide div. This is used primarily to set the position/zoom/rotation of the
slide, either with the ``data-x``, ``data-y`` and other impress.js settings,
or the ``hovercraft-path`` setting, more on that later.

Hovercraft! will start making the first slide when it first encounters either
a transition or a header. Everything that comes before that will belong to the
presentation as a whole.

A presentation can therefore look something like this:

::

    .. title: Presentation Title
    
    :data-transition-duration: 2000
    
    ----

    This is the first slide
    =======================
    
    Here comes some text.
    
    ----

    :data-x: 300
    :data-y: 2000

    This is the second slide
    ========================
    
    1. Here we have
    
    1. A numbered list
    
    1. It will get correct 
    
    1. Numbers automatically


Paths
-----

Hovercraft supports positioning slides along and SVG path. This is handy, as
you can create a drawing in a software that supports SVG, and then copy-paste
that drawings path into your presentation.

There are some things you need to be careful about, though.

Relative and absolute coordinates
.................................

In SVG coordinates can either be absolute, that is in reference to the page,
or relative, which is in reference to the last point. Hovercraft can handle
both, but what it can not handle very well is a mixture of them.

Specifically, if you take an SVG path that starts with a relative movement
and extract that from the SVG document, you will lose the context. All
coordinates later must then also be relative. If you have an absolute
coordinate you then suddenly regain the context, and everything after the
first absolute corrdinate will be misplaced compared to the points that come
before.

Most notable, the open source software "Inkscape" will mix absolute and
relative coordinates, if you allow it to use relative coordinates. You
therefore need to go into it's settings and uncheck the checkbox that allows
you to use relative coordinates. This forces Inkscape to save all coordinates
as absolute, which woll work fine.

SVG transforms
..............

SVG allows you to draw up path and then transform it. Hovercraft has no
support for these transforms, so before you extract the path you should make
sure the SVG software doesn't use transforms. In Inkscape you can do this by
the "Simplify" command.

Other SVG shapes
................

Hovercraft doesn't support other SVG shapes, just the path. This is because
organising slides in squares, etc, is quite simple anyway, and the shapes can
be made into paths. Usually in the software you will have to select the shape
and tell your software to make it into a path. In Inkscape, transforming an
object into a path will generally mean that the whole path is made of
CubicBezier curves, which are unecessariy complex. Using the "Simplify"
command in Inkscape is usually enough to make the shapes into paths.

Shape-scaling
.............

Hovercraft will counts how many slides that are to fit into the path you are
using, and it will scale the path accordingly. If you therefore have several
paths in your presentation, they will **not** keep their relative sizes, but
will be resized so the slides fit. If you need to let the shapes keep their
relative sizes, you need to combine them into one object/path.


.. _documentation: http://docutils.sourceforge.net/docs/index.html
.. _parameters: http://docutils.sourceforge.net/docs/ref/rst/directives.html#images
.. _book: http://python3porting.com/