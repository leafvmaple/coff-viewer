import os

from tkinter import Tk, filedialog, Menu
from tkinter.ttk import Treeview, Notebook

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


def open_file(nb: Notebook):
    tv = Treeview(nb, columns=['key', 'desc', 'address'], height=800, show='tree')

    file = filedialog.askopenfile(mode="rb", filetypes=[('Object File', '.obj .lib .dll')])
    node = parse(file=file)

    show_node(node, tv, '')
    nb.add(tv, text=os.path.basename(file.name))


if __name__ == "__main__":
    window = Tk()
    window.title("COFF VIEWER")

    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "dark")

    window.geometry("1200x800")
    # sv_ttk.set_theme("dark")

    nb = Notebook(window, height=800)
    # nb.pack(fill='both', expand=False)

    menubar = Menu(window)
    file_menu = Menu(menubar)
    menubar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open', command=lambda: open_file(nb))

    # label = Label(root)
    # label.grid()

    nb.pack(fill='both', expand=False)

    window.config(menu=menubar, bg="black")
    window.mainloop()
