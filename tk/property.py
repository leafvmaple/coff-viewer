from tkinter import Frame, CENTER, NO
from tkinter.ttk import Treeview


COLUMN_COUNT = 8


class Property(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        columns = ['' for i in range(COLUMN_COUNT)]

        self.tv = Treeview(self, columns=columns, show='headings')
        for i in range(COLUMN_COUNT):
            id = '%d' % i
            self.tv.column(id, anchor=CENTER, stretch=NO, width=25)
            self.tv.heading(id, text=id)

        self.tv.pack(side='top', fill='both', expand=True)

        self.master = master

    def update(self, data):
        count = len(data)
        supplement = count % COLUMN_COUNT
        if supplement != 0:
            data += b'\0' * (COLUMN_COUNT - supplement)
            count = len(data)
        for i in range(count // COLUMN_COUNT):
            values = ['%02X' % x for x in data]
            self.tv.insert('', 'end', text=str(i), values=values)
