import shutil
import os
import ntpath

from .combine_text_items import combine_text_items
from .text_to_xml import text_to_xml

from .make_title_page import make_title_page
from .make_text_page import make_text_page
from .make_image_page import make_image_page
from .make_text_left_image_right_page import make_text_left_image_right_page
from .make_image_left_text_right_page import make_image_left_text_right_page
from .make_text_top_image_bottom_page import make_text_top_image_bottom_page
from .make_image_top_text_bottom_page import make_image_top_text_bottom_page

def make_page(page, page_type, pictures, settings):
    """
    Create page xml sections
    add images to the pictures folder as necessary
    """

    if page_type == 'MAIN_TITLE':
        title = page[0].plain_text
        if len(page) > 1:
            subtitle = page[1].plain_text
        return make_title_page(settings, title, subtitle)
    
    elif page_type == 'TEXT':
        title = page[0].plain_text
        page.pop(0)
        
        text = combine_text_items(page)
        text = text_to_xml(text)
        
        return make_text_page(settings, title, text)
    
    elif page_type == 'IMAGE':
        title = page[0].plain_text
        
        img_path = page[1].text.strip().replace('.. image:: ', '')
        img_filename = ntpath.basename(img_path)
        if not img_filename in os.listdir(pictures):
            shutil.copy(img_path, os.path.join(pictures, img_filename))
        
        return make_image_page(settings, title, img_filename)
    
    elif page_type == 'TEXT_LEFT_IMAGE_RIGHT':
        title = page[0].plain_text
        page.pop(0)
        
        text = combine_text_items(page)
        text = text_to_xml(text)
        
        img_path = page[-1].text.strip().replace('.. image:: ', '')
        img_filename = ntpath.basename(img_path)
        if not img_filename in os.listdir(pictures):
            shutil.copy(img_path, os.path.join(pictures, img_filename))
        
        return make_text_left_image_right_page(settings, title, text, img_filename)
        
    elif page_type == 'IMAGE_LEFT_TEXT_RIGHT':
        title = page[0].plain_text
        page.pop(0)
        
        img_path = page[0].text.strip().replace('.. image:: ', '')
        img_filename = ntpath.basename(img_path)
        if not img_filename in os.listdir(pictures):
            shutil.copy(img_path, os.path.join(pictures, img_filename))
        page.pop(0)
        
        text = combine_text_items(page)
        text = text_to_xml(text)
        
        return make_image_left_text_right_page(settings, title, text, img_filename)
        
    elif page_type == 'TEXT_TOP_IMAGE_BOTTOM':
        title = page[0].plain_text
        page.pop(0)
        
        text = combine_text_items(page)
        text = text_to_xml(text)
        
        img_path = page[-1].text.strip().replace('.. image:: ', '')
        img_filename = ntpath.basename(img_path)
        if not img_filename in os.listdir(pictures):
            shutil.copy(img_path, os.path.join(pictures, img_filename))
        
        return make_text_top_image_bottom_page(settings, title, text, img_filename)
    
    elif page_type == 'IMAGE_TOP_TEXT_BOTTOM':
        title = page[0].plain_text
        page.pop(0)
        
        img_path = page[0].text.strip().replace('.. image:: ', '')
        img_filename = ntpath.basename(img_path)
        if not img_filename in os.listdir(pictures):
            shutil.copy(img_path, os.path.join(pictures, img_filename))
        page.pop(0)
        
        text = combine_text_items(page)
        text = text_to_xml(text)
        
        return make_image_top_text_bottom_page(settings, title, text, img_filename)
    
    
        
        
