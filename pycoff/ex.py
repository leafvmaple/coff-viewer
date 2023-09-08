import os
import re
import json
import runpy
import datetime
from utility import read


def upper_hex(num):
    return '0x' + hex(num)[2:].upper()


def read_py(f, path):
    if not os.path.exists(path):
        return False
    py_data = runpy.run_path(path)
    if not check_magic(f, py_data):
        return False
    return py_data


def read_file(f, path, check=False):
    py_path = path.replace('.json', '.py')
    py_data = read_py(f, py_path)
    if check and not py_data:
        return False, None

    with open(path, 'r') as jf:
        json_data = json.load(jf)

    return json_data, py_data


def check_magic(f, py_data):
    if "MAGIC" not in py_data:
        return True
    magic_data = py_data["MAGIC"]
    if type(magic_data) is bytes:
        return magic_data == f.read(len(magic_data))
    return magic_data(f)


def get_value(raw, tab):
    obj = re.search(r'(\S+)\[(\S+)*\]', raw)
    key = obj.group(1)
    values = obj.group(2).split('.')
    for value in values:
        tab = tab._data[value]
    num = int(tab._data)
    return key, num


def get_obj(raw_key, tab):
    key = raw_key[1:]
    return tab[key]


class Node:
    def __init__(self, file=None, json_data=None, py_data=None, key='', data=None, from_py=False, num=None):
        self._addr = ''
        self._desc = ''
        self._display = ''
        self._key = key
        self._data = data if data else {}

        if file:
            self._addr = upper_hex(file.tell())

        if num:
            self._data = [Node(file, json_data, py_data, key, from_py=from_py) for i in range(num)]
        elif from_py:
            self.decrypt_from_py(file, self._key, json_data, py_data)
        else:
            self.decrypt(file, json_data, py_data)

    def __getitem__(self, i):
        return self._data[i]

    def __setitem__(self, i, node):
        if type(node) is not Node:
            node = Node(data=node)
        self._data[i] = node

    def __lt__(self, other):
        return self._data < other

    def __gt__(self, other):
        return self._data > other

    def __eq__(self, other):
        return self._data == other

    def __int__(self):
        return self._data

    def decrypt(self, f, json_data, py_data):
        if json_data is None:
            return
        if type(json_data) is str:
            self.decrypt_str(f, json_data, py_data)
        if type(json_data) is dict:
            self.decrypt_dict(f, json_data, py_data)

    def desc(self, json_data):
        if json_data == 'timestamp':
            self._desc = datetime.datetime.fromtimestamp(self._data) if self._data > 0 else 'FFFFFFFF'
        elif type(json_data) is dict:
            self._desc = []
            desc = {eval(k) if type(k) is str else k: v for k, v in json_data.items()}
            keys = sorted(desc, reverse=True)
            value = self._data
            for k in keys:
                if value >= k and value & k:
                    self._desc.append(desc[k])
                    value -= k

    def display(self, json_data):
        if json_data == "0x":
            self._display = upper_hex(self._data)

    def prefix(self, key: str, json_data, tab):
        if key.startswith('?'):
            value = get_obj(key, tab)
            value.desc(json_data)
        elif key.startswith('>'):
            value = get_obj(key, tab)
            value.display(json_data)

    def decrypt_from_py(self, f, key, json_data, py_data):
        if callable(py_data[key]):
            py_data[key](self, f, json_data, py_data)

    def decrypt_json(self, f, json_data, py_data):
        path = os.path.join(os.path.dirname(__file__), 'template', json_data)
        sub_json, sub_py = read_file(f, path)

        if sub_py and '__init__' in sub_py:
            sub_py['__init__'](self, f, sub_json, sub_py)
        else:
            self.decrypt(f, sub_json, sub_py)

    def decrypt_str(self, f, json_data: str, py_data):
        if json_data.endswith('.json'):
            self.decrypt_json(f, json_data, py_data)
        else:
            self._data = read(f, json_data)

    def decrypt_dict(self, f, json_data: dict, py_data):
        for k, v in json_data.items():
            self.prefix(k, v, self._data)

            from_py = False
            num = None

            if k.startswith('$'):
                from_py = True
                k = k[1:]

            if k.startswith('-') or k.startswith('?') or k.startswith('>'):
                continue

            if k.endswith(']'):
                k, num = get_value(k, self)

            self._data[k] = Node(f, v, py_data, k, from_py=from_py, num=num)

    def get(self):
        if self._display != '':
            return self._display
        if type(self._data) is int:
            return upper_hex(self._data)
        return self._data

    def to_data(self):
        data = self.get()
        if type(data) is dict:
            return {k: v.to_data() for k, v in data.items()}
        else:
            return data


def parse(filename):
    with open(filename, 'rb') as f:
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'template')):
            for file in files:
                if not file.endswith('json') or root.endswith('header'):
                    continue
                f.seek(0)
                json_data, py_data = read_file(f, os.path.join(root, file), True)
                if json_data:
                    return Node(f, json_data, py_data)
