import bpy


class FPSAdjust(bpy.types.Operator):

    bl_label = "FPS Adjust"
    bl_idname = "sequencerextra.fps_adjust"
    bl_description = "Applies speed to strips and adjusts scene FPS"

    def execute(self, context):
        scene = context.scene
        sequence = scene.sequence_editor
        fps = scene.render.fps/scene.render.fps_base
        target_fps = scene.fps_adjustment

        strips = selected_video_strips()

        if len(strips) == 0:
            scene.render.fps = target_fps
            scene.render.fps_base = 1
            return {"FINISHED"}

        apply_speed_modifiers(strips, scene, target_fps, sequence)
        adjust_strip_lengths(scene, target_fps, sequence)

        return {"FINISHED"}


def selected_video_strips():
    """Gets the selected video strips and returns them as sorted list"""
    sel = list(bpy.context.selected_editable_sequences)
    selected = []
    movie_types = [
        "IMAGE", "META", "SCENE", "MOVIE",
        "MOVIECLIP", "MASK", "COLOR"
    ]

    for clip in sel:
        if clip.type in movie_types:
            selected.append(clip)
    selected = list(sorted(selected,
                           key=lambda x: x.frame_start))
    return selected


def apply_speed_modifiers(strips, scene, target_fps, sequence):
    """Applies speed modifier to sequence strips"""
    fps = scene.render.fps / scene.render.fps_base
    speed_factor = fps / target_fps

    for strip in strips:
        bpy.ops.sequencer.select_all(action="DESELECT")
        sequence.active_strip = strip

        screen, area = find_sequencer_area()
        window = bpy.context.window
        location = {
            "window": window,
            "scene": scene,
            "area": area,
            "screen": screen,
            "region": area.regions[0]
        }
        bpy.ops.sequencer.effect_strip_add(
            location,
            type="SPEED")
        name = sequence.active_strip.name
        name = "bligify_" + name

        speed = sequence.active_strip
        speed.name = name
        speed.use_default_fade = False
        speed.speed_factor = speed_factor


def adjust_strip_lengths(scene, target_fps, sequence):
    """Set strip length to match original prior to speed modifier"""

    bpy.ops.sequencer.select_all(action="DESELECT")

    scene.render.fps = target_fps
    scene.render.fps_base = 1

    moveables = movie_types = [
        "IMAGE", "META", "SCENE", "MOVIE",
        "MOVIECLIP", "MASK", "COLOR", "SOUND"
    ]

    children = []
    count = 0
    all_strips = list(sorted(sequence.sequences,
                             key=lambda x: x.frame_start))

    while count < len(all_strips):
        if all_strips[count].type == "SPEED":
            strip = all_strips[count]
            if strip.input_1 not in children:
                children.append(strip.input_1)
                count += 1
            else:
                for other in all_strips:
                    if (other.type == "SPEED" and not
                            other.name.startswith("bligify_")):
                        if (other.input_1 == strip.input_1 and not
                                other == strip):
                            ssf = strip.speed_factor
                            osf = other.speed_factor
                            strip.speed_factor = osf * ssf
                            other.select = True
                            bpy.ops.sequencer.delete()

        else:
            count += 1
        all_strips = list(sorted(sequence.sequences,
                                 key=lambda x: x.frame_start))

    movie_strips = []
    channels = {}
    for strip in all_strips:
        channels[strip.name] = strip.channel

    for strip in all_strips:
        if strip.type == "SPEED":
            movie_strip = strip.input_1
            movie_strips.append(movie_strip)
            speed_factor = round(strip.speed_factor, 4)
            ffd = movie_strip.frame_final_duration
            duration = (ffd + 1) / speed_factor
            end = movie_strip.frame_final_start + duration + 1
            original_end = movie_strip.frame_final_end
            difference = original_end - end
            movie_strip.frame_final_end = end

            for st in all_strips:
                if st.frame_final_start >= original_end:
                    if st.type in moveables:
                        st.frame_start -= difference + (end % 1)

    for strip in all_strips:
        strip.channel = channels[strip.name]

    movie_strips = list(sorted(movie_strips,
                               key=lambda x: x.frame_final_end))
    last_frame = movie_strips[-1].frame_final_end - 1
    scene.frame_end = last_frame

    sequence.active_strip = movie_strips[0]


def find_sequencer_area():
    screens = list(bpy.data.screens)
    for screen in screens:
        for area in screen.areas:
            if area.type == "SEQUENCE_EDITOR":
                return screen, area
