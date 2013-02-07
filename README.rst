Hovercraft!
===========

*The merging of convenience and cool!*

Hovercraft! is a tool to make impress.js_ presentations from
reStructuredText. Documentation is currently sparse, but available in the
documentation subdirectory.

Why?
----

As a programmer, I like making my presentations in some sort of text-markup.
GUI tools feel restricted and limited when it comes to creating the
presentation, simply writing it in text makes it easier to move things around
as you like.

But the tools that exist to make presentations from text-markup will make
slideshows that has a sequence of slides from left to right. That was fine
until Prezi arrived, with zooms and slides and twists and turns.

But Prezi is a GUI toool. And it's closed source. But the open source
community fixed that problem with impress.js.

But impress.js is an HTML tools. Sitting and writing HTML is an annoying
pain. It's not a very smooth tool compared reStructuredText or markdown.
It's especially annoying since you have to sit and add x/y/zoom/rotation
for each slide, and if you insert a new slide in the middle, you have to
change everything around.

There are GUI tools to layout impress.js presentations but they are all in
alpha-state, and doesn't work very well. They also do not support having
presenter notes via impress-console_, a feature I of course need. After all,
that's why I wrote it.

So, I wanted to make impress.js presentations from reStructuredText. That
turned out to be easy, I make landslide-impress_, a template for Landslide
that create an impress.js presentation. But I ran into a limitation of
Landslide. There was no way to get the position information out from the
reStructuredText to impress.js. As such, with Landslide all I could do with
impress.js was slides that boringly went from left to right, completely
losing the whole point of impress.js.

So, I have to make something myself. Hence: Hovercraft!

TODO
----

* Add a parameter to not show the help pop up when starting.

* Add a keybinding to pop up the help when pressing "h".

* A parameter to skip the presentation notes for web-publishing.

* Somehow specify what DEFAULT_MOVEMENT should be.

Future features:
................

* Perhaps support a directory of infiles, Sphinx-style?
  
Contributors
------------

Hovercraft! was written by Lennart Regebro <regebro@mail.com>, and is licensed
as CC-0, except for the following:

* ``reST.xsl`` is (c) Michael Alyn Miller <malyn@strangeGizmo.com> and
  published under a BSD-style license included in reST.xsl itself.

* ``impress.js`` is (c) Bartek Szopka (@bartaz) released under MIT and GPL
  licenses. See the impress.js_ page for more information.

.. _impress.js: http://github.com/bartaz/impress.js
.. _landslide-impress: https://github.com/regebro/landslide-impress
.. _impress-console: https://github.com/regebro/impress-console
