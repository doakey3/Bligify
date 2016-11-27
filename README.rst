.. contents::

Tutorial Video
==============

.. image:: http://i.imgur.com/WFNCAWA.png
    :target: https://www.youtube.com/watch?v=eCdI6hfqsK8&feature=youtu.be


Installation
============

1. Download the repository. 
2. Open Blender. 
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded release
5. Check the box next to "Sequencer:bligify"
6. If using linux, you must install gifsicle and imagemagick.

Usage
=====

The user interface

.. image:: http://i.imgur.com/V5SOzNe.png

GIF Quality
-----------

.. image:: http://i.imgur.com/O6DxDxo.gif
.. image:: http://i.imgur.com/LpOAB1U.gif

Above shows a comparison between leaving the GIF quality on the default
setting (full) and limiting the colors to 64. The output size is 1.2 mb
and 470 kb respectively.

Loop
----

Uncheck this box if you want the GIF to play through once and stop

FPS Adjustment
--------------

Sets the scene FPS to the value in the integer property window. It also
applies a speed modifier to the selected clips to adjust for the slower
frames-per-second setting of the scene.

Render GIF
----------

Click the button, name the output file, and click ok. A progress box
will appear telling you how much time is left.

Import GIF
----------

Click the button, find the file to import, and click ok. The GIf will be
imported as an image sequence.

How it Works
============

Inside the addon, there are 2 executables, namely: convert.exe and
gifsicle.exe. When the render button is clicked, blender will render a
PNG image sequence, then convert.exe (from imagemagick) will convert
the PNGs to GIF files. Finally, gifsicle.exe will merge all the GIF
files into a single animated GIF. This process occurs in reverse when
a GIF is imported.

If you're using linux, then you must install gifsicle and imagemagick
on your system for this addon to work. 

