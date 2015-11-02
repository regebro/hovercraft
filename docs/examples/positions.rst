:title: Positioning tutorial
:css: tutorial.css

This is a tutorial for Hovercraft! positioning. It's meant to be read as
`source code <../_sources/examples/positions.txt>`_.

You can render this presentation to HTML with the command::

    hovercraft positions.rst outdir

And then view the outdir/index.html file to see how it turned out.

If you are seeing this text, and not reading this as source code, you are
doing it wrong! It's going to be confusing and not very useful.

Use The Source, Luke! But first you probably want to read through the
official documentation at https://hovercraft.readthedocs.org/
There are links to the source code in the Examples section.

----

Positions
=========

Each step can be explicitly positioned by putting some ``data-`` fields in
the beginning of the slide. This has to be first in the slide (although you
have to have a blank line beneath the four dashes that start the slide.

To put the slide at zero pixels to the right and a thousand pixels below the
coordinate centre you add the following::

    :data-x: 0
    :data-y: 1000

Let's do that for the next slide:

----

:data-x: 0
:data-y: 1000

X & Y
=====

You don't have to give both X and Y coordinates. They will default to "no
difference from the last slide" if not given. As the first slide ends up at
X=0 and Y=0, the ``:data-x: 0`` above is strictly speaking not necessary.

----

:data-x: 2000
:data-y: 1000

Positioning fields
==================

Any field starting with ``data-`` will be converted to a ``data-`` attribute
on the impress.js step. There is no filtering done, so if new attributes are
supported by impress.js, they should just work from Hovercraft! as well.

The ones impress.js currently uses are::

    data-x          Position on the X-axis
    data-y          Position on the Y-axis
    data-z          Position on the Z-axis (which means 3D!)
    data-rotate     Rotation in degrees
    data-rotate-z   An alias for data-rotate
    data-rotate-x   Rotation on the X-axis, which agains means 3D effects
    data-rotate-y   Rotation on the Y-axis
    data-scale      The size of the slide, which means zooming effects

Let's do some zoom and rotate!

----

:data-scale: 5
:data-rotate: 90
:data-x: 3000
:data-y: 1000

Zoom out!
=========

So here we rotated 90 degrees and zoomed out five times.

----

:data-scale: 1
:data-x: 4000
:data-y: 2000

Relative positions
==================

One thing that *is* a problem is the absolute positioning. All the positions
we used so far above are in relation to the start of the coordinate system.
But if we now need to insert a slide somewhere in between the slides above,
we need to make room for it, and that means we have to reposition all the
slides that come after. That quickly becomes annoying.

Hovercraft! therefore supports relative positioning where you just give a
relative coordinate to the last slide.

----

:data-x: r1000

Like this
=========

You just prefix the position with an ``r`` and it becomes relative. That
means that if the previous slide moves, this moves with it. You'll find that
it's generally good practice to use mostly relative positioning if you are
still flexible about what your slides are and what they should say or
in which order.

For some types of presentation, where typography is important, you need to
decide everything that the slide should say and their position from the
start. Then absolute positioning works fine. But otherwise you probably want
to use relative positioning.

----

:data-rotate: r15

Automatic positioning
=====================

Every field will retain it's last value if you don't specify a new one.
In this case, we keep a r1000 value for data-x and introduce a new
r15 value for data-rotate. This and the next slide will therefore
move right 1000 pixels and rotate 15 degrees more for each slide.

It looks like it moves "up" because we are already rotated 90 degrees.

----

:data-scale: 0.15

**A warning!**
==============

----

:data-x: r1000
:data-scale: 1

Didn't that slide look good?
============================

Don't worry, when you make big zooms, different browsers will behave
differently and be good at different things. Some will be slow and jerky on
the 3D effects, and others will show fonts with jagged edges when you zoom.
Older and less common browsers can also have problems with 3D effects.

----

:hovercraft-path: m275,175 a150,150 0 0,1 -150,150

SVG paths
=========

The field ``:hovercraft-path:`` tells Hovercraft! to place the slides
along a SVG path. This enables you to put slides along a graphical shape.

----

SVG paths
=========

You can design the shape in a vector graphics program like Inkscape
and then lift it out of the SVG file (which are in XML) and use it
in Hovercraft!

This example is an arc.

----

SVG paths
=========

Using SVG path so is not entirely without it's difficulties and
surprises, and this is discussed more in the documentation, under
the SVG Paths heading.

----

SVG paths
=========

Every following slide will be placed along the path,
and the path will be scaled to fit the slides.

----

:data-rotate: -180
:data-x: r-1200

SVG paths
=========

And the positioning along the path will end when you get a path that has
explicit positioning, like this one.

----

:data-rotate-y: -45
:data-y: r-100
:data-x: r-800

3D!
===

Now it get's complicated!

----

:data-rotate-y: 0
:data-y: r100
:data-x: r-1000

3D Rotation
===========

We have already seen how we can rotate the slide with ``:data-rotate:``. This is actually rotation
in the Z-axis, so you can use ``:data-rotate-z:`` as well, it's the same thing.
But you can also rotate in the Y-axis.

----

:data-x: r0
:data-y: r0
:data-rotate-y: 90

3D Rotation
===========

That was a 90 degree rotation in the Y-axis.
Let's go back.

----

:data-x: r0
:data-y: r0
:data-rotate-y: 0

----

:data-x: r-1000
:data-y: r0
:data-rotate-y: 0

3D Rotation
===========

Notice how the text was invisible before the rotation?
The text is there, but it has no depth, so you can't see it.
Of course, the same happens in the X-axis.

----

:data-x: r0
:data-y: r0
:data-rotate-x: 90

3D Rotation
===========

That was a 90 degree rotation in the X-axis.
Let's go back.

----

:data-x: r0
:data-y: r0
:data-rotate-x: 0

----

:data-x: r-1000

3D Positioning
==============

You can not only rotate in all three dimensions, but also position in all
three dimensions. So far we have only used ``:data-x`` and ``:data-y``, but
there is a ``:data-z`` as well.

----

:data-z: 1000
:data-x: r0
:data-y: r-50

Z-space
=======

----

:data-x: r0
:data-y: r-500

Z-space
=======

This can be used for all sorts of interesting effects. It should be noted
that the depth of the Z-axis is quite limited in some browsers.

If you set it too high, you'll find the slide appearing low and upside down.

----

:data-x: r800
:data-y: r0

Z-space
=======

But well used it can give an extra wow-factor,

----

:data-z: 0
:data-x: r100
:data-y: r-200
:data-scale: 1

and make text pop!
==================

----

:data-x: r3000
:data-y: r-1500
:data-scale: 15
:data-rotate-z: 0
:data-rotate-x: 0
:data-rotate-y: 0
:data-z: 0


That's all for now
==================

*Have fun!*

