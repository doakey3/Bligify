import bpy
import os
import sys
import shutil
import subprocess
from bpy_extras.io_utils import ExportHelper
from .bligify_utils import remove_bads, update_progress

class RenderGIF(bpy.types.Operator, ExportHelper):
    bl_label = 'Render GIF'
    bl_idname = 'sequencerextra.render_gif'
    bl_description = ''.join(['Render an animated GIF\n',
        '** Requires Gifsicle & Imagemagick **'])
    
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
        scene.render.image_settings.file_format = "PNG"
        user_filepath = scene.render.filepath

        if not sys.platform == 'win32':
            try:
                devnull = open(os.devnull)
                subprocess.call(['convert'],stdout=devnull, 
                    stderr=devnull)
                subprocess.call(['gifsicle'],stdout=devnull,
                    stderr=devnull)
            except FileNotFoundError:
                print('Gifsicle and Imagemagick must be installed...')
                return {'FINISHED'} 

        path = self.filepath.replace('\\','/')
        split = path.split('/')
        output_name = split.pop()
        path = '/'.join(split) + '/'
        name = os.path.splitext(output_name)[0]
            
        temp = path + name + '_frames/'

        try:
            os.mkdir(temp)
        except FileExistsError:
            shutil.rmtree(temp)
            os.mkdir(temp)

        wm = context.window_manager
        wm.progress_begin(0, 100.0)
        
        scene.render.filepath = temp
        start = scene.frame_start
        end = scene.frame_end
        for i in range(start, end):
            if sys.platform == 'win32':
                os.system('cls')
            elif sys.platform == 'linux':
                subprocess.call('clear',shell=True)
            progress = (i - start) / (end - start)
            update_progress("Rendering Frames as PNG",progress)
            wm.progress_update((progress * 50))
            scene.frame_start = i
            scene.frame_end = i
            bpy.ops.render.render(animation=True)
        if sys.platform == 'win32':
                os.system('cls')
        elif sys.platform == 'linux':
            subprocess.call('clear',shell=True)
        update_progress("Rendering Frames as PNG",1)
        scene.frame_start = start
        scene.frame_end = end

        images = list(sorted(os.listdir(scene.render.filepath)))
        if sys.platform == 'win32':
            converter = os.path.join(os.path.dirname(__file__),
                'convert.exe')
        else:
            converter = 'convert'
        
        total = len(images)
        for i in range(total):
            update_progress("Converting PNG to GIF frames",i/total)
            wm.progress_update(((i / total) * 50) + 50)
            old = os.path.join(temp,images[i])
            new_name = os.path.splitext(images[i])[0] + '.gif'
            new_gif = os.path.join(temp,new_name)
            command = [converter,old,new_gif]
            subprocess.call([converter,old,new_gif])
            os.remove(old)
        update_progress("Converting PNG to GIF frames",1)
        
        if sys.platform == 'win32':
            gifsicle = '"' + os.path.join(os.path.dirname(__file__),
                'gifsicle.exe') + '"'
        else:
            gifsicle = 'gifsicle'
        
        command = [gifsicle,'--careful', '--optimize=3', '--disposal' ,
            'background','--no-background','--no-warnings']
        
        if scene.gif_looped:
            command.append('--loop')
            
        fps = scene.render.fps/scene.render.fps_base
        delay = str(int(100/fps))
        command.append('--delay')
        command.append(delay)

        quality = scene.gif_quality
        if not quality == 'Full':
            command.append('--colors')
            command.append(quality)
        else:
            pass
        
        pics = '"' + temp + '"*.gif'
        out = '"' + path + output_name + '"'
        command.append(pics)
        command.append('--output')
        command.append(out)
        print("Combining GIF frames into animated GIF...")
        subprocess.call(' '.join(command),shell=True)
        wm.progress_end()
        
        shutil.rmtree(temp)
        
        #reset the user's render filepath to what is was before
        scene.render.filepath = user_filepath

        print("----------Complete----------")
        return {'FINISHED'}
