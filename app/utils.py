def strtobool(val: str, default: bool = False) -> bool:
    """Convert a string representation of a boolean to a boolean

    Accepted values for True: yes, y, true, t, on, 1.
    Accepted values for False: no, n, false, off, 0.

    Note: The input value will be lowercased, so it also matches e.g.
    'Yes', 'N', 'ON', and so on. If nothing matches, a default will
    be returned, which is False if not changed.
    """
    val = val.lower()
    if val in {'y', 'yes', 't', 'true', 'on', '1'}:
        return True
    elif val in {'n', 'no', 'f', 'false', 'off', '0'}:
        return False
    return default
