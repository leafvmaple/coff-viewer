from tkinter import Frame, CENTER, NO
from tkinter.ttk import Treeview
import math

COLUMN_COUNT = 8


class Property(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        columns = [''] * (COLUMN_COUNT * 2 + 2)

        self.tv = Treeview(self, columns=columns, show='headings')
        self.tv.column(0, anchor=CENTER, stretch=NO, width=80)
        self.tv.heading(0, text='Address')
        for i in range(COLUMN_COUNT):
            self.tv.column(i + 1, anchor=CENTER, stretch=NO, width=25)
            self.tv.heading(i + 1, text=i % COLUMN_COUNT)

        self.tv.column(COLUMN_COUNT + 1, anchor=CENTER, stretch=NO, width=30)
        self.tv.heading(COLUMN_COUNT + 1, text='')

        for i in range(COLUMN_COUNT):
            self.tv.column(i + COLUMN_COUNT + 2, anchor=CENTER, stretch=NO, width=18)

        self.tv.pack(side='top', fill='both', expand=True)

        self.master = master

    def clear(self):
        for i in self.tv.get_children():
            self.tv.delete(i)

    def update(self, data):
        self.clear()
        offset, hex, display = data
        count = len(hex)
        if count % COLUMN_COUNT != 0:
            hex += [''] * (COLUMN_COUNT - (count % COLUMN_COUNT))

        for i in range(math.ceil(count / COLUMN_COUNT)):
            begin = i * COLUMN_COUNT
            end = (i + 1) * COLUMN_COUNT
            addr = ['%08X' % (offset + begin)]
            self.tv.insert('', 'end', text='', values=addr + hex[begin: end] + [''] + display[begin: min(end, count)])
