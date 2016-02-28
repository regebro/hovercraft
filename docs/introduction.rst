Introduction
============

GUI tools are limiting
----------------------

I used to do presentations with typical slideshow software, such as
OpenOffice/LibreOffice Impress, but these tools felt restricted and limiting.
I need to do a lot of reorganizing and moving around, and that might mean
changing things from bullet lists to headings to text to pictures and back to
bullet lists over again. This happens through the whole process. I might
realize something that was just a bullet point needs to be a slide, or that a
set of slides for time reasons need to be shortened down to bullet points.
Much of the reorganization comes from seeing what fits on one slide and what
does not, and how I need to pace the presentation, and to some extent even
what kinda of pictures I can find to illustrate what I try to say, and if the
pictures are funny or not.

**Presentation software should give you complete freedom to reorganize your
presentation on every level, not only by reorganizing slides.**

The solution for me and many others, is to use a text-markup language, like
reStructuredText, Markdown or similar, and then use a tool that generates an
HTML slide show from that.

**Text-markup gives you the convenience and freedom to quickly move parts
around as you like.**

I chose reStructuredText_, because I know it and because it has a massive
feature set. When I read the documentations of other text-markup langages it
was not obvious if they has the features I needed or not.


Pan, rotate and zoom
--------------------

The tools that exist to make presentations from text-markup will make
slideshows that has a sequence of slides from left to right. But the fashion
now is to have presentations that rotate and zoom in and out. One open source
solution for that is impress.js_.

**With impress.js you can make modern cool presentations.**

But impress.js requires you to write your presentation as HTML, which is
annoying, and the markup isn't flexible enough to let you quickly reorganize
things from bullet points to headings etc.

You also have to position each slide separately, and if you insert a new
slide in the middle, you have to reposition all the slides that follow.

Hovercraft!
-----------

So what I want is a tool that takes the power, flexibility and convenience of
reStructuredText and allows me to generate pan, rotate and zoom presentations
with impress.js, without having to manually reposition each slide if I
reorganize a little bit of the presentation. I couldn't find one, so I made
Hovercraft.

Hovercraft’s power comes from the combination of reStructuredText’s
convenience with the cool of impress.js, together with a flexible and
powerful solution to position the slides.

There are four ways to position slides:

 #. Absolute positioning: You simply add X and Y coordinates to a slide,
    in pixels. Doing only this will not be fun, but someone might need it.

 #. Relative positioning: By specifying x and/or y with with a starting r,
    you specify the distance from the previous slide. By using this form of
    positioning you can insert a slide, and the other slides will just move
    to make space for the new slide.

 #. Automatically: If you don’t specify any position the slide will have the
    same settings as the previous slide. With a relative positioning, this
    means the slide will move as long as the previous slide moved. This
    defaults to moving 1600px to the right, which means that if you supply
    no positions at all anywhere in the presentation, you get the standard
    slide-to-the-left presentation.

 #. With an SVG path: In this last way of positioning, you can take an
    SVG path from an SVG document and stick it into the presentation, and that
    slide + all slides following that has no explicit positioning will be
    positioned on that path. This can be a bit fiddly to use, but can create
    awesome results, such as positioning the slides as snaking Python or
    similar.

Hovercraft! also includes impress-console_, a presenter console that will
show you your notes, slide previews and the time, essential tools for any
presentation.

.. _reStructuredText: http://docutils.sourceforge.net/docs/index.html
.. _impress.js: http://github.com/bartaz/impress.js
.. _impress-console: https://github.com/regebro/impress-console
