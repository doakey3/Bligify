#bligify

A Blender 3d addon for exporting and importing animated GIF sequences.
The user interface is found on the right side of the video sequence editor.

![UI](http://i.imgur.com/V5SOzNe.png)

##Installation

1. Download the repository. 
2. Open Blender. 
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded release
5. Check the box next to "Sequencer:bligify"
6. If using linux, you must install gifsicle and imagemagick.

##Usage

###GIF Quality

![Bunny Full](http://i.imgur.com/O6DxDxo.gif) ![Bunny 64](http://i.imgur.com/LpOAB1U.gif)

You can limit the colors in the animated gif. Fewer colors means smaller file size.
Above is a side by side comparison of the full version vs the 64 colors version.
The full is 1.2mb, the 64 color version is 470kb.

###Loop

You can set whether or not the output GIF will be looped.

###FPS Adjustment

Sets the scene fps to the new value.
This function will also add speed modifiers so that the clips
play at the same speed. To use this, first select all the strips that
will be part of the animated GIF and click the FPS Adjust button. 

###Render GIF

Click the render GIF button, name the output file, and click ok.

###Import GIF

Click the import button, navigate to the gif file, and click ok.
The GIF will be converted to a sequence of PNG files and imported
to the sequencer.

##Video Tutorial

![tutorial(http://i.imgur.com/Smu4ldw.png)](http://i.imgur.com/Smu4ldw.png)
