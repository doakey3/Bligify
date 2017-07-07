def looped_page(res_x, res_y, image, aspect_ratio, 
                offset_left=1.0, offset_right=1.0, 
                offset_top=1.0, offset_bottom=1.0,
                border_thickness=0):
    """
    Generates part of) the content.xml file for and odp for a non-looped GIF
    """
    
    if aspect_ratio == '4:3':
        width = 28
        height = 21
    
    elif aspect_ratio == '16:9':
        width = 28
        height = 15.75
    
    x_cents_per_pixel = res_x / width
    y_cents_per_pixel = res_y / height
    
    available_x_space = width - offset_left - offset_right
    available_y_space = height - offset_top - offset_bottom
    
    ratio = res_x / res_y
    available_ratio = available_x_space / available_y_space
    
     
    if ratio >= available_ratio:
        img_w = available_x_space
        img_h = (res_y * available_x_space) / res_x
        
    if ratio < available_ratio:
        img_h = available_y_space
        img_w = (res_x * available_y_space) / res_y
        
    img_x_pos = offset_left + ((available_x_space - img_w) / 2)
    img_y_pos = offset_top + ((available_y_space - img_h) / 2)
    
    border_x_thickness = border_thickness / x_cents_per_pixel
    border_y_thickness = border_thickness / y_cents_per_pixel
    
    border_x_position = img_x_pos - border_x_thickness
    border_y_position = img_y_pos - border_y_thickness
    
    if border_thickness > 0:
        output = '''
        <draw:page draw:style-name="page_standard" draw:master-page-name="Default" presentation:presentation-page-layout-name="AL1T1">
        
            <draw:custom-shape draw:style-name="graphic_rectangle" draw:layer="layout" svg:width="''' + str(img_w + (2 * border_x_thickness)) + '''cm" svg:height="''' + str(img_h + (2 * border_y_thickness)) + '''cm" svg:x="''' + str(border_x_position) + '''cm" svg:y="''' + str(border_y_position) + '''cm">
              <draw:enhanced-geometry svg:viewBox="0 0 21600 21600" draw:type="rectangle" draw:enhanced-path="M 0 0 L 21600 0 21600 21600 0 21600 0 0 Z N"/>
            </draw:custom-shape>
            
            <draw:frame draw:style-name="image_unbordered" draw:layer="layout" svg:width="''' + str(img_w) + '''cm" svg:height="''' + str(img_h) + '''cm" svg:x="''' + str(img_x_pos) + '''cm" svg:y="''' + str(img_y_pos) + '''cm">
              <draw:image xlink:href="Pictures/''' + image + '''" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad">
                <text:p/>
              </draw:image>
            </draw:frame>
            '''
    else:
        output = '''
        <draw:page draw:style-name="page_standard" draw:master-page-name="Default" presentation:presentation-page-layout-name="AL1T1">
            <draw:frame draw:style-name="image_unbordered" draw:layer="layout" svg:width="''' + str(img_w) + '''cm" svg:height="''' + str(img_h) + '''cm" svg:x="''' + str(img_x_pos) + '''cm" svg:y="''' + str(img_y_pos) + '''cm">
              <draw:image xlink:href="Pictures/''' + image + '''" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad">
                <text:p/>
              </draw:image>
            </draw:frame>
            '''
    output += '</draw:page>'
    
    return output
    
