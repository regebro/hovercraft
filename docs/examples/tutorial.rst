:title: Slideshow Tutorial
:author: Lennart Regebro
:description: The Hovercraft! tutorial.
:keywords: presentation, restructuredtext, impress.js, tutorial
:css: tutorial.css

.. header::

    .. image:: images/hovercraft_logo.png

.. footer::

   Hovercraft! Tutorial, https://hovercraft.readthedocs.io

This slide show is a sort of tutorial of how to use Hovercraft! to make
presentations. It will show the most important features of Hovercraft! with
explanations.

Hopefully you ended up here by the link from the official documentation at
https://hovercraft.readthedocs.io/ . If not, you probably want to go there
and read through it first.

This tutorial is meant to be read as source code, not in any HTML form, so if
you can see this text (it won't be visible in the final presentation) and you
aren't seeing the source code, you are doing it wrong. It's going to be
confusing and not very useful. Again, go to the official docs. There are
links to the source code in the Examples section.

You can render this presentation to HTML with the command::

    hovercraft tutorial.rst outdir

And then view the outdir/index.html file to see how it turned out.

**Now then, on to the tutorial part!**

The first thing to note is the special syntax for information about the
presentation that you see above. This is in reStructuredText called "fields"
and it's used all the time in Hovercraft! to change attributes and set data
on the presentation, on slides and on images. The order of the fields is not
important, but you can only have one of each field.

The fields above are meta-data about the presentation, except for the
:css:-field. This meta data is only useful if you plan to publish the
presentation by putting the HTML online. If you are only going to show this
presentation yourself in a meeting you can skip all of it.

The title set is the title that is going to be shown in the title bar of the
browser. reStructuredText also has a separate syntax for titles that is also
supported by Hovercraft::

    .. title:: Slideshow Tutorial

However that requires an empty line after it, and it looks better to use the
same syntax for all metadata.

The :css: field will add a custom CSS-file to this presentation. This is
something you almost always want to do, as you otherwise have no control over
how the presentation will look. You can also specify different media for
the CSS, for example "screen,projection"::

    :css-screen,projection: hovercraft.css

This way you can have different CSS for print and for display. You can only
specify one CSS-file per field, however. If you want to include more you
need to use the @import directive in CSS.

Once you have added metadata and CSS, it's time to start on the slides.

You separate slides with a line that consists of four or more dashes. The
first slide will start at the first such line, or at the first heading. Since
none of the text so far has been a heading, it means that the first slide has
not yet started. As a result, all this text will be ignored in the output.

So lets start the first slide by having a line with four dashes. Since the
first slide starts with a heading, that line is strictly speaking not needed,
but it's good to be explicit.

----

This is a first slide
=====================

Restructured text takes any line that is underlined with punctuation and
makes it into a heading. Each type of underlining will be made into a different
level of heading, but it is not the type that is important, but rather the
order of which each type will be enountered.

So in this presentation, lines underlined with equal (=) characters will be
made into a first-level (H1) heading.

----

First header
============

You can choose other punctuation characters as your level 1 heading if you like,
but this is the most common. Any if these character works::

    = - ` : ' " ~ ^ _ * + # < > .

Second header
-------------

Third header
............

The drawback with reStructuredText is that you can't skip levels. You can't
go directly from level 1 to level 3 without having a level 2 in between.
If you do you get an error::

    Title level inconsistent

----

Other formatting
================

All the normal reStructuredText functions are supported in Hovercraft!

- Such as bulletlists, which start with a dash (-) or an asterisk (*).
  You can have many lines of text in one bullet if you indent the
  following lines.

   - And you can have many levels of bullets.

       - Like this.

- There is *Emphasis* and **strong emphasis**, rendered as <em> and <strong>.

----

More formatting
===============

#. Numbered lists are of course also supported.

#. They are automatically numbered.

#. But only for single-level lists and single rows of text.

#. ``inline literals``, rendered as <tt> and usually shown with a monospace font, which is good for source code.

#. Hyperlinks, like Python_

.. _Python: http://www.python.org


----

Images
======

You can insert an image with the .. image:: directive:

.. image:: images/hovercraft_logo.png

And you can optionally set width and height:

.. image:: images/hovercraft_logo.png
    :width: 50px
    :height: 130px

Some people like to have slideshows containing only illustrative images. This
works fine with Hovercraft! as well, as you can see on the next slide.

----

.. image:: images/hovercraft_logo.png

----

Slides can have presenter notes!
================================

This is the killer-feature of Hovercraft! as very few other tools like this
support a presenter console. You add presenter notes in the slide like this:

.. note::

    And then you indent the text afterwards. You can have a lot of formatting
    in the presenter notes, like *emphasis* and **strong** emphasis.

    - Even bullet lists!

    - Which can be handy!

    But you can't have any headings.


----

Source code
===========

You can also have text that is mono spaced, for source code and similar.
There are several syntaxes for that. For code that is a part of a sentence
you use the inline syntax with ``double backticks`` we saw earlier.

If you want a whole block of preformatted text you can use double colons::

    And then you
    need to indent the block
    of text that
    should be preformatted

You can even have the double colons on a line by themselves:

::

    And this text will
    now be
    rendered as
    preformatted text

----

Syntax highlighting
===================

But the more interesting syntax for preformatted text is the .. code::
directive. This enables you to syntax highlight the code.

.. code:: python

    def day_of_year(month, day):
        return (month - 1) * 30 + day_of_month

    def day_of_week(day):
        return ((day - 1) % 10) + 1

    def weekno(month, day):
        return ((day_of_year(month, day) - 1) // 10) + 1

----

More code features
==================

The syntax highlighting is done via docutils by a module called Pygments_
which support all popular languages, and a lot of unpopular ones as well.

The coloring is done by CSS, if you want to change it, copy the CSS in
the highlight.css file and override it in your custom CSS.

.. _Pygments: http://pygments.org/

----

Testing the code
================

If you are including Python-code, then Manuel_ 1.7.0 and later can test the
code for you. This enables you to have code in your presentation and make
sure it works.

To do this properly you sometimes want setup and teardown code, code that
should be executed as a part of the test, but not shown in the presentation.

To do that, you can simply set a class on the code block.

.. code:: python
    :class: hidden

    from datetime import datetime

Add the hidden class in your css:

.. code:: css

    pre.hidden {
        display: none;
    }

----

And your visible code will now be runnable with Manuel:

.. code:: python

   >>> datetime(2013, 2, 19, 12)
   datetime.datetime(2013, 2, 19, 12, 0)

.. _Manuel: https://pypi.python.org/pypi/manuel

----

Render mathematics!
===================

Mathematical formulas can be rendered with Mathjax!

.. math::

    e^{i \pi} + 1 = 0

    dS = \frac{dQ}{T}

And inline: :math:`S = k \log W`

.. _Mathjax: https://www.mathjax.org/

----



That's all folks!
=================

That finishes the basic tutorial for Hovercraft! Next you probably want to
take a look at the positioning tutorial, so you can use the pan, rotate and
zoom functionality.
