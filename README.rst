.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=79D9YLVGVYNHN

=======
Bligify
=======
.. image:: http://i.imgur.com/O6DxDxo.gif
.. contents::

Installation
============
You will need to download the appropriate zip file for your system,
navigate in Blender to File > User Preferences > Add-ons > Install
Add-on from File... and install the zip file you downloaded.

If you are using an operating system other than Windows, you will also
need to install ImageMagick and Gifsicle.

You'll find the Bligify tool in the "Tools Tab."

Windows
-------
Install using the "Bligify_Windows.zip" file from the `latest release`_.

This zip file contains the necessary executables from ImageMagick and
Gifsicle for Windows 64 bit operating systems.

Mac
---
Install using the "Bligify.zip" file from the `latest release`_.

You can install both ImageMagick and Gifsicle using Homebrew_

.. _Homebrew: https://brew.sh/

To install Homebrew, open a terminal and paste this command into the
terminal and press enter:

    `/usr/bin/ruby -e "$(curl -fsSL
    https://raw.githubusercontent.com/Homebrew/install/master/install)"`

To install ImageMagick, enter this into the terminal

    `brew install ImageMagick`

To install Gifsicle, enter this into the terminal

    `brew install gifsicle`

Linux
-----
Install using the "Bligify.zip" file from the `latest release`_.

Installation of Gifsicle and ImageMagick is dependent on your system.

If you're using Arch linux, this addon is available on the Arch User
Repository as blender-plugin-bligify_

.. _blender-plugin-bligify: https://aur.archlinux.org/packages/blender-plugin-bligify/

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

.. _ImageMagick: https://www.imagemagick.org/script/index.php
.. _Gifsicle: https://www.lcdf.org/gifsicle/

.. _latest release: https://github.com/doakey3/Bligify/releases
