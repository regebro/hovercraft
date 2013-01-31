Presentations
=============

A note on terminology
---------------------

Traditionally a presentation is made up of slides. Calling them "slides" is
not really relevant in an impress.js context, as they can overlap and doesn't
necessarily slide, but can zoom, roll and pitch. The name "steps" is
better, but it's also more ambigiouos. Hence Impress.js uses the terms "slide"
and "step" as meaning the same thing, and so does Hovercraft!


Hovercraft! syntax
------------------

Presentations are reStructuredText files. TODO: Find links for good
reStructuredText manuals. If you are reading this documentation from the
source code, then you are looking at a reStructuredText document already.

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


.. _documentation: http://docutils.sourceforge.net/docs/index.html
.. _book: http://python3porting.com/