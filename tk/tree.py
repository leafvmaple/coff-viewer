from tkinter.ttk import Treeview
import pydumpbin


def display(tree: Treeview, parent, k, v, node, intent):
    intent = '    ' * intent
    desc = node.desc()
    addr = node._addr

    if type(desc) is list:
        desc = " | ".join(desc)
    tv = tree.insert(parent, 'end', text=k, values=(v, desc, intent + addr))

    # tv._data = node._raw
    tree._raw_dict[tv] = (node._begin, node.to_hex(), node.to_display())
    return tv


def show_node(node, tree: Treeview, parent=None, intent=0):
    data = node.get()
    if type(data) is dict:
        for k, v in data.items():
            if k.startswith('_'):
                continue
            value = v.get()
            if type(value) is str or type(value) is int:
                display(tree, parent, k, value, v, intent)
            else:
                tv = display(tree, parent, k, '', v, intent)
                show_node(v, tree, tv, intent + 1)
    elif type(data) is list:
        for i, k in enumerate(data):
            value = k.get()
            if type(value) is str:
                display(tree, parent, '', value, k, intent)
            else:
                tv = display(tree, parent, "[%d]" % i, '', k, intent)
                show_node(k, tree, tv, intent + 1)


class Tree(Treeview):
    def __init__(self, file, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._raw_dict = {}

        node = pydumpbin.parser(file=file)
        show_node(node, self, '')

        self.bind('<<TreeviewSelect>>', self._treeview_click)
        # bind_event_data(self, '<<TreeviewSelect>>', self._treeview_click)

    def _treeview_click(self, event):
        focus = event.widget.focus()
        data = self._raw_dict[focus]
        self.event_generate('<<PropertyUpdate>>', data=data)
