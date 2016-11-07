#bligify

A Blender 3d addon for exporting and importing animated GIF sequences.

##Installation

<img src="http://i.imgur.com/p6ZJsG5.gif" width="640" height="480">

1. Download the repository. 
2. Open Blender. 
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded release
5. Check the box next to "Sequencer:bligify"
6. If using linux, you must install gifsicle and imagemagick.

##Usage

###FPS to 10
![FPS 10](http://i.imgur.com/Nfyh3xb.gif)

The scene fps is set to 10 and speed modifiers are added to selected videos so that playback speed and length match the scene frame rate.

###Render GIF

Set an output location. Click the Render button. Images will be rendered from blender, converted to GIF files, and combined into an animated gif.

###Import GIF

Click the import button and navigate to the gif file you would like to import. The gif will be split into individual .gifs, then each converted to PNG. Finally, these will be added to the sequence editor as an image sequence.
