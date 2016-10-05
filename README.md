#GIF_Render

A Blender 3d addon for exporting and importing animated GIF sequences.

A video tutorial is available [here](https://www.youtube.com/watch?v=xbroTg3UN7A)

##Installation

1. Download the [Release](https://github.com/doakey3/GIF_Render/releases). 
2. Open Blender. 
3. Go to File > User Preferences > Addons > Sequencer
4. Click "Install From File" and navigate to the downloaded release
5. Check the box next to "Sequencer:GIF Render"
6. If using linux, you must install gifsicle and imagemagick.
  - UBUNTU: open a terminal and type:
    sudo apt-get install gifsicle imagemagick

##About

Render Function:
This addon tells blender to render the animation as PNG files. Imagemagick is used to convert the PNG files to GIF files. Gifsicle is used to combine the GIF files into a single animated GIF. 

Import Function:
Gifsicle splits the animated GIF into separate GIF files. Imagemagick is used to convert the GIF files into PNG. Blender imports the image sequence into the sequencer.
