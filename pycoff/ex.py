import os
import re
import json
import runpy
import datetime
from utility import read
from tk import show


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def read_py(f, path):
    py_data = runpy.run_path(path)
    if "MAGIC" in py_data:
        magic = f.read(len(py_data["MAGIC"]))
        if magic != py_data["MAGIC"]:
            return False, None

    json_data = read_json(path.replace('.py', '.json'))
    return json_data, py_data


def get_value(raw, tab):
    obj = re.search(r'(\S+)\[(\S+)*\]', raw)
    key = obj.group(1)
    values = obj.group(2).split('.')
    for value in values:
        tab = tab[value]
    num = int(tab)
    return key, num


def get_display(value, desc):
    if desc == "0x":
        return hex(value)


def get_desc(value, desc):
    res = []
    if desc == 'timestamp':
        return datetime.datetime.fromtimestamp(value) if value > 0 else 'FFFFFFFF'
    elif type(desc) is dict:
        keys = sorted(desc, reverse=True)
        for k in keys:
            num = eval(k) if type(k) is str else k
            if value > num and value & num:
                res.append(desc[k])
                value -= num
        return res


def get_py(f, key, json_data, py_data):
    if callable(py_data[key]):
        return py_data[key](f, json_data, py_data)


PREFIX = {
    '?': lambda f, key, dst, json_data, py_data: get_display(dst[key], json_data[key]),
    '>': lambda f, key, dst, json_data, py_data: get_desc(dst[key], json_data[key]),
    '$': lambda f, key, dst, json_data, py_data: get_py(f, py_data[key])
}


def prefix(key):
    for k, func in PREFIX.items():
        if key.startswith(k):
            return key[1:], func
    return key, lambda f, key, dst, json_data, py_data: decrypt(f, (json_data[key], py_data))


def decrypt(f, json_data, py_data):
    if type(json_data) is str:
        if json_data.endswith('.py'):
            sub_json, sub_py = read_py(f, os.path.join(os.path.dirname(__file__), 'template', json_data))
            return decrypt(f, sub_json, sub_py)
        elif json_data.endswith('.json'):
            data = read_json(os.path.join(os.path.dirname(__file__), 'template', json_data))
            return decrypt(f, data, None)
        return read(f, json_data)
    elif type(json_data) is dict:
        res = {}
        for k, v in json_data.items():
            if k.startswith('-'):
                continue

            key = k
            addr = hex(f.tell())

            if type(v) is str and v.startswith('@'):
                value = v[1:]
                v = res if value == '' else res[value]

            if k.startswith('?'):
                key = key[1:]
                if key in res:
                    res[k] = get_desc(res[key], v)
            elif k.startswith('>'):
                key = key[1:]
                if key in res:
                    res[k] = get_display(res[key], v)
            elif k.startswith('$'):
                key = key[1:]
                if key.endswith(']'):
                    key, num = get_value(key, res)
                    res[key] = [get_py(f, key, v, py_data) for i in range(num)]
                else:
                    res[key] = get_py(f, key, v, py_data)
            else:
                if key.endswith(']'):
                    key, num = get_value(key, res)
                    res[key] = [decrypt(f, v, py_data) for i in range(num)]
                else:
                    res[key] = decrypt(f, v, py_data)
            res['#' + key] = addr
        return res


def parse(filename):
    with open(filename, 'rb') as f:
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'template')):
            for file in files:
                if not file.endswith('py') or root.endswith('header'):
                    continue
                f.seek(0)
                json_data, py_data = read_py(f, os.path.join(root, file))
                if json_data:
                    show(filename, decrypt(f, json_data, py_data))
                    # print(decrypt(f, data))


parse('E:\\L3D11Engine\\x64\\Debug\\LEngineD.lib')
