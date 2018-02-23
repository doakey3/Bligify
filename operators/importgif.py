import bpy
import os
import sys
import subprocess
import shutil
from .utilities.remove_bads import remove_bads
from .utilities.update_progress import update_progress
from bpy_extras.io_utils import ImportHelper


def adjust_scene_for_gif(context, abspath, frames_folder):
    """
    Get the frame rate and resolution of the animated gif
    and adjust scene fps and resolution accordingly.
    """

    scene = context.scene

    gif = ''.join(['"', abspath, '"'])
    info_path = os.path.join(frames_folder, 'info.txt')
    info = ''.join(['"', info_path, '"'])
    command = ' '.join(["gifsicle", '--info', gif, '>', info])
    subprocess.call(command, shell=True)

    info_file = open(info_path, 'r')
    lines = info_file.readlines()
    info_file.close()
    os.remove(info_path)

    fps = 10
    delay = -1
    x = -1
    y = -1
    for line in lines:
        if line.lstrip().startswith("+"):
            split = line.split(" ")
            for word in split:
                if "x" in word:
                    x = int(word.split("x")[0])
                    y = int(word.split("x")[1])
        elif "delay" in line:
            delay = line.rstrip().split(" ")[-1]
            delay = delay[0:len(delay)-1]
            delay = float(delay)
            fps = 1/delay
        if not delay == -1 and not x == -1 and not y == -1:
            break
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    scene.render.fps = fps
    scene.render.fps_base = 1


def animated_gif_2_gifs(context, abspath, frames_folder):
    """Separate the animated gif into frames"""
    scene = context.scene

    gif = ''.join(['"', abspath, '"'])
    frames = ''.join(['"', frames_folder, '/"'])
    command = ' '.join(['gifsicle', '--unoptimize', '--explode',
                        gif, '--output', frames])

    print("Separating animated GIF into frames...")
    subprocess.call(command, shell=True)


def gifs_2_pngs(context, frames_folder):
    """
    Convert gif frames to PNGs.
    Each frame must be combined with the previous frame
    """

    images = list(sorted(os.listdir(frames_folder)))

    wm = context.window_manager
    wm.progress_begin(0, 100.0)
    total = len(images)
    for i in range(total):
        update_progress("Converting GIF frames to PNG", i/total)
        wm.progress_update((i/total) * 100)

        curr_img = os.path.join(frames_folder, images[i])
        curr_img = ''.join(['"', curr_img, '"'])

        out_name = images[i][1::] + '.png'
        out_img = os.path.join(frames_folder, out_name)
        out_img = ''.join(['"', out_img, '"'])

        command = ' '.join(['convert', curr_img, out_img])

        subprocess.call(command, shell=True)

    update_progress("Converting GIF frames to PNG", 1)
    wm.progress_end()

    images = os.listdir(frames_folder)
    for i in range(len(images)):
        if not images[i].endswith(".png"):
            os.remove(os.path.join(frames_folder, images[i]))


class ImportGIF(bpy.types.Operator, ImportHelper):
    bl_idname = "bligify.import_gif"
    bl_label = "GIF Import"
    bl_description = "Import animated GIF as an image sequence"

    adjust_scene_for_gif_prop = bpy.props.BoolProperty(
        name="Adjust Scene For GIF", default=True)

    filter_glob = bpy.props.StringProperty(
        default="*.gif",
        options={"HIDDEN"},
        maxlen=255,
        )

    def execute(self, context):
        scene = context.scene

        abspath = os.path.abspath(self.filepath)
        folder_path = os.path.dirname(abspath)
        file_name = os.path.splitext(os.path.basename(abspath))[0]
        frames_folder = os.path.join(folder_path, file_name + "_frames/")

        try:
            os.mkdir(frames_folder)
        except FileExistsError:
            shutil.rmtree(frames_folder)
            os.mkdir(frames_folder)

        if self.adjust_scene_for_gif_prop:
            adjust_scene_for_gif(context, abspath, frames_folder)
        animated_gif_2_gifs(context, abspath, frames_folder)
        gifs_2_pngs(context, frames_folder)

        dict_list = []
        images = list(sorted(os.listdir(frames_folder)))
        for image in images:
            dict_list.append({"name": image, "name": image})
        current_frame = scene.frame_current

        bpy.ops.sequencer.image_strip_add(
            directory=frames_folder,
            files=dict_list,
            frame_start=current_frame
            )

        print(os.path.basename(abspath) + " added to VSE")
        return {"FINISHED"}
