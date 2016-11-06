import bpy

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

def find_sequencer_area():
    screens = list(bpy.data.screens)
    for screen in screens:
        for area in screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                return screen, area
