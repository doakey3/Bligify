import bpy
from .operators.fpsadjust import FPSAdjust
from .operators.importgif import ImportGIF
from .operators.rendergif import RenderGIF
from .operators.export_odp import ExportODP

bl_info = {
    "name": "Bligify",
    "description": "export/import animated GIF from VSE. Currently runs on Windows and Linux only.",
    "author": "doakey3",
    "version": (1, 3, 4),
    "blender": (2, 7, 8),
    "warning": "Requires imagemagick & gifsicle install on linux",
    "wiki_url": "https://github.com/doakey3/bligify",
    "tracker_url": "https://github.com/doakey3/bligify/issues",
    "category": "Sequencer"}

class gif_UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Bligify"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.prop(scene, "gif_disposal", text="Disposal", icon="GHOST")
        row = box.row()
        row.prop(scene, "gif_dither", text="Dither", icon="GROUP_VERTEX")
        row = box.row()
        row.prop(scene, "gif_color_method", text="Filter", icon="FILTER")
        row = box.row()
        row.prop(scene, "gif_color_map", text="Map", icon="IMAGE_RGB")
        special_row = box.row()
        special_row.prop(scene, "gif_mapfile", text="Map File")
        if scene.gif_color_map == "custom":
            special_row.enabled = True
        else:
            special_row.enabled = False
        row = box.row()
        row.prop(scene, "gif_careful", text="Careful")
        row.prop(scene, "gif_optimize", text="Optimize")
        row = box.row()
        row.prop(scene, "gif_colors", text="Colors")
        row.prop(scene, "gif_loop_count", text="Loop")
        row = layout.row()
        row.prop(scene, "gif_dither_conversion", text="Dither Conversion")
        row = layout.row()
        row.prop(scene, "delete_frames", text="Cleanup on Completion")
        row = layout.row()
        row.operator("sequencerextra.fps_adjust",
                     icon="RECOVER_LAST")
        row.prop(scene, "fps_adjustment", text="")
        row = layout.row()
        row.operator("sequencerextra.render_gif",
                     icon="RENDER_ANIMATION")
        row.operator("sequencerextra.import_gif",
                     icon="LIBRARY_DATA_DIRECT")

class ODP_UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Bligify to ODP"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.prop(scene, "odp_aspect_ratio", text="Aspect")
        row = box.row()
        row.prop(scene, "odp_offset_left", text="Offset Left")
        row = box.row()
        row.prop(scene, "odp_offset_right", text="Offset Right")
        row = box.row()
        row.prop(scene, "odp_offset_top", text="Offset Top")
        row = box.row()
        row.prop(scene, "odp_offset_bottom", text="Offset Bottom")
        row = box.row()
        row.prop(scene, "odp_border_thickness", text="Border")
        row.prop(scene, "odp_border_color", text="")
        row = layout.row()
        row.operator("sequencerextra.export_odp", text="Render ODP", icon="RENDER_RESULT")
    

def initprop():
    
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
    
    aspect_ratios = [
        ("4:3", "4:3", "28cm wide by 21cm height"),
        ("16:9", "16:9", "28cm wide by 15.75cm height"),
    ]
    
    bpy.types.Scene.odp_aspect_ratio = bpy.props.EnumProperty(
        name="ODP Aspect Ratio",
        items=aspect_ratios,
        description="The aspect ratio that will be used in the slideshow",
        default="4:3"
    )
    
    bpy.types.Scene.odp_offset_left = bpy.props.FloatProperty(
        name="ODP Offset Left",
        description="Offset the GIF from the left by x centimeters",
        default=1.0,
    )
    
    bpy.types.Scene.odp_offset_right = bpy.props.FloatProperty(
        name="ODP Offset Right",
        description="Offset the GIF from the right by x centimeters",
        default=1.0,
    )
    
    bpy.types.Scene.odp_offset_top = bpy.props.FloatProperty(
        name="ODP Offset Top",
        description="Offset the GIF from the top by x centimeters",
        default=1.0
    )
    
    bpy.types.Scene.odp_offset_bottom = bpy.props.FloatProperty(
        name="ODP Offset Bottom",
        description="Offset the GIF from the bottom by x centimeters",
        default=1.0
    )
    
    bpy.types.Scene.odp_border_thickness = bpy.props.IntProperty(
        name="ODP Border Thickness",
        default=3,
        description="Thickness of the border around the animated GIF",
        min=0,
    )
    
    bpy.types.Scene.odp_border_color = bpy.props.FloatVectorProperty(  
       subtype='COLOR_GAMMA',
       description="Border color around the animated GIF",
       size=3,
       default=(0.2, 0.2, 0.2),
       min=0.0, 
       max=1.0,
    )
        

def register():
    bpy.utils.register_module(__name__)
    initprop()

def unregister():
    bpy.utils.unregister_module(__name__)
    
    del bpy.types.Scene.gif_dither
    del bpy.types.Scene.gif_disposal
    del bpy.types.Scene.gif_color_method
    del bpy.types.Scene.gif_color_map
    del bpy.types.Scene.gif_mapfile
    del bpy.types.Scene.gif_careful
    del bpy.types.Scene.gif_dither_conversion
    del bpy.types.Scene.delete_frames
    del bpy.types.Scene.gif_colors
    del bpy.types.Scene.gif_loop_count
    del bpy.types.Scene.fps_adjustment
    

if __name__ == "__main__":
    register()
