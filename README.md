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

##Usage

###FPS to 10
![FPS 10](http://i.imgur.com/Nfyh3xb.gif)

The scene fps is set to 10 and speed modifiers are added to selected videos so that playback speed and length match the scene frame rate.

###Render GIF

Set an output location. Click the Render button. Images will be rendered from blender, converted to GIF files, and combined into an animated gif.

###Import GIF

Click the import button and navigate to the gif file you would like to import. The gif will be split into individual .gifs, then each converted to PNG. Finally, these will be added to the sequence editor as an image sequence.
