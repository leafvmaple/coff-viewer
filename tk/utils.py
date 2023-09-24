from tkinter import Event


def bind_event_data(widget, sequence, func, add=None):
    def _substitute(*args, **kw):
        e = Event()
        e.data = eval(args[0])
        e.widget = widget
        return (e,)

    funcid = widget._register(func, _substitute, needcleanup=1)
    cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format('+' if add else '', funcid)
    widget.tk.call('bind', widget._w, sequence, cmd)
