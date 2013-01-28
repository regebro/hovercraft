Hovercraft
==========

Hovercraft will be a tool to make impress.js_ presentations from
reStructuredText. You may at this point ask "Why!?" and it is a reasonable
question, as there are other ways of doing it, including landslide-impress,
a template for Landslide that create an impress.js presentation.

The reason is that I ran into a limitation of Landslide. There was no way to
get the position information out from the reStructuredText to impress.js.

The tools that exist to layout impress.js presentations manually are still in
alpha-state, and doesn't work very well. They also do not support having
presenter notes via impress-console_, a feature I of course need.

So, I have to make something myself. Hence: Hovercraft!

This is still in pre-alpha mode, but I've gotten to the state that I'm now
fairly certain that this is feasible, and not even that complicated.

Lennart Regebro <regebro@mail.com>

.. _impress.js: http://github.com/bartaz/impress.js
.. _landslide-impress: https://github.com/regebro/landslide-impress
.. _impress-console: https://github.com/regebro/impress-console
