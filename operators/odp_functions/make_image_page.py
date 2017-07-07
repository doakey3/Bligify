from PIL import Image

def make_image_page(settings, title, image):
    """Make a slide that consists only of a title and an image"""
    
    rect_h = float(settings['title_background_height']) * float(settings['height'])

    x_cents_per_pixel = float(settings['resolution_x']) / float(settings['width'])
    y_cents_per_pixel = float(settings['resolution_y']) / float(settings['height'])
    
    available_x_space = float(settings['resolution_x']) - (2 * x_cents_per_pixel * float(settings['padding']))
    available_y_space = float(settings['resolution_y']) - (2 * y_cents_per_pixel * float(settings['padding'])) - (rect_h * y_cents_per_pixel)
    
    img = Image.open(image)
    
    ratio = img.size[0] / img.size[1]
    available_ratio = available_x_space / available_y_space
    
    if ratio >= available_ratio:
        img_w = available_x_space / x_cents_per_pixel
        img_h = ((available_x_space / img.size[0]) * img.size[1]) / y_cents_per_pixel
        
    if ratio < available_ratio:
        img_h = available_y_space / y_cents_per_pixel
        img_w = ((available_y_space / img.size[1]) * img.size[0]) / x_cents_per_pixel
        
    img_x_pos = (float(settings['width']) - img_w) / 2
    img_y_pos = img_y_pos = ((float(settings['height']) - img_h - float(settings['padding']) - rect_h) / 2) + rect_h + (float(settings['padding']) / 2)
    mode = img.mode
    
    output = '''
      <draw:page draw:style-name="page_standard" draw:master-page-name="Default" presentation:presentation-page-layout-name="AL1T1">
        
        <draw:custom-shape draw:style-name="graphic_rectangle" draw:layer="layout" svg:width="''' + settings['width'] + '''cm" svg:height="''' + str(rect_h) + '''cm" svg:x="0cm" svg:y="0cm">
          <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:type="rectangle" draw:enhanced-path="M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N"/>
        </draw:custom-shape>
        
        <draw:line draw:style-name="line_title" draw:layer="layout" svg:x1="0cm" svg:y1="''' + str(rect_h) + '''cm" svg:x2="''' + settings['width'] + '''cm" svg:y2="''' + str(rect_h) + '''cm">
          <text:p/>
        </draw:line>
        
        <draw:frame presentation:style-name="frame_title" draw:layer="layout" svg:width="''' + settings['width'] + '''cm" svg:height="''' + str(rect_h) + '''cm" svg:x="0cm" svg:y="0cm" presentation:class="title">
          <draw:text-box>
            <text:p text:style-name="paragraph_centered">
              <text:span text:style-name="text_title">''' + title + '''</text:span>
            </text:p>
          </draw:text-box>
        </draw:frame>
        '''
    
    if image.endswith('.gif'):
        
        img_rect_pos_x = str(img_x_pos - 0.106)
        img_rect_pos_y = str(img_y_pos - 0.106)
        img_rect_w = str(img_w + (2 * 0.106))
        img_rect_h = str(img_h + (2 * 0.106))
        
        output += '''
        
        <draw:custom-shape draw:style-name="graphic_rectangle" draw:layer="layout" svg:width="''' + img_rect_w + '''cm" svg:height="''' + img_rect_h + '''cm" svg:x="''' + img_rect_pos_x + '''cm" svg:y="''' + img_rect_pos_y + '''cm">
          <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:type="rectangle" draw:enhanced-path="M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N"/>
        </draw:custom-shape>
        
        <draw:frame draw:style-name="image_unbordered" draw:layer="layout" svg:width="''' + str(img_w) + '''cm" svg:height="''' + str(img_h) + '''cm" svg:x="''' + str(img_x_pos) + '''cm" svg:y="''' + str(img_y_pos) + '''cm">
          <draw:image xlink:href="Pictures/''' + image + '''" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad">
            <text:p/>
          </draw:image>
        </draw:frame>
        '''
    
    elif mode == 'RGB':
        output += '''
        <draw:frame draw:style-name="image_bordered" draw:layer="layout" svg:width="''' + str(img_w) + '''cm" svg:height="''' + str(img_h) + '''cm" svg:x="''' + str(img_x_pos) + '''cm" svg:y="''' + str(img_y_pos) + '''cm">
          <draw:image xlink:href="Pictures/''' + image + '''" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad">
            <text:p/>
          </draw:image>
        </draw:frame>
        '''
    
    else:
        output += '''
         <draw:frame draw:style-name="image_unbordered" draw:layer="layout" svg:width="''' + str(img_w) + '''cm" svg:height="''' + str(img_h) + '''cm" svg:x="''' + str(img_x_pos) + '''cm" svg:y="''' + str(img_y_pos) + '''cm">
          <draw:image xlink:href="Pictures/''' + image + '''" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad">
            <text:p/>
          </draw:image>
        </draw:frame>
        '''
    output += "</draw:page>"
    return output.strip()
