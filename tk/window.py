import os

from tkinter import Tk, filedialog, Menu
from tkinter.ttk import Notebook

from tk.tree import Tree
from tk.property import Property

from .utils import bind_event_data


class Window(Tk):
    def __init__(self):
        super().__init__()
        # self.title("COFF VIEWER")

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")

        self.geometry("1500x800")
        # sv_ttk.set_theme("dark")
        self.nb = Notebook(self, height=800, width=1000)
        self.nb.pack(side='left', fill='y', expand=True)

        self.property = Property(self, width=600, height=800)
        self.property.pack(side='right', fill='both', expand=False)

        menubar = Menu(self)
        file_menu = Menu(menubar)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self._menu_open)

        self.config(menu=menubar, bg="black")

    def _bytes_update(self, event):
        self.property.update(event.data)

    def _menu_open(self):
        file = filedialog.askopenfile(mode="rb", filetypes=[
            ('Object File', '.obj .lib .dll .o'),
        ])
        if not file:
            return
        tree = Tree(file, self.nb, columns=['key', 'desc', 'address'], show='tree')
        bind_event_data(tree, '<<PropertyUpdate>>', self._bytes_update)
        # tree.bind('<<PropertyUpdate>>', self._bytes_update)

        self.nb.add(tree, text=os.path.basename(file.name))
