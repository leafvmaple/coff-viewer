def format(key, value, desc):
    if type(value) == int:
        res = "{0:X}".format(value)
    elif type(value) == str:
        res = value
    elif type(value) == list:
        res = [format(key, v, desc) for v in value]
    elif type(value) == tuple:
        res = str(value)
    elif type(value) == bytes:
        res = ' '.join(['%02X' % b for b in value])
    return res


def decrypt(obj):
    keys = [v for v in vars(obj).keys() if (not v.startswith('_') or v in obj._display) and v not in obj._filter]
    res = {}
    for k in keys:
        value = getattr(obj, k)
        res[k] = format(k, value, obj._desc)
    return format(obj, keys, obj._desc)
