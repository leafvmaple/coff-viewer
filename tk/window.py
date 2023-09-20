import os

from tkinter import Tk, filedialog, Menu
from tkinter.ttk import Notebook

from tk.tree import Tree


class Window(Tk):
    def __init__(self):
        super().__init__()
        # self.title("COFF VIEWER")

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        self.geometry("1200x800")
        # sv_ttk.set_theme("dark")
        self.nb = Notebook(self, height=800)
        self.nb.pack(side='top', fill='both', expand=False)

        menubar = Menu(self)
        file_menu = Menu(menubar)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self._menu_open)

        self.config(menu=menubar, bg="black")

    def _menu_open(self):
        file = filedialog.askopenfile(mode="rb", filetypes=[('Object File', '.obj .lib .dll')])
        if not file:
            return
        tree = Tree(file, self.nb, columns=['key', 'desc', 'address'], height=800, show='tree')
        self.nb.add(tree, text=os.path.basename(file.name))
