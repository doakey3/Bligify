import bpy
import os
import sys
import shutil
import subprocess
from bpy_extras.io_utils import ExportHelper
from .utilities.remove_bads import remove_bads
from .utilities.update_progress import update_progress
from .utilities.is_gifsicle_installed import is_gifsicle_installed
from .utilities.is_magick_installed import is_magick_installed


def pngs_2_gifs(context, frames_folder):
    """Convert the PNGs to gif images and report progress"""

    images = list(sorted(os.listdir(frames_folder)))

    total = len(images)
    wm = context.window_manager
    wm.progress_begin(0, 100.0)

    for i in range(total):
        update_progress("Converting PNG to GIF frames", i / total)
        wm.progress_update((i / total) * 100)
        png = os.path.join(frames_folder, images[i])
        gif = os.path.splitext(png)[0] + ".gif"
        command = ['magick']
        if context.scene.gif_dither_conversion:
            command.append("+dither")

        command.append(png)
        command.append(gif)

        subprocess.call(command)

    update_progress("Converting PNG to GIF frames", 1)


def gifs_2_animated_gif(context, abspath, frames_folder):
    """Combines gifs into animated gif"""

    scene = context.scene

    command = ["gifsicle", "--no-background", "--disposal"]

    command.append(scene.gif_disposal)

    if not scene.gif_dither == "none":
        command.append('--dither=' + scene.gif_dither)

    command.append('--color-method=' + scene.gif_color_method)

    if not scene.gif_color_map == "none":

        if not scene.gif_color_map == "custom":
            command.append("--use-colormap=" + scene.gif_color_map)
        elif not scene.gif_mapfile == '':
            map_path = ''.join(['"', bpy.path.abspath(scene.gif_mapfile), '"'])
            command.append("--use-colormap=" + map_path)

    if scene.gif_careful:
        command.append('--careful')

    command.append('--optimize=' + str(scene.gif_optimize))

    if scene.gif_loop_count == 0:
        command.append("--loop")
    elif scene.gif_loop_count == 1:
        command.append("--no-loopcount")
    else:
        command.append("--loopcount=" + str(scene.gif_loop_count - 1))

    fps = scene.render.fps / scene.render.fps_base
    delay = str(int(100 / fps))
    command.append("--delay")
    command.append(delay)

    command.append("--colors=" + str(scene.gif_colors))

    gifs = ''.join(['"', frames_folder, '/"*.gif'])
    animated_gif = ''.join(['"', abspath, '"'])

    command.append(gifs)
    command.append("--output")
    command.append(animated_gif)

    print("Combining GIF frames into animated GIF...")
    subprocess.call(" ".join(command), shell=True)

    context.window_manager.progress_end()


class RenderGIF(bpy.types.Operator, ExportHelper):
    bl_label = "Render GIF"
    bl_idname = "bligify.render_gif"
    bl_description = "Render an animated GIF."

    filename_ext = ".gif"

    blank_first_frame = bpy.props.BoolProperty(
        description="When true, the first frame of the GIF will be replaced by empty space",
        default=False
    )

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene and scene.sequence_editor:
            return True
        else:
            return False

    def make_gif(self, context):
        scene = context.scene
        frames_folder = scene.render.filepath
        abspath = os.path.abspath(self.filepath)

        pngs_2_gifs(context, frames_folder)
        gifs_2_animated_gif(context, abspath, frames_folder)
        scene.render.filepath = self.original_filepath

        if scene.delete_frames:
            shutil.rmtree(frames_folder)

    def execute(self, context):
        gifsicle_installed = is_gifsicle_installed()
        if not gifsicle_installed:
            self.report({'ERROR'}, "Gifsicle must be installed for this to work.")
            return {"FINISHED"}

        magick_installed = is_magick_installed()
        if not magick_installed:
            self.report({'ERROR'}, "Imagemagick must be installed for this to work.")
            return {"FINISHED"}

        scene = context.scene
        self.original_filepath = scene.render.filepath

        scene.render.image_settings.file_format = "PNG"

        abspath = os.path.abspath(self.filepath)
        folder_path = os.path.dirname(abspath)
        file_name = os.path.splitext(os.path.basename(abspath))[0]
        frames_folder = os.path.join(folder_path, file_name + "_frames")
        while os.path.isdir(frames_folder):
            frames_folder += "_frames"

        frames_folder += '/'

        os.mkdir(frames_folder)

        wm = context.window_manager
        wm.modal_handler_add(self)
        self.timer = wm.event_timer_add(0.5, context.window)

        scene.render.filepath = frames_folder
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        scene = context.scene
        frames_folder = scene.render.filepath

        if event.type == 'TIMER':
            try:
                frame_count = scene.frame_end - scene.frame_start + 1
                if len(os.listdir(frames_folder)) == frame_count:

                    self.make_gif(context)
                    context.area.type = "SEQUENCE_EDITOR"
                    return {"FINISHED"}

                else:
                    return {"PASS_THROUGH"}
            except FileNotFoundError:
                return {"FINISHED"}

        else:
            return {"PASS_THROUGH"}
