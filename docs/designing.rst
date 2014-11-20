Designing your presentations
============================

There are several tricks to making presentations. I certainly do not claim to
be an expert, but here are some beginners hints.


Take it easy
------------

Don't go too heavy on the zoom. Having a difference between two slides in
scale of more than 5 is rarely going to look good. It would make for a nice
cool zooming effect if it did, but this is not what browsers are designed
for, so it won't.

And the 3D effects can be really cool if used well. But not all the time,
it gets tiring for the audience.

Try, if you can, to use the zoom and 3D effects when they make sense in the
presentation. You can for example mention the main topics on one slide, and
then zoom in on each topic when you discuss it in more detail. That way the
effects help clarify the presentation, rather than distract from it.


Custom fonts
------------

Browsers tend to render things subtly differently.

They also have different default fonts, and different operating systems have
different implementations of the same fonts. So to make sure you have as much
control over the design as possible, you should always include fonts with the
presentation. A good source for free fonts are Google Webfonts_. Those fonts
are free and open source, so you can use them with no cost and no risk of
being sued. They can also be downloaded or included online.

Online vs Downloaded
^^^^^^^^^^^^^^^^^^^^

If you are making a presentation that is going to run on your computer at a
conference or customer meeting, always download the fonts and have them
as a part of the presentation. Put them in a folder called ``fonts``
under the folder where your presentation is.

You also need to define the font-family in your CSS. `Font Squirrel`_'s
webfont generator will provide you with a platform-independent toolkit for
generating both the varius font formats and the CSS.

If the presentation is online only, you can put an ``@include``-statement in
your CSS to include Googles webfonts directly::

    @import url(http://fonts.googleapis.com/css?family=Libre+Baskerville|Racing+Sans+One|Satisfy);

But don't use this for things you need to show on your computer, as it
requires you to have internet access.


Test with different browsers
----------------------------

If you are putting the presentation online, test it with a couple of major
browsers, to make sure nothing breaks and that everything still looks good.
Not only are there subtle differences in how things may get positioned,
different browsers are also good at different things.

I've tested some browsers, all on Ubuntu, and it is likely that they behave
differently on other operating systems, so you have to try for yourself.


Firefox
^^^^^^^

Firefox 18 is quite slow to use with impress.js, especially for 3D stuff, so
it can have very jerky movements from slide to slide. It does keep text
looking good no matter how much you zoom. On the other hand, it refuses to
scale text infinitely, so if you scale too much characters will not grow
larger, they will instead start moving around.

Firefox 19 is better, but for 3D stuff it's still a bit slow.

Chrome
^^^^^^

Chrome 24 is fast, but will not redraw text in different sizes, but will
instead create an image of them and rescale them, resulting in the previous
slide having a fuzzy pixelated effect.

Epiphany
^^^^^^^^

Epiphany 3.4.1 is comparable to Firefox 19, possibly a bit smoother, and the
text looks good. But it has bugs in how it handles 3D data, and the location
bar is visible in fullscreen mode, making it less suitable for any sort of
presentation.

.. _Webfonts: http://www.google.com/webfonts
.. _Font Squirrel: http://www.fontsquirrel.com/
