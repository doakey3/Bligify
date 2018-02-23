def get_open_channel(scene):
    """Get a channel with nothing in it"""
    channels = []
    try:
        for strip in scene.sequence_editor.sequences_all:
            channels.append(strip.channel)
        if len(channels) > 0:
            return max(channels) + 1
        else:
            return 1
    except AttributeError:
        return 1