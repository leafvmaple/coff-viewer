from tkinter.ttk import Treeview

import pycoff


def display(tree, parent, k, v, desc, addr, intent):
    intent = '    ' * intent
    if type(desc) is list and len(desc) > 0:
        tv = tree.insert(parent, 'end', text=k, values=(v, desc[0], intent + addr))
        for i in range(1, len(desc)):
            tree.insert(tv, 'end', text='', values=('', desc[i], ''))
    else:
        tv = tree.insert(parent, 'end', text=k, values=(v, desc, intent + addr))
    return tv


def show_node(node, tree: Treeview, parent=None, intent=0):
    data = node.get()
    if type(data) is dict:
        for k, v in data.items():
            if k.startswith('_'):
                continue
            value = v.get()
            if type(value) is str or type(value) is int:
                display(tree, parent, k, value, v._desc, v._addr, intent)
            else:
                tv = display(tree, parent, k, '', v._desc, v._addr, intent)
                show_node(v, tree, tv, intent + 1)
    elif type(data) is list:
        for i, k in enumerate(data):
            value = k.get()
            if type(value) is str:
                display(tree, parent, '', value, k._desc, k._addr, intent)
            else:
                tv = display(tree, parent, "[%d]" % i, '', k._desc, k._addr, intent)
                show_node(k, tree, tv, intent + 1)


class Tree(Treeview):
    def __init__(self, file, *args, **kwargs):
        # super(Treeview, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        node = pycoff.parser(file=file)
        show_node(node, self, '')
