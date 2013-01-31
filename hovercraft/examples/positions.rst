.. title:: Slideshow title

:data-transition-duration: 2000
:data-x: 200
:data-y: 500

Positions
==========

Each step can be explicitly positioned by putting some ``step-`` fields in
the beginning of the step.

----

:step-x: 200
:step-y: 500
:step-z: -2000
:step-rotate: 90
:step-scale: 5
:step-foo: bar

Any field starting with ``step-`` will be converted to a ``data-`` attribute
on the impress.js step. There is no filtering done, so if new attributes are
supported by impress.js, they should just work from Hovercraft as well.

Any field starting with ``presentation-`` will be set as a ``data-``
attribute on the presentation div as a whole. This is most useful for setting
the default transition duration.

----

steps that has no explicit positioning will get a calculated position.
By default this will create a simple left-to-right stepshow.

----

Title
=====

Text

Subtitle
--------

Textext
