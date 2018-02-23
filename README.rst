.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=79D9YLVGVYNHN

=======
Bligify
=======
.. image:: http://i.imgur.com/O6DxDxo.gif
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

If you have a video loaded into the VSE, you'll find Bligify in the
"Tools Tab."

Dependencies
------------
Bligify requires ImageMagick_ and Gifsicle_ to work.

Windows
~~~~~~~
For ImageMagick_, use the installer provided on their downloads page.

For Gifsicle, download the executable and add the path to the folder
containing the executable to your system's PATH environment variable.

Alternatively, you can download the `old 1.3.4 release`_ of Bligify
which had these executables packaged as part of the addon.

.. _old 1.3.4 release: https://github.com/doakey3/Bligify/releases/tag/1.3.4

MAC
~~~
You can install both ImageMagick and Gifsicle using Homebrew_

.. _Homebrew: https://brew.sh/

To install Homebrew, open a terminal and paste this command into the
terminal and press enter:

    `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

To install ImageMagick, enter this into the terminal

    `brew install ImageMagick`

To install Gifsicle, enter this into the terminal

    `brew install gifsicle`

Linux
~~~~~
Installation of Gifsicle and ImageMagick is dependent on your system.
Using Arch Linux, installation is like this:

    `sudo pacman -S gifsicle imagemagick`

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
The older version of the addon had a feature which allowed users to
export addons to a Libreoffice Impress presentation. This feature will
be moved to a separate addon.

.. _ImageMagick: https://www.imagemagick.org/script/index.php
.. _Gifsicle: https://www.lcdf.org/gifsicle/
