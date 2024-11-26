import bpy
import os
import sys
from .operators import *

bl_info = {
    "name": "Bligify",
    "description": "export/import animated GIF from VSE.",
    "author": "doakey3",
    "version": (1, 3, 9),
    "blender": (2, 80, 0),
    "warning": "Requires imagemagick & gifsicle",
    "wiki_url": "https://github.com/doakey3/bligify",
    "tracker_url": "https://github.com/doakey3/bligify/issues",
    "category": "Sequencer"}


class PREFERENCES_PT_exe_paths(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene, "gifsicle_path")
        layout.prop(scene, "magick_path")


class SEQUENCER_PT_bligify(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Bligify"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Tools"

    @classmethod
    def poll(cls, context):
        return context.space_data.view_type == "SEQUENCER" or context.space_data.view_type == "SEQUENCER_PREVIEW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        box = layout.box()
        row = box.row()
        row.prop(scene, "gif_disposal", text="Disposal", icon="FAKE_USER_OFF")
        row = box.row()
        row.prop(scene, "gif_dither", text="Dither", icon="STRANDS")
        row = box.row()
        row.prop(scene, "gif_color_method", text="Filter", icon="FILTER")
        row = box.row()
        row.prop(scene, "gif_color_map", text="Map", icon="NODE_TEXTURE")
        special_row = box.row()
        special_row.prop(scene, "gif_mapfile", text="Map File")
        if scene.gif_color_map == "custom":
            special_row.enabled = True
        else:
            special_row.enabled = False
        row = box.row()
        row.prop(scene, "gif_lossy", text="Lossy")
        row.prop(scene, "gif_optimize", text="Optimize")
        row = box.row()
        row.prop(scene, "gif_colors", text="Colors")
        row.prop(scene, "gif_loop_count", text="Loop")
        row = layout.row()
        row.prop(scene, "gif_careful", text="Careful")
        row.prop(scene, "gif_dither_conversion", text="Dither Conversion")
        row = layout.row()
        row.prop(scene, "delete_frames", text="Cleanup on Completion")
        row = layout.row()
        row.operator("bligify.fps_adjust",
                     icon="MOD_TIME")
        row.prop(scene, "fps_adjustment", text="")
        row = layout.row()
        row.operator("bligify.render_gif",
                     icon="RENDER_ANIMATION")
        row.operator("bligify.import_gif",
                     icon="FILE_FOLDER")


def make_absolute_gifsicle_path(context):
    """Convert relative gifsicle path to absolute"""
    prop = context.scene.gifsicle_path
    prop = bpy.path.abspath(prop)


def make_absolute_magick_path(context):
    """Convert relative magick path to absolute"""
    prop = context.scene.magick_path
    prop = bpy.path.abspath(prop)


def initprop():
    default_gifsicle_path = ""
    default_magick_path = ""

    # OS X
    if sys.platform == "darwin":
        default_gifsicle_path = "/usr/local/bin/gifsicle"
        default_magick_path = "/usr/local/bin/magick"
    # Windows
    elif sys.platform == "win32":
        default_gifsicle_path = os.path.join(
            os.path.dirname(__file__),
            'executables',
            'gifsicle.exe'
        )
        default_magick_path = os.path.join(
            os.path.dirname(__file__),
            'executables',
            'convert.exe'
        )

    bpy.types.Scene.gifsicle_path = bpy.props.StringProperty(
        name="Gifsicle Path",
        description="Define path to the executable for gifsicle. If empty, Bligify will use the system installation of gifsicle.",
        subtype="FILE_PATH",
        default=default_gifsicle_path,
        update=lambda self, context: make_absolute_gifsicle_path(context),
        )

    bpy.types.Scene.magick_path = bpy.props.StringProperty(
        name="Magick Path",
        description="Define path to the executable for Magick. If empty, Bligify will use the system installation of ImageMagick.",
        subtype="FILE_PATH",
        default=default_magick_path,
        update=lambda self, context: make_absolute_magick_path(context),
        )

    disposal_options = [
        ("none", "None", "Leave frame visible for future frames to build upon"),
        ("background", "Background", "Replace the frame with the background"),
        ("previous", "Previous", "Replace frame with the area from the previous displayed frame"),
        ]

    bpy.types.Scene.gif_disposal = bpy.props.EnumProperty(
        name="Disposal Method",
        items=disposal_options,
        description="Set the disposal method",
        default="background"
        )

    dither_methods = [
        ("none", "None", "Dithering makes bigger files that are usually better appearing,\nbut can cause animation artifacts, so it is off by default"),
        ("floyd-steinberg", "Floyd-Steinberg", "Use Floyd-Steinberg diffusion, usually best, but may cause artifacts"),
        ("ro64", "ro64", "Use large, random looking pattern that generally produces good results"),
        ("o3", "o3", "Use smaller, regular pattern"),
        ("o4", "o4", "Use smaller, regular pattern"),
        ("o8", "o8", "Use smaller, regular pattern"),
        ("ordered", "Ordered", "A good ordered dithering algorithm"),
        ("halftone", "Halftone", "For special effects"),
        ("squarehalftone", "Square Halftone", "For special effects"),
        ("diagnoal", "Diagnoal", "For special effects")
        ]

    bpy.types.Scene.gif_dither = bpy.props.EnumProperty(
        name="Dither Method",
        items=dither_methods,
        description="Set the dithering method",
        default="none"
        )

    color_methods = [
        ("diversity", "Diversity", "Use a strict subset of existing colors.\nGenerally produces good results"),
        ("blend-diversity", "Blend Diversity", "Some color values are blended from groups of existing colors."),
        ("median-cut", "Median Cut", "The median cut algorithm as described by Heckbert"),
    ]

    bpy.types.Scene.gif_color_method = bpy.props.EnumProperty(
        name="Color Reduction Method",
        items=color_methods,
        description="Determine how a smaller colormap is chosen",
        default="diversity"
        )

    color_maps = [
        ("none", "None", "Don't use a color map"),
        ("web", "Web", 'Use the 216-color "Web-safe palette"'),
        ("gray", "Grayscale", "Use grayscale color map"),
        ("bw", "Black & White", "Use Black and White color map"),
        ("custom", "Custom", "Use a custom color map")
    ]

    bpy.types.Scene.gif_color_map = bpy.props.EnumProperty(
        name="Color Map",
        items=color_maps,
        description="Use a color map so that each pixel in the image is\nchanged to the closest match in colormap.\n\n(See Gifsicle's Manual Page for more info)",
        default="none",
        )

    bpy.types.Scene.gif_mapfile = bpy.props.StringProperty(
        name="Map File",
        description="Path to the custom color map",
        subtype="FILE_PATH",
        )

    bpy.types.Scene.gif_careful = bpy.props.BoolProperty(
        name="Careful",
        description="Create a slightly larger GIF, but avoid bugs with some Java and Internet Explorer versions",
        default=True
        )

    bpy.types.Scene.gif_optimize = bpy.props.IntProperty(
        name="Optimization Method",
        description="Optimization Method\n\n1 store only changed portion of each image (fast)\n2 use transparency to shrink the file further\n3 try several methods (slower, but smaller file)",
        default=3,
        max=3,
        min=1,
        )

    bpy.types.Scene.gif_colors = bpy.props.IntProperty(
        name="GIF Colors",
        description="Number of colors used in the GIF",
        default=256,
        max=256,
        min=2,
        )
    
    bpy.types.Scene.gif_lossy = bpy.props.IntProperty(
        name="GIF Colors",
        description="Optimisation using Lossy GIF encoder",
        default=0,
        max=200,
        min=0,
        )

    bpy.types.Scene.gif_loop_count = bpy.props.IntProperty(
        name="Loop Count",
        description="Loop x number of times; 0 = loop forever",
        default=0,
        min=0
        )

    bpy.types.Scene.fps_adjustment = bpy.props.IntProperty(
        name="FPS Adjustment",
        description="Set the new FPS that will be used after running FPS Adjust",
        default=10,
        max=1000,
        min=1
        )

    bpy.types.Scene.gif_dither_conversion = bpy.props.BoolProperty(
        description="Add dither to PNGs as they are converted to GIFs\n\nMay or may not make your animated GIF look better.",
        default=False
    )

    bpy.types.Scene.delete_frames = bpy.props.BoolProperty(
        description="Delete the PNG frames folder after GIF is complete",
        default=True
    )


classes = [
    PREFERENCES_PT_exe_paths,
    SEQUENCER_PT_bligify,
    SEQUENCER_OT_fps_adjust,
    SEQUENCER_OT_import_gif,
    SEQUENCER_OT_render_gif
]

def register():
    initprop()
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
