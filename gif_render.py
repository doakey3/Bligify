#If you're running linux, you'll need to install gifsicle and imagemagick

bl_info = {
    "name": "GIF Render",
    "description": "Render sequence as animated GIF",
    "author": "doakey3",
    "version": (1, 0, 3),
    "blender": (2, 7, 8),
    "wiki_url": "",
    "tracker_url":"",
    "category": "Sequencer"}

import bpy
import os
import shutil
import subprocess
import sys
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper

class UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "GIF Tools"
    
    def draw(self, context):
        layout = self.layout
        
        b_row = layout.row()
        box = b_row.box()
        box.label('GIF Tools')
        box.prop_menu_enum(context.scene, 'gif_quality', 
            text='GIF Quality', icon='SCRIPTWIN')
        row = box.row()
        split=row.split(percentage=0.5)
        colL = split.column()
        colR = split.column()
        colL.operator("sequencerextra.fps_to_ten", 
            icon="RECOVER_LAST")
        colR.operator("sequencerextra.res320x240", 
            icon='RENDER_REGION')
        row = box.row()
        row.operator('sequencerextra.render_gif',
            icon="RENDER_ANIMATION")
        row2 = box.row()
        row.operator('sequencerextra.import_gif',
            icon="LIBRARY_DATA_DIRECT")
        
gif_quality_options = [
                ('Full','Full','All colors included (bigger filesize)'),
                ('256','256','Limit number of colors to 256'),
                ('128','128','Limit number of colors to 128'),
                ('64','64','Limit number of colors to 64'),
]

########################################################################

class ImportGIF(bpy.types.Operator, ImportHelper):
    bl_idname = "sequencerextra.import_gif"
    bl_label = "GIF Import"
    bl_description = ' '.join(['Import animated GIF as an image',
                'sequence\n** Requires Imagemagick and Gifsicle **'])

    filter_glob = StringProperty(
            default="*.gif",
            options={'HIDDEN'},
            maxlen=255,
            )

    def execute(self, context):
        scene = context.scene
        path = self.filepath.replace('\\','/')
        split = path.split('/')
        name = split.pop()
        name = os.path.splitext(name)[0]
        temp = '/'.join(split) + '/' + name + '_frames'
        
        try:
            os.mkdir(temp)
        except FileExistsError:
            shutil.rmtree(temp)
            os.mkdir(temp)
        
        if sys.platform == 'win32':
            gifsicle = '"' + os.path.join(
                os.path.dirname(__file__),'gifsicle.exe') + '"'
        else:
            gifsicle = 'gifsicle'
        command = ' '.join([gifsicle, '--info', '"' + path + '"', '>', 
                            '"' + temp + '/info.txt"'])
        subprocess.call(command, shell=True)
        
        info = open(temp + '/info.txt')
        lines = info.readlines()
        info.close()
        
        delay = -1
        x = -1
        y = -1
        for line in lines:
            if line.lstrip().startswith('+'):
                split = line.split(' ')
                for word in split:
                    if 'x' in word:
                        x = int(word.split('x')[0])
                        y = int(word.split('x')[1])
            elif 'delay' in line:
                delay = line.rstrip().split(' ')[-1]
                delay = delay[0:len(delay)-1]
                delay = float(delay)
                fps = 1/delay
            if not delay == -1 and not x == -1 and not y == -1:
                break
        scene.render.resolution_x = x
        scene.render.resolution_y = y
        scene.render.fps = fps
        scene.render.fps_base = 1
        
        os.remove(temp + '/info.txt')
        command = ' '.join([gifsicle,'--explode','"' + path + '"',
            '--output','"' + temp + '/"'])
        subprocess.call(command,shell=True)
        
        if sys.platform == 'win32':
            converter = '"' + os.path.join(os.path.dirname(__file__),
                'convert.exe') + '"'
        else:
            converter = 'convert'
        
        images = list(sorted(os.listdir(temp)))
        for i in range(len(images)):
            if i > 0:
                command = ' '.join([converter, temp + '/' + images[i-1][1::] + '.png', 
                    temp + '/' + images[i], '-layers','merge',
                    temp + '/' + images[i][1::] + '.png'])
            else:
                command = ' '.join([converter, temp + '/' + images[i], 
                    temp + '/' + images[i][1::] + '.png'])
            subprocess.call(command, shell=True)
        
        images = os.listdir(temp)
        for i in range(len(images)):
            if not images[i].endswith('.png'):
                os.remove(temp + '/' + images[i])
        
        dict_list = []
        for image in list(sorted(os.listdir(temp))):
            dict_list.append({"name":image,"name":image})
        current_frame = scene.frame_current
        
        bpy.ops.sequencer.image_strip_add(directory=temp+'/',
            files=dict_list,frame_start = current_frame)
        
        return {'FINISHED'}

########################################################################

class RenderGIF(bpy.types.Operator):
    bl_label = 'Render GIF'
    bl_idname = 'sequencerextra.render_gif'
    bl_description = ''.join(['Render an animated GIF\n',
        '** Requires Gifsicle & Imagemagick **'])
    
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
        
        framepath = scene.render.frame_path(scene.frame_current)
        framepath = framepath.replace('\\','/')
        links = framepath.split('/')
        links.pop()
        path = '/'.join(links) + '/'
        temp = path + 'temp_gif'
        
        relative_path = scene.render.filepath.replace('\\','/')
        if not relative_path.endswith('/'):
            name = relative_path.split('/')[-1]
            output_name = os.path.splitext(name)[0] + '.gif'
        else:
            output_name = 'animation.gif'

        try:
            os.mkdir(temp)
        except FileExistsError:
            shutil.rmtree(temp)
            os.mkdir(temp)

        temp += '/'

        scene.render.filepath = temp

        bpy.ops.render.render(animation=True)

        images = list(sorted(os.listdir(scene.render.filepath)))
        if sys.platform == 'win32':
            converter = '"' + os.path.join(os.path.dirname(__file__),
                'convert.exe') + '"'
        else:
            converter = 'convert'
        for i in range(len(images)):
            old = '"' + temp + images[i] + '"'
            old_path = temp + images[i]
            new_name = os.path.splitext(images[i])[0] + '.gif'
            new_gif = '"' + temp + new_name + '"'
            command = " ".join([converter,old,new_gif])
            subprocess.call(command, shell=True)
            os.remove(old_path)
            print(' '.join(['converted',images[i],'to .GIF']))

        print('Combining images into animation...')
        
        if sys.platform == 'win32':
            gifsicle = '"' + os.path.join(os.path.dirname(__file__),
                'gifsicle.exe') + '"'
        else:
            gifsicle = 'gifsicle'
        
        command = [gifsicle,'--careful', '--optimize=3', '--disposal' ,
            'background','--no-background','--loop','--no-warnings']
            
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
        
        pics = '"' + temp + '"' + '*.gif'
        out = '"' + path + output_name + '"'
        command.append(pics)
        command.append('--output')
        command.append(out)
        print(' '.join(command))
        subprocess.call(' '.join(command), shell=True)

        shutil.rmtree(temp)
        
        if output_name == 'animation.gif':
            scene.render.filepath = path
        else:
            scene.render.filepath = path + output_name
        
        print('Complete.')
        
        return {'FINISHED'}
        
def find_sequencer_area():
    screens = list(bpy.data.screens)
    for screen in screens:
        for area in screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                return screen, area

########################################################################

class FPSToTen(bpy.types.Operator):
    bl_label = 'FPS: 10'
    bl_idname = 'sequencerextra.fps_to_ten'
    bl_description = ''.join(['Adjusts the scene FPS to 10.\n',
                        'Applies speed effect to selected video clips'])
    
    def execute(self, context):
        scene = context.scene
        sequence = scene.sequence_editor
        fps = scene.render.fps/scene.render.fps_base
        target_fps = 10

        strips = selected_video_strips()
        
        if len(strips) == 0:
            scene.render.fps = target_fps
            scene.render.fps_base = 1
            return {'FINISHED'}  

        apply_speed_modifiers(strips, scene, sequence)
        adjust_speed_factors(scene, target_fps, sequence)
        adjust_strip_lengths(scene, target_fps, sequence)

        return {'FINISHED'}
        
def selected_video_strips():
    """Gets the selected video strips and returns them as sorted list"""
    sel = list(bpy.context.selected_editable_sequences)
    selected = []
    for clip in sel:
        if clip.type == 'MOVIE' or clip.type == 'SCENE':
            selected.append(clip)
    selected = list(sorted(selected,
        key=lambda x: x.frame_start))
    return selected
    
def apply_speed_modifiers(strips, scene, sequence):
    """Applies speed modifier to sequence strips"""
    for strip in strips:
        bpy.ops.sequencer.select_all(action='DESELECT')
        sequence.active_strip = strip

        screen, area = find_sequencer_area()
        window = bpy.context.window
        bpy.ops.sequencer.effect_strip_add(
            {'window':window,
            'scene':scene,
            'area':area,
            'screen':screen,
            'region':area.regions[0]},
            type="SPEED")

def adjust_speed_factors(scene, target_fps, sequence):
    """
    Adjusts the speed factor of each speed modifier to 
    current_fps/target_fps
    """
    fps = scene.render.fps/scene.render.fps_base
    for strip in sequence.sequences:
        if strip.type == 'SPEED':
            movie_strip = strip.input_1
            strip.use_default_fade = False
            speed_factor = fps/target_fps
            strip.speed_factor = speed_factor

def adjust_strip_lengths(scene, target_fps, sequence):
    """
    Change the scene fps to target_fps
    Divide the duration of each movie strip by its speed factor
    Set the scene end frame to the last frame of the last selected strip
    """
    movie_strips = []
    all_strips = list(sorted(sequence.sequences,
        key=lambda x: x.frame_start))
    channels = {}
    for strip in all_strips:
        channels[strip.name] = strip.channel
    
    scene.render.fps = target_fps
    scene.render.fps_base = 1
        
    for strip in all_strips:
        if strip.type == 'SPEED':
            movie_strip = strip.input_1
            movie_strips.append(movie_strip)
            speed_factor = round(strip.speed_factor, 4)
            ffd = movie_strip.frame_final_duration
            duration = (ffd + 1)/speed_factor
            end = movie_strip.frame_final_start + duration + 1
            original_end = movie_strip.frame_final_end
            difference = original_end - end
            movie_strip.frame_final_end = end
            
            for st in all_strips:
                if st.frame_final_start >= original_end:
                    if st.type == 'MOVIE' or st.type == 'SOUND' or st.type == 'SCENE':
                        st.frame_start -= difference + (end % 1)
            
    for strip in all_strips:
        strip.channel = channels[strip.name]

    movie_strips = list(sorted(movie_strips, 
        key=lambda x: x.frame_final_end))
    last_frame = movie_strips[-1].frame_final_end - 1
    scene.frame_end = last_frame
    
    bpy.ops.sequencer.select_all(action='DESELECT')
    sequence.active_strip = movie_strips[0]
            
########################################################################

class Res320x240(bpy.types.Operator):
    bl_label = '320x240'
    bl_idname = 'sequencerextra.res320x240'
    bl_description = 'Change resolution to 320 by 240 px'
    
    def execute(self, context):
        scene = context.scene
        scene.render.resolution_x = 320
        scene.render.resolution_y = 240
        return {'FINISHED'}

########################################################################
    
def register():
    bpy.utils.register_class(UI)
    bpy.utils.register_class(RenderGIF)
    bpy.utils.register_class(Res320x240)
    bpy.utils.register_class(FPSToTen)
    bpy.utils.register_class(ImportGIF)
    
    bpy.types.Scene.gif_quality = bpy.props.EnumProperty(
        items=gif_quality_options)
    
def unregister():
    bpy.utils.unregister_class(UI)
    bpy.utils.unregister_class(RenderGIF)
    bpy.utils.unregister_class(Res320x240)
    bpy.utils.unregister_class(FPSToTen)
    bpy.utils.unregister_class(ImportGIF)
    
    del bpy.types.Scene.gif_quality
    
if __name__ == "__main__":
    register()
