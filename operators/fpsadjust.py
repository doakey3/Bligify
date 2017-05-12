import bpy
import math

class FPSAdjust(bpy.types.Operator):

    bl_label = "FPS Adjust"
    bl_idname = "sequencerextra.fps_adjust"
    bl_description = "Applies speed to strips and adjusts scene FPS"

    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        target_fps = scene.fps_adjustment
        
        if fps == target_fps:
            scene.render.fps_base = 1
            return {"FINISHED"}

        strips = list(bpy.context.selected_editable_sequences)
        strips = list(sorted(strips, key=lambda x: x.frame_start))

        if len(strips) == 0:
            scene.render.fps = target_fps
            scene.render.fps_base = 1
            return {"FINISHED"}

        message = apply_speed_modifiers(scene, strips, target_fps)
        if not message == None:
            self.report(set({'ERROR'}), message)
            return {"FINISHED"}

        return {"FINISHED"}

def apply_speed_modifiers(scene, strips, target_fps):
    """
    Applies speed modifier to strips and 
    shortens them according to target fps
    """
    
    all_strips = list(sorted(scene.sequence_editor.sequences,
        key=lambda x: x.frame_start))
    
    for strip in strips:
        if not is_independent(all_strips, strip):
            return "FPS Adjust should only be done to independent strips\nEither prerender the timeline section or make a metastrip before applying FPS Adjust."
    
    fps = scene.render.fps / scene.render.fps_base
    speed_factor = fps / target_fps
    
    scene.render.fps = target_fps
    scene.render.fps_base = 1
    
    for strip in strips:

        speed_strip = scene.sequence_editor.sequences.new_effect(
            name="Bligify_" + strip.name,
            type="SPEED",
            channel=strip.channel + 1,
            frame_start=strip.frame_final_start,
            frame_end=strip.frame_final_end,
            seq1=strip
            )
        speed_strip.use_default_fade = False
        speed_strip.speed_factor = speed_factor

        duration = strip.frame_final_duration
        end = strip.frame_final_end
        
        new_duration = math.ceil(duration / speed_factor)
        new_end = strip.frame_final_start + new_duration
        difference = end - new_end
        shift_difference = difference + (end % 1)
        
        strip.frame_final_end = new_end
        
        shift_afters(all_strips, end, shift_difference)
    
    scene.frame_start = strips[0].frame_start
    scene.frame_end = strips[-1].frame_final_end - 1

def is_independent(all_strips, strip):
    """
    Check if a strip has neighbors sharing the same timeline space
    
    Speed modifiers should only be added to independent strips
    """
    
    for potential_relative in all_strips:
        if not potential_relative == strip:
            start = strip.frame_start
            end = strip.frame_final_end
            p_start = potential_relative.frame_start
            p_end = potential_relative.frame_final_end
            
            if p_start >= start and p_start < end:
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
        
