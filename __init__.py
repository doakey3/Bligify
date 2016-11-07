bl_info = {
    "name": "bligify",
    "description": "export/import animated GIF from VSE",
    "author": "doakey3",
    "version": (1, 1, 0),
    "blender": (2, 7, 8),
    "warning": 'Requires imagemagick & gifsicle install on linux',
    "wiki_url": "https://github.com/doakey3/bligify",
    "tracker_url":"https://github.com/doakey3/bligify/issues",
    "category": "Sequencer"}
    
import bpy
from .fpsadjust import FPSAdjust
from .importgif import ImportGIF
from .rendergif import RenderGIF

class gif_UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Bliggify"
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop_menu_enum(context.scene, 'gif_quality', 
            text='GIF Quality', icon='SCRIPTWIN')
        box.prop(context.scene, 'gif_looped',
            text='Loop GIF')
        row = box.row()
        row.operator("sequencerextra.fps_adjust", 
            icon="RECOVER_LAST")
        row.prop(context.scene, 'fps_adjustment',text="")
        row = box.row()
        row.operator('sequencerextra.render_gif',
            icon="RENDER_ANIMATION")
        row.operator('sequencerextra.import_gif',
            icon="LIBRARY_DATA_DIRECT")

def initprop():
    
    gif_quality_options = [
        ('Full','Full','All colors included (bigger filesize)'),
        ('256','256','Limit number of colors to 256'),
        ('128','128','Limit number of colors to 128'),
        ('64','64','Limit number of colors to 64')]
    
    bpy.types.Scene.gif_quality = bpy.props.EnumProperty(
        items=gif_quality_options,
        description = "Number of colors used in final GIF")
        
    bpy.types.Scene.gif_looped = bpy.props.BoolProperty(
        name="Enable or Disable",
        description="Make the GIF Looped",
        default = True)
    
    bpy.types.Scene.fps_adjustment = bpy.props.IntProperty(
        description = "Set the new FPS that will be used",
        default = 10,
        min=1)

def register():
    bpy.utils.register_module(__name__)
    initprop()
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
    del bpy.types.Scene.gif_quality
    del bpy.types.Scene.gif_looped
    
if __name__ == "__main__":
    register()
