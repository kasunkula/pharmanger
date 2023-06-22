def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int(string):
    try:
        int(string)
        if string != str(int(string)):
            return False
        return True
    except ValueError:
        return False


def transform_str_on_keyboard_input(str, key):
    if key == "\b":  # if backspace remove last character
        return_str = str[:len(str) - 1]
    else:
        return_str = str + key
    return return_str.strip().replace('\x1b', '')

