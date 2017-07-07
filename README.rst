.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=79D9YLVGVYNHN

=======
Bligify
=======

.. contents::

Installation
============

Download the repository.

.. image:: http://i.imgur.com/NvrcI8I.gif

Install the addon

1. Open Blender.
2. Go to File > User Preferences > Addons
3. Click "Install From File" and navigate to the downloaded zip file
4. Check the box next to "Sequencer:Bligify"
5. Save user settings

The addon interface is on the right side of the sequencer

.. image:: http://i.imgur.com/QXvwNad.gif

Note: If using Linux, you must install Gifsicle and ImageMagick.

Currently, the addon does not work on Mac.

Usage
=====

A `Tutorial Video`_ is available for an early version of the addon.

.. _Tutorial Video: https://www.youtube.com/watch?v=eCdI6hfqsK8&feature=youtu.be

GIF Quality
-----------

.. image:: http://i.imgur.com/LEpKMXP.png

You can adjust the settings to fine-tune the quality of your animated
GIF (and it's filesize). For most situations, the default settings
should give good results. You can learn more about each of the settings
by hovering your mouse over them or by reading the `Gifsicle Manpage`_

.. _Gifsicle Manpage: https://www.lcdf.org/gifsicle/man.html

FPS Adjustment
--------------

High frame rates will make output filesize much larger. You can easily
adjust a video's frame rate with the FPS adjust tool. It changes the
scene FPS value and adds a speed modifier to selected clips to maintain
playback speed.

.. image:: http://i.imgur.com/njWvf7S.gif

I recommend you try setting the Dither to "Floyd-Stienberg" and checking
the box that says "Dither Conversion". These 2 properties typically make
good quality GIFs that are also small. They can cause artifacts, so they
are not enabled by default.

Render GIF
----------

Render the animation to PNG files. Convert those PNGs to GIFs. Finally,
convert the GIFs to an animated GIF.

.. image:: http://i.imgur.com/pvydLO8.gif

Import GIF
----------

Separate an animated GIF into it's frames. Convert those GIFs to PNGs
and import the PNGs into the sequencer.

.. image:: http://i.imgur.com/lhjCOCG.gif

Bligify to ODP
==============

Making unlooped GIFs work right in slideshow presentations can be 
difficult. While you might expect an unlooped GIF to play, then stop
on the last frame--the way it does in an internet browser--this is not
the behavior of GIFs inside PowerPoint or LibreOffice Impress. Instead,
GIFs will play, then stop on the first frame of the animation.

This problem is overcome by making the first frame of the animated GIF
invisible, then hiding a still image of the first and last frames of the 
animation underneath the GIF. This part of the Bligify addon will set 
this up for you.

Set the loop count to 1, adjust the offset, aspect ratio, and border
thickness as desired and click the Render ODP button.

How it Works
============

Inside the addon, there are 2 executables, namely: convert.exe (from
ImageMagick) and gifsicle.exe. The addon is really just a front-end for
these two programs.

.. image:: http://i.imgur.com/O6DxDxo.gif
