from tkinter import Frame, CENTER, W, NO
from tkinter.ttk import Treeview
import math

COLUMN_COUNT = 8


class Property(Frame):
    COLUMN_TITLE = [
        ('Address', 80, CENTER),
        ('1', 25, CENTER),
        ('2', 25, CENTER),
        ('3', 25, CENTER),
        ('4', 25, CENTER),
        ('5', 25, CENTER),
        ('6', 25, CENTER),
        ('7', 25, CENTER),
        ('8', 25, CENTER),
        ('', 30, CENTER),
        ('', 80, W)
    ]

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        columns = [''] * (COLUMN_COUNT * 2 + 2)

        self.tv = Treeview(self, columns=columns, show='headings')
        for i, v in enumerate(self.COLUMN_TITLE):
            self.tv.column(i, anchor=v[2], stretch=NO, width=v[1])
            self.tv.heading(i, text=v[0])

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
            self.tv.insert('', 'end', text='', values=addr + hex[begin: end] + [''] + [''.join(display[begin: min(end, count)])])
