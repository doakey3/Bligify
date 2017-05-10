import bpy
from .fpsadjust import FPSAdjust
from .importgif import ImportGIF
from .rendergif import RenderGIF

bl_info = {
    "name": "Bligify",
    "description": "export/import animated GIF from VSE",
    "author": "doakey3",
    "version": (1, 2, 0),
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
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.prop(context.scene, "gif_colors", text="Color")
        row.prop(context.scene, "gif_looped", text="Loop GIF")
        row = box.row()
        row.operator("sequencerextra.fps_adjust",
                     icon="RECOVER_LAST")
        row.prop(context.scene, "fps_adjustment", text="")
        row = box.row()
        row.operator("sequencerextra.render_gif",
                     icon="RENDER_ANIMATION")
        row.operator("sequencerextra.import_gif",
                     icon="LIBRARY_DATA_DIRECT")


def initprop():

    bpy.types.Scene.gif_colors = bpy.props.IntProperty(
        description="Number of colors used in the GIF",
        default=256,
        max=256,
        min=2,
        )

    bpy.types.Scene.gif_looped = bpy.props.BoolProperty(
        name="Enable or Disable",
        description="Make the GIF Looped",
        default=True
        )

    bpy.types.Scene.fps_adjustment = bpy.props.IntProperty(
        description="Set the new FPS that will be used",
        default=10,
        min=1
        )

def register():
    bpy.utils.register_module(__name__)
    initprop()


def unregister():
    bpy.utils.unregister_module(__name__)

    del bpy.types.Scene.gif_colors
    del bpy.types.Scene.gif_looped
    del bpy.types.Scene.fps_adjustment

if __name__ == "__main__":
    register()
