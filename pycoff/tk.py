from tkinter import Tk, Label
from tkinter.ttk import Treeview
# import sv_ttk


def get_dest(key, tab):
    if key not in tab:
        return ''
    value = tab[key]
    if type(value) is list:
        return ' | ' .join(value)
    return value


def show_tree(data, tree: Treeview, parent=None):
    if type(data) is dict:
        for k, v in data.items():
            if k.startswith('_') or k.startswith('>') or k.startswith('#') or k.startswith('?'):
                continue
            if '>' + k in data:
                v = data['>' + k]
            addr = data['#' + k] if '#' + k in data else ''
            desc = data['?' + k] if '?' + k in data else ''
            if type(v) is str or type(v) is int:
                if type(desc) is list and len(desc) > 0:
                    tv = tree.insert(parent, 'end', text=k, values=(v, desc[0], addr))
                    for i in range(1, len(desc)):
                        tree.insert(tv, 'end', text='', values=('', desc[i], addr))
                else:
                    tree.insert(parent, 'end', text=k, values=(v, desc, addr))

            else:
                tv = tree.insert(parent, 'end', text=k, values=('', desc, addr))
                show_tree(v, tree, tv)
    elif type(data) is list:
        for i, k in enumerate(data):
            if type(k) is str:
                tree.insert(parent, 'end', values=(k))
            else:
                tv = tree.insert(parent, 'end', text="[%d]" % i)
                show_tree(k, tree, tv)


def show(path, data):
    window = Tk()
    window.title(path)

    window.tk.call("source", "azure.tcl")
    window.tk.call("set_theme", "dark")

    # sv_ttk.set_theme("dark")

    # decrypt(obj)

    tv = Treeview(window, columns=['key', 'value'], height=600)

    show_tree(data, tv, '')

    tv.pack(fill='both', expand=False)

    # label = Label(root)
    # label.grid()

    window.geometry("1200x800")
    window.config(bg="black")
    window.mainloop()
