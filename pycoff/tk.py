from tkinter import Tk, Label
from tkinter.ttk import Treeview

from ex import parse, Node
# import sv_ttk


def display(tree, parent, k, v, desc, addr, intent):
    intent = '    ' * intent
    if type(desc) is list and len(desc) > 0:
        tv = tree.insert(parent, 'end', text=k, values=(v, desc[0], intent + addr))
        for i in range(1, len(desc)):
            tree.insert(tv, 'end', text='', values=('', desc[i], ''))
    else:
        tv = tree.insert(parent, 'end', text=k, values=(v, desc, intent + addr))
    return tv


def show_node(node: Node, tree: Treeview, parent=None, intent=0):
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


def show_path(path):
    window = Tk()
    window.title(path)

    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "dark")

    # sv_ttk.set_theme("dark")

    # decrypt(obj)

    tv = Treeview(window, columns=['key', 'desc', 'address'], height=600)

    # show_tree(data, tv, '')

    node = parse(path)
    show_node(node, tv, '')

    tv.pack(fill='both', expand=False)

    # label = Label(root)
    # label.grid()

    window.geometry("1200x800")
    window.config(bg="black")
    window.mainloop()


show_path('LEngineD.lib')
