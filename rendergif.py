import bpy
import os
import sys
import subprocess

if sys.platform == "win32":
    sys.path.append(os.path.dirname(__file__))
from PIL import Image
from io import BytesIO
from bpy_extras.io_utils import ExportHelper
from .bligify_utils import remove_bads, update_progress

class PNGs2GIFs(bpy.types.Operator):
    """Convert all PNG files in a directory to GIFs"""

    bl_label = "PNGs 2 GIFs"
    bl_idname = "sequencerextra.pngs2gifs"
    bl_description = "Convert PNGs to GIFs"

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bligify_frames == "":
            return False
        else:
            return True

    def execute(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.bligify_frames)
        frames = os.listdir(path)
        wm = context.window_manager
        wm.progress_begin(0, 100.0)
        for i in range(len(frames)):
            img = Image.open(os.path.join(path, frames[i]))
            buffer = BytesIO()
            img.save(buffer, quality=100, format="gif")
            name = os.path.splitext(frames[i])[0] + '.gif'
            open(os.path.join(path, name), 'wb').write(buffer.getvalue())
            img.close()
            os.remove(os.path.join(path, frames[i]))
            wm.progress_update((i / len(frames)) * 100)
            update_progress("Converting PNGs to GIFs", i / len(frames))
        update_progress("Converting PNGs to GIFs", 1)
        
        return {"FINISHED"}

class RenderGIF(bpy.types.Operator, ExportHelper):
    bl_label = "Render GIF"
    bl_idname = "sequencerextra.render_gif"
    bl_description = "Render an animated GIF"

    filename_ext = ".gif"

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bligify_frames == "":
            return False
        else:
            return True

    def execute(self, context):

        scene = context.scene

        if sys.platform == "linux":
            try:
                devnull = open(os.devnull)
                subprocess.call(["gifsicle"], stdout=devnull,
                                stderr=devnull)
            except FileNotFoundError:
                print("Gifsicle must be installed...")
                return {"FINISHED"}
        
        if sys.platform == "win32":
            gifsicle_path = os.path.join(os.path.dirname(__file__),
                                         "gifsicle.exe")
            gifsicle = '"' + gifsicle_path + '"'
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

        quality = scene.gif_quality
        if not quality == "Full":
            command.append("--colors")
            command.append(quality)
        else:
            pass

        path = bpy.path.abspath(scene.bligify_frames).replace('\\', '/')
        pics = '"' + path + '"/*.gif'
        out = '"' + self.filepath + '"'
        command.append(pics)
        command.append("--output")
        command.append(out)
        subprocess.call(" ".join(command), shell=True)
        return {"FINISHED"}
