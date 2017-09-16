import bpy
from bpy_extras.io_utils import ExportHelper
import os
import shutil
import ntpath

from .odp_functions.make_manifest import make_manifest
from .odp_functions.looped_page import looped_page
from .odp_functions.unlooped_page import unlooped_page
from .odp_functions.folder_zip import folder_zip
from .odp_functions.color_to_hexcode import color_to_hexcode

def get_gif_frames_folder(gif_name, directory):
    """Gets the full path to the frames folder"""
    output = ''
    for file in os.listdir(directory):
        if file.startswith(gif_name) and len(file) > len(output):
            output = file
    
    return os.path.join(directory, output)

def get_border_color(scene):
    """returns the border color as a hexcode"""
    
    color_list = [scene.odp_border_color[0],
    scene.odp_border_color[1],
    scene.odp_border_color[2],]

    color = color_to_hexcode(color_list)
    return color

def get_content_intro(scene):
    
    color = get_border_color(scene)
    
    content = [
        '<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:smil="urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0" xmlns:anim="urn:oasis:names:tc:opendocument:xmlns:animation:1.0" xmlns:rpt="http://openoffice.org/2005/report" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:officeooo="http://openoffice.org/2009/office" xmlns:tableooo="http://openoffice.org/2009/table" xmlns:drawooo="http://openoffice.org/2010/draw" xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0" xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0" xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0" xmlns:css3t="http://www.w3.org/TR/css3-text/" office:version="1.2">',
        '<office:automatic-styles>',
        
        """<style:style style:name="graphic_rectangle" style:family="graphic">
            <style:graphic-properties draw:fill-color="[gif_border_color]" svg:stroke-color="[gif_border_color]"/>
        </style:style>""".replace('[gif_border_color]',  color),

        """<style:style style:name="image_unbordered" style:family="graphic">
            <style:graphic-properties style:protect="size"/>
        </style:style>""",
        
        """<style:style style:name="page_standard" style:family="drawing-page">
            <style:drawing-page-properties presentation:background-visible="true"/>
        </style:style>""",

        '</office:automatic-styles>',
        
        '<office:body>',
        '<office:presentation>'
    ]
    return content
    

class ExportODP(bpy.types.Operator, ExportHelper):
    bl_label = "Export ODP"
    bl_idname = "sequencerextra.export_odp"
    bl_description = "Render an ODP with the animated GIF loaded inside\n\nHandy for creating stepwise animations."

    filename_ext = ".odp"
    
    def __init__(self):
        self.folder_path = ''
        self.file_list = []
        self.folder_list = []
    
    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene and scene.sequence_editor:
            return True
        else:
            return False
    
    def execute(self, context):
        scene = context.scene
        self.filepath = os.path.abspath(self.filepath)
        self.cleanup_setting = scene.delete_frames
        scene.delete_frames = False
        
        self.gif_path = os.path.splitext(self.filepath)[0] + '.gif'
        
        if scene.gif_loop_count > 0:
            bpy.ops.sequencerextra.render_gif(filepath=self.gif_path, 
                blank_first_frame=True)
        else:
            bpy.ops.sequencerextra.render_gif(filepath=self.gif_path)
        
        wm = context.window_manager
        wm.modal_handler_add(self)
        self.timer = wm.event_timer_add(0.5, context.window)
        
        return {"RUNNING_MODAL"}
    
    def modal(self, context, event):
        
        if event.type == 'TIMER':
            if os.path.isfile(self.gif_path):
                scene = context.scene
                scene.delete_frames = self.cleanup_setting
                
                gif_name = os.path.splitext(ntpath.basename(self.filepath))[0]
                folder = os.path.dirname(self.filepath)
                gif_frames_folder = get_gif_frames_folder(gif_name, folder)
                
                self.file_list = []
                self.folder_list = []
                self.pictures_list = []
                
                pictures_folder = os.path.join(os.path.dirname(
                    self.filepath), 'Pictures')
                
                try:
                    os.makedirs(pictures_folder)
                except FileExistsError:
                    shutil.rmtree(pictures_folder)
                    os.makedirs(pictures_folder)
                
                new_gif_path = os.path.join(pictures_folder, 
                    ntpath.basename(self.gif_path))
                shutil.move(self.gif_path, new_gif_path)
                self.pictures_list.append(ntpath.basename(self.gif_path))
                
                self.folder_list.append(pictures_folder)
                
                content = get_content_intro(scene)
                
                if scene.gif_loop_count == 0:
                    image_content = looped_page(
                        scene.render.resolution_x, 
                        scene.render.resolution_y, 
                        ntpath.basename(self.gif_path),
                        scene.odp_aspect_ratio,
                        offset_left=scene.odp_offset_left,
                        offset_right=scene.odp_offset_right,
                        offset_top=scene.odp_offset_top,
                        offset_bottom=scene.odp_offset_bottom,
                        border_thickness=scene.odp_border_thickness)
                else:
                    images = sorted(os.listdir(gif_frames_folder))
                    
                    start = os.path.join(folder, 'first_frame.gif')
                    shutil.move(start, os.path.join(pictures_folder, ntpath.basename(start)))
                    self.pictures_list.append(ntpath.basename(start))
                    
                    end = os.path.join(gif_frames_folder, images[-2])
                    self.pictures_list.append(ntpath.basename(end))
                    shutil.copy(end, os.path.join(pictures_folder, ntpath.basename(end)))
                    
                    image_content = unlooped_page(
                        scene.render.resolution_x, 
                        scene.render.resolution_y,
                        ntpath.basename(start),
                        ntpath.basename(self.gif_path),
                        ntpath.basename(end),
                        scene.odp_aspect_ratio,
                        offset_left=scene.odp_offset_left,
                        offset_right=scene.odp_offset_right,
                        offset_top=scene.odp_offset_top,
                        offset_bottom=scene.odp_offset_bottom,
                        border_thickness=scene.odp_border_thickness)
                
                content.append(image_content)
                
                content.append('</office:presentation>')
                content.append('</office:body>')
                content.append('</office:document-content>')
                
                content_path = os.path.join(os.path.dirname(self.filepath), 'content.xml')
                f = open(content_path, 'w')
                f.write('\n'.join(content))
                f.close()
                self.file_list.append(content_path)
                
                meta = os.path.join(os.path.dirname(self.filepath), 'META-INF')
                try:
                    os.makedirs(meta)
                except FileExistsError:
                    shutil.rmtree(meta)
                    os.makedirs(meta)
                manifest = os.path.join(meta, 'manifest.xml')
                manifest_text = make_manifest(self.pictures_list)
                f = open(manifest, 'w')
                f.write(manifest_text)
                f.close()
                self.folder_list.append(meta)
                
                if scene.odp_aspect_ratio == '16:9':
                    folder = os.path.abspath(os.path.dirname(__file__))
                    style_xml = os.path.join(folder, 'odp_functions', '16_9.xml')
                    out_style = os.path.join(os.path.dirname(self.filepath), 'styles.xml')
                    shutil.copy(style_xml, out_style)
                    self.file_list.append(out_style)
                
                folder_zip(self.filepath, self.folder_list, self.file_list)
                
                for file in self.file_list:
                    os.remove(file)
                
                shutil.rmtree(meta)
                shutil.rmtree(pictures_folder)
                
                if scene.delete_frames == True:
                    shutil.rmtree(gif_frames_folder)
                    
                
                return {"FINISHED"}
                
            else:
                return {"PASS_THROUGH"}
                
        else:
            return {"PASS_THROUGH"}
            
            
            
