import bpy
import os
import ntpath
import sys
import shutil
import subprocess
from bpy_extras.io_utils import ExportHelper
from .bligify_utils import remove_bads, update_progress

def render_frames(context):
    """Render frame by frame and report progress"""
    scene = context.scene
    
    wm = context.window_manager
    wm.progress_begin(0, 100.0)
    
    start = scene.frame_start
    end = scene.frame_end
    
    for i in range(start, end + 1):
        if sys.platform == "win32":
            os.system("cls")
        elif sys.platform == "linux":
            subprocess.call("clear", shell=True)
            
        progress = (i - start) / (end - start)
        update_progress("Rendering Frames as PNG", progress)
        wm.progress_update((progress * 50))
        
        scene.frame_start = i
        scene.frame_end = i
        
        bpy.ops.render.render(animation=True)
    
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "linux":
        subprocess.call("clear", shell=True)
    
    update_progress("Rendering Frames as PNG", 1)
    wm.progress_end()
    
    scene.frame_start = start
    scene.frame_end = end

def pngs_2_gifs(context, frames_folder):
    """Convert the PNGs to gif images and report progress"""
    
    images = list(sorted(os.listdir(frames_folder)))
    
    total = len(images)
    wm = context.window_manager
    wm.progress_begin(0, 100.0)
    
    if sys.platform == "win32":
        addon_folder = os.path.dirname(__file__)
        converter = os.path.join(addon_folder, "convert.exe")
    else:
        converter = "convert"
    
    for i in range(total):
        update_progress("Converting PNG to GIF frames", i / total)
        wm.progress_update(((i / total) * 50) + 50)
        png = os.path.join(frames_folder, images[i])
        gif = os.path.splitext(png)[0] + ".gif"
        subprocess.call([converter, '+dither', png, gif])
        os.remove(png)
    update_progress("Converting PNG to GIF frames", 1)

def gifs_2_animated_gif(context, abspath, frames_folder):
    """Combines gifs into animated gif"""
    
    scene = context.scene
    
    if sys.platform == "win32":
        addon_folder = os.path.dirname(__file__)
        gifsicle_path = os.path.join(addon_folder, "gifsicle.exe")
        gifsicle = ''.join(['"', gifsicle_path, '"'])
    else:
        gifsicle = 'gifsicle'

    command = [
        gifsicle, "--careful", "--optimize=3", "--disposal",
        "background", "--no-background", "--no-warnings"
        ]
        
    if scene.gif_looped:
        command.append("--loop")
    
    fps = scene.render.fps / scene.render.fps_base
    delay = str(int(100 / fps))
    command.append("--delay")
    command.append(delay)
    
    colors = str(scene.gif_colors)
    if not colors == "256":
        command.append("--colors")
        command.append(colors)
    
    gifs = ''.join(['"', frames_folder, '/"*.gif'])
    animated_gif = ''.join(['"', abspath, '"'])
    
    command.append(gifs)
    command.append("--output")
    command.append(animated_gif)
    
    print("Combining GIF frames into animated GIF...")
    subprocess.call(" ".join(command), shell=True)

class RenderGIF(bpy.types.Operator, ExportHelper):
    bl_label = "Render GIF"
    bl_idname = "sequencerextra.render_gif"
    bl_description = "Render an animated GIF"

    filename_ext = ".gif"

    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            return scn.sequence_editor.sequences
        else:
            return False

    def execute(self, context):
        scene = context.scene
        original_filepath = scene.render.filepath
        
        scene.render.image_settings.file_format = "PNG"
        
        abspath = os.path.abspath(self.filepath)
        folder_path = os.path.dirname(abspath)
        file_name = os.path.splitext(ntpath.basename(abspath))[0]
        frames_folder = os.path.join(folder_path, file_name + "_frames/")
        
        scene.render.filepath = frames_folder

        try:
            os.mkdir(frames_folder)
        except FileExistsError:
            shutil.rmtree(frames_folder)
            os.mkdir(frames_folder)
        
        scene.render.filepath = frames_folder
        
        render_frames(context)
        pngs_2_gifs(context, frames_folder)
        gifs_2_animated_gif(context, abspath, frames_folder)
        
        shutil.rmtree(frames_folder)

        scene.render.filepath = original_filepath

        print("----------Complete----------")
        return {"FINISHED"}
