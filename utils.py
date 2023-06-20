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
