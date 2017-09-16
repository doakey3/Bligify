def color_to_hexcode(color):
    """convert float color to hexcode color"""
    for i in range(len(color)):
        color[i] = int(color[i] * 256)
        if color[i] == 256:
            color[i] -= 1
    return '#%02x%02x%02x' % tuple(color)
