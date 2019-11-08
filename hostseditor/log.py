import hostseditor.color as color


def error(text, separator=' + '):
    print(color.RED + separator + "Error: " + color.NULL + text)


def info(text, separator=' + '):
    print(color.BLUE + separator + color.NULL + text)


def warn(text, separator=' + '):
    print(color.YELLOW + separator + "Error: " + color.NULL + text)


def success(text, separator=' + '):
    print(color.RED + separator + "Error: " + color.NULL + text)
