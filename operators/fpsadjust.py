import bpy
import math
from .utilities.get_open_channel import get_open_channel

class FPSAdjust(bpy.types.Operator):

    bl_label = "FPS Adjust"
    bl_idname = "sequencerextra.fps_adjust"
    bl_description = "Applies speed to strips and adjusts scene FPS"

    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        target_fps = scene.fps_adjustment
        speed_factor = fps / target_fps
        
        if fps == target_fps:
            return {"FINISHED"}

        strips = list(bpy.context.selected_editable_sequences)
        strips = list(sorted(strips, key=lambda x: x.frame_start))

        i = 0
        while i < len(strips):
            if strips[i].type == 'SOUND':
                strips.pop(i)
            else:
                i += 1

        if len(strips) == 0:
            return {"FINISHED"}
            
        all_strips = list(sorted(scene.sequence_editor.sequences,
        key=lambda x: x.frame_start))
    
        for unchecked_strip in strips:
            if not is_independent(all_strips, unchecked_strip):
                message = "FPS Adjust should only be done to independent strips\n(No strips stacked on other strips)\n\nEither prerender the timeline section or make a metastrip before applying FPS Adjust."
                self.report(set({'ERROR'}), message)
                return {"FINISHED"}
        
        set_scene_fps(scene, target_fps)

        apply_speed_modifiers(scene, strips, fps, speed_factor)  

        return {"FINISHED"}

def set_scene_fps(scene, target_fps):
    """Sets the scene fps"""
    
    if target_fps <= 120:
        scene.render.fps = target_fps
        scene.render.fps_base = 1
    
    else:
        scene.render.fps = 100
        scene.render.fps_base = 100 / target_fps

def apply_speed_modifiers(scene, strips, fps, speed_factor):
    """
    Applies speed modifier to strips and 
    shortens them according to target fps
    """
    
    all_strips = list(sorted(scene.sequence_editor.sequences,
        key=lambda x: x.frame_start))
    
    speed_channel = get_open_channel(scene)
    
    for strip in strips:

        speed_strip = scene.sequence_editor.sequences.new_effect(
            name="Bligify_" + strip.name,
            type="SPEED",
            channel=speed_channel,
            frame_start=strip.frame_final_start,
            frame_end=strip.frame_final_end,
            seq1=strip
            )
        speed_strip.use_default_fade = False
        speed_strip.speed_factor = speed_factor

        duration = strip.frame_final_duration
        new_duration = math.ceil(duration / speed_factor)        
        strip.frame_final_end = strip.frame_final_start + new_duration
        shift_difference = duration - strip.frame_final_duration
        
        shift_afters(all_strips, strip.frame_final_end, shift_difference)
    
    scene.frame_start = strips[0].frame_final_start
    scene.frame_end = strips[-1].frame_final_end - 1

def is_independent(all_strips, strip):
    """
    Check if a strip has neighbors sharing the same timeline space
    
    Speed modifiers should only be added to independent strips
    """
    if strip.type == 'SOUND':
        return True
    
    start = strip.frame_final_start
    end = strip.frame_final_end
    
    for potential_relative in all_strips:
        if not potential_relative.type == 'SOUND':
            if not potential_relative == strip:
                
                p_start = potential_relative.frame_final_start
                p_end = potential_relative.frame_final_end

                if p_start >= start and p_start < end:
                    print(p_start, start, p_end, end)
                    return False
                elif p_end > start and p_end <= end:
                    return False
                elif p_start == start and p_end == end:
                    return False
    return True

def shift_afters(all_strips, frame, shift_count):
    """
    Shifts all strips after frame to the left by shift_count frames
    """
    
    for strip in all_strips:
        if strip.frame_final_start >= frame:
            try:
                strip.input_1
            except AttributeError:
                strip.frame_start -= shift_count
        
