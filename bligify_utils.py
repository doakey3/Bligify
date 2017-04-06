import sys


def remove_bads(string):
    """Removes symbols that will mess with subprocess"""
    string = string.replace("\\", "")
    string = string.replace("/", "")
    string = string.replace(":", "")
    string = string.replace("*", "")
    string = string.replace("?", "")
    string = string.replace('"', "")
    string = string.replace("<", "")
    string = string.replace(">", "")
    string = string.replace("|", "")
    string = string.replace("\n", "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    text = ''
    for i in range(len(string)):
        if ord(string[i]) < 128:
            text = text + string[i]
    return text


def update_progress(job_title, progress):
    length = 20
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title,
                                     "#" * block + "-" * (length-block),
                                     "%.2f" % (progress * 100))
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()
