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
