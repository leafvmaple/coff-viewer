import os

from tkinter import Tk, filedialog, Menu
from tkinter.ttk import Notebook

from tk.tree import Tree
from tk.property import Property


class Window(Tk):
    def __init__(self):
        super().__init__()
        # self.title("COFF VIEWER")

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        self.geometry("1400x800")
        # sv_ttk.set_theme("dark")
        self.nb = Notebook(self, height=800, width=1000)
        self.nb.pack(side='left', fill='y', expand=True)

        self.property = Property(self, width=400, height=800)
        self.property.update(b'abcdefg')
        self.property.pack(side='right', fill='both', expand=False)

        menubar = Menu(self)
        file_menu = Menu(menubar)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self._menu_open)

        self.config(menu=menubar, bg="black")

    def _menu_open(self):
        file = filedialog.askopenfile(mode="rb", filetypes=[('Object File', '.obj .lib .dll')])
        if not file:
            return
        tree = Tree(file, self.nb, columns=['key', 'desc', 'address'], show='tree')
        self.nb.add(tree, text=os.path.basename(file.name))
