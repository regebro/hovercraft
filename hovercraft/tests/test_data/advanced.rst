.. title:: Presentation title

:data-transition-duration: 2000
:auto-console: True
:css-screen: extra.css


This is an advanced presentation. It doesn't have a section in the first
step, meaning the first step will not be a step at all, but a sort of
introductory comment about the presentation, that will not show up in the
presentation at all.

It also sets a title and a transition-duration.

----

:data-x: 1000
:data-y: 1600

Advanced Presentation
=====================

Here we show the positioning feature, where we can explicitly set a position
on one of the steps.

----

:id: name-this-step
:data-x: r1600

Formatting
==========

Let us also try some basic formatting, like *italic*, and **bold**.

* We can also
* have a list
* of things.

----

There should also be possible to have
preformatted text for code.

.. code:: python

    def foo(bar):
        # Comment
        a = 1 + "hubbub"
        return None


----

An image, with attributes:

.. image:: images/hovercraft_logo.png
    :class: imageclass
    :width: 50%

----

Character sets
==============

The character set is UTF-8 as of now. Like this: åäö.
