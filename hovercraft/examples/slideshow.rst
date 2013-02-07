.. title:: Slideshow title

:author: Me!
:data-x: 200
:data-y: 500

Hovercraft
==========

A reStructuredText to impress.js slideshow generator.

----

Four (or more) dashes is reStructuredText for a "transition". We use that as
a separator between slides, mainly for compatibility with Landslide.

----

Slides can have Titles
======================

And subtitles
-------------

And subsubtitles
^^^^^^^^^^^^^^^^

All the normal reStructuredText functions are supported.

- Such as bulletlists

  With text under them.

- *Emphasis* and **strong emphasis**

- ``inline literals``

- `I don't know what interpreted text is`

But I guess I'll find out.

#. Numbered lists is of course also supported.

#. Hyperlinks, like Python_

.. _Python: http://www.python.org


----

A slide with only a title!
==========================

----

A slide with a title!
=====================

And a subtitle
---------------

----

It is also supported to insert images.

.. image:: images/_dead_10.jpg

And more importantly, to have slides with nothing but an image, as the next
slide.

----

.. image:: images/_dead_10.jpg

----

Slides can have presenter notes!
================================

You put them under a heading called "Presenter Notes".

Presenter Notes
---------------

This will show up as presenter notes, but not in the slide.

----

.. image:: images/rome-pathway_to_power.jpg

Presenter Notes
---------------

It's important that a slide with just an image can have presenter notes. 
This was a bug in landslide.

----

::

    def day_of_year(month, day):
        return (month - 1) * 30 + day_of_month
    
    def day_of_week(day):
        return ((day - 1) % 10) + 1 
    
    def weekno(month, day):
        return ((day_of_year(month, day) - 1) // 10) + 1

Presenter Notes
---------------

We also of course need code blocks.

----

:data-x: 200
:data-y: 500

impress.js support
==================

Is done by setting position 

----

That's it so far!
