import bpy
import os
import sys
import subprocess
import shutil
from .bligify_utils import remove_bads, update_progress
from bpy_extras.io_utils import ImportHelper


class ImportGIF(bpy.types.Operator, ImportHelper):
    bl_idname = "sequencerextra.import_gif"
    bl_label = "GIF Import"
    bl_description = "Import animated GIF as an image sequence"

    filter_glob = bpy.props.StringProperty(
            default="*.gif",
            options={"HIDDEN"},
            maxlen=255,
            )

    def execute(self, context):
        scene = context.scene
        path = self.filepath.replace("\\", "/")
        split = path.split("/")
        name = split.pop()
        name = remove_bads(os.path.splitext(name)[0])
        split.append(name + "_frames")
        temp = '/'.join(split)

        try:
            os.mkdir(temp)
        except FileExistsError:
            shutil.rmtree(temp)
            os.mkdir(temp)

        if sys.platform == "win32":
            gifsicle_path = os.path.join(os.path.dirname(__file__),
                                        "gifsicle.exe")
            gifsicle = '"' + gifsicle_path + '"'

        else:
            gifsicle = "gifsicle"
        command = " ".join([
            gifsicle, "--info", '"' + path + '"', ">",
            '"' + temp + '/info.txt"'
            ])

        subprocess.call(command, shell=True)

        info = open(temp + "/info.txt")
        lines = info.readlines()
        info.close()
        os.remove(temp + "/info.txt")

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

        command = " ".join([
            gifsicle, "--explode", '"' + path + '"',
            '--output', '"' + temp + '/"'
            ])

        print("Separating animated GIF into frames...")
        subprocess.call(command, shell=True)

        if sys.platform == 'win32':
            converter_path = os.path.join(os.path.dirname(__file__),
                                          'convert.exe')
            converter = '"' + converter_path + '"'
        else:
            converter = "convert"

        images = list(sorted(os.listdir(temp)))

        wm = context.window_manager
        wm.progress_begin(0, 100.0)
        total = len(images)
        for i in range(total):
            update_progress("Converting GIF frames to PNG", i/total)
            wm.progress_update((i/total) * 100)
            if i > 0:
                command = " ".join([
                    converter,
                    '"' + temp + "/" + images[i-1][1::] + '.png"',
                    '"' + temp + "/" + images[i] + '"', "-layers",
                    "merge", '"' + temp + "/" + images[i][1::] + '.png"'
                    ])
            else:
                command = " ".join([
                    converter, '"' + temp + "/" + images[i] + '"',
                    '"' + temp + "/" + images[i][1::] + '.png"'
                    ])
            subprocess.call(command, shell=True)
        update_progress("Converting GIF frames to PNG", 1)

        images = os.listdir(temp)
        for i in range(len(images)):
            if not images[i].endswith(".png"):
                os.remove(temp + "/" + images[i])

        dict_list = []
        for image in list(sorted(os.listdir(temp))):
            dict_list.append({"name": image, "name": image})
        current_frame = scene.frame_current

        bpy.ops.sequencer.image_strip_add(
            directory=temp + "/",
            files=dict_list,
            frame_start=current_frame
            )

        wm.progress_end()
        print("----------Strip added to VSE----------")

        return {"FINISHED"}
