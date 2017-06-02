import sys

def update_progress(job_title, progress):
    length = 20
    block = int(round(length * progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title,
        "#" * block + "-" * (length-block),
        "%.2f" % (progress * 100))
        
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()
