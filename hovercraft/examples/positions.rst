:title: Positioning tutorial

This is a tutorial for Hovercraft! positioning. It's meant to be read as 
source code, and not as a finished presentation.

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

You don't have to gove both X and Y coordinates. They will default to "no
differece to the last slide" if not given. As the first slide ends up at
X=0 and Y=0, the ``:data-x: 0`` above is strictly speaking not necessary.

----

Automatic positioning
=====================

If you don't set a position, Hovercraft! will position the slide
automatically, by simply continuing in the same direction and length as the
last slide. This slide has no positioning at all, and that means it will end
up at X=0 and Y=2000.


----

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
:data-y: 6000

Zoom out!
=========

So here we rotated 90 degrees and zoomed out five times.

----

:data-x: -1000

Sticky data!
============

All fields except data-x and data-y are "sticky!" That means that
they keep the same value as the last slide. So this slide will
keep the 90 degree rotation and scale of 5.

But I set the X position to -1000, so we now move on the X-scale instead.
Negative numbers are not a problem.

----


Relative positions
==================

One thing that *is* a problem is the absolute positioning. All the positions
we used so far above are in relation to the start of the coordinate system.
But if we no need to insert a slide somewhere in between the slides above, we
need to make room for it, and that means we have to reposition all the slides
that come after. That quickly becomes annoying.

Hovercraft! therefore supports relative positioning where you just give a
relative coordinate to the last slide.

----

:data-scale: 0.1
:data-y: r-500
:data-x: r350
:data-rotate: 0

Like this!
==========

You just prefix the position with an ``r`` and it becomes relative. That
means that if the previous slide moves, this moves with it. You'll find that
it's generally good practice to use mostly relative positioning if you are
still flexible about what your slides are and what they should say or
in which order.

For some types of presentation, where typography is important, you need to
decide everything that the slide should say and their position from the
start. Then absolute positioning works fine. But otherwise you probably want
to use relative positioning.
