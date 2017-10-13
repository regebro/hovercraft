
.. |br| raw:: html
        
        <br />

---- 

Media directives
=================

* New video directive
* New audio directive
* Image directive extended |br| (and hopefully improved)

---- 

Video and audio directives
===========================

* Syntax familiar from image directive
* Support for multiple sources and multiple tracks (subtitles)
* Video takes up the full window by default
* Optional full window display also extended to image directive
* Nice javascript to make audio autoplay on slide enter |br| (autoplay can be overiden)

---- 

Video
======

::

        .. video:: filename.ogg https://upload.wikimedia.org/wikipedia/commons/transcoded/d/d5/Elephants_Dream.ogv/Elephants_Dream.ogv.240p.webm 
                :class: someGreatClassName anotherClassName
                :no_fullscreen:
                :track: filename (en_AU)
        
                * filename1 (chapters es) "chapter list"
                * filename2 (captions dutch) "label"

---- 

* any number of sources may be given after the '::'
* sources are seperated by spaces.
* sources may be relative paths or urls
* options can be key-value pairs (eg. :class:) or flags (eg. :no_fullscreen:)

---- 

* Video supports the following key:value options
        + description: "string"
                - useful for your own reference or if presentation is used with screen reader
        + class: list of css class names
        + height: any valid css height. If no suffix given, px is assumed
                - option prevents fullscreen
        + id: css id
        + name: name that will be used to link to video from elsewhere in presentation
        + style: any valid css that is allowed in html style attribute
        + width: same as :height:
        + track: a single valid track description (see below)
                - If a track is specified in the options list it has the 'default' attribute added to it
        + poster: path/url to image to display before playback
        + crossorigin: this can be 'attributes', 'use-credentials' or 'none'. See below for more.

---- 

* and the following flags:
        + loop:
        + muted:
        + no_autoplay:
        + no_controls:
        + no_preload:
        + no_fullscreen:

---- 

Tracks
=======

* Tracks provide time synchronised text
* Five kinds of track
        + subtitles: this is default if no explict kind is given
        + captions: subtitles + description of sound effects (suitable for deaf individuals)
        + descriptions: text description of video (suitable for blind individuals using a screen reader)
        + chapters: defines chapters
        + metadata: metadata - no visible to users
* languages:
        + should be BCP 47 language code
        + hovercraft will automagically convert most language names to their BCP 47 code
* Label: a user-readable description of the track
        + if no label is given, the kind and the language name are combined to produce the label

---- 

Track filetypes
================

At present, only WEBVTT is supported by the major browsers, however, the html5 spec does not specify a particular filetype and roll-your-own video and audio players tend to support a wider range of track filetypes.

---- 

Sources from other other domains
=================================

If you link directly to a video, audio, image or track from a different domain to your presentation (eg. if you link to a youtube video), browsers will frequently complain. To get around this, elements where the source begins with 'http' (ie. are not local), have the attribute 'crossorigin' set to 'anonymous'. This will will not solve all cross-domain issues, but it will solve some. If you want to prevent this behaviour set the crossorigin option to 'none'. You can also set crossorigin to 'use-credentials' or 'anonymous' if you want to force either of those settings.

**Note**: Saving your presentation to a file rather than serving from localhost:8000 can also help with crossorigin problems.

---- 

Audio
====== 

Much the same as Video, but without support for fullscreen or poster.

**Note**: Support for <track> within <audio> on most browsers. `Captionjs<http://captionatorjs.com/>`_ or other polyfill libraries will be required until this issue is addressed.

---- 

Image
======

* Any image that works with the old image directive should still work with the new one.
* Added :fullscreen: option (not on by default, unlike video)
* Added :id: and :style: options

---- 

And some examples...
=====================

---- 

A video with autoplay disabeled, a poster, and a subtitle track.

----

.. video:: https://upload.wikimedia.org/wikipedia/commons/transcoded/6/63/Elephants_Dream_1024.avi.w400vbr180abr48c2two-pass.ogv/Elephants_Dream_1024.avi.w400vbr180abr48c2two-pass.ogv.160p.webm https://upload.wikimedia.org/wikipedia/commons/transcoded/d/d5/Elephants_Dream.ogv/Elephants_Dream.ogv.240p.webm 
        :poster: https://upload.wikimedia.org/wikipedia/commons/e/e8/Elephants_Dream_s5_both.jpg
        :no_autoplay:
        :track: https://raw.githubusercontent.com/gpac/gpac/master/tests/media/webvtt/elephants-dream-subtitles-en.vtt (subtitles en) "Fantastic subtitles in English"

        * https://raw.githubusercontent.com/gpac/gpac/master/tests/media/webvtt/elephants-dream-subtitles-de.vtt (german)
        * https://raw.githubusercontent.com/gpac/gpac/master/tests/media/webvtt/elephants-dream-chapters-en.vtt (chapters en)

---- 

Some audio with autoplay on step enter, and pause on step exit

---- 

.. audio:: https://ableplayer.github.io/ableplayer/media/paulallen.ogg https://ableplayer.github.io/ableplayer/media/paulallen.mp3
        :track: https://ableplayer.github.io/ableplayer/media/paulallen_meta.vtt (subtitles en) "Unrelated captions in Englsih"

---- 

And an image with width set to 100%

---- 

.. image:: https://upload.wikimedia.org/wikipedia/commons/a/a8/Pinneberg_%28Helgoland%29_2.jpg
        :width: 100%

---- 

Versus the same image with :fullscreen: option

---- 

.. image:: https://upload.wikimedia.org/wikipedia/commons/a/a8/Pinneberg_%28Helgoland%29_2.jpg
        :fullscreen: 

