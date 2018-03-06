import subprocess


def is_magick_installed():
    """
    Check if imagemagick is installed and usable

    Returns
    -------
    bool
    """
    try:
        subprocess.call(
            ['magick', '--help'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return True

    except OSError:
        return False
