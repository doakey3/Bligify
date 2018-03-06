import subprocess


def is_gifsicle_installed():
    """
    Check if gifsicle is installed

    Returns
    -------
    bool
    """
    try:
        subprocess.call(
            ['gifsicle', '--help'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return True

    except OSError:
        return False
