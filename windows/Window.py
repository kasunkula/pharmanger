import tkinter


class Window:
    def __init__(self, parent, title):
        self.main_window = tkinter.Toplevel(parent)
        self.main_window.protocol('WM_DELETE_WINDOW', lambda: self.on_close(self.main_window))
        self.main_window.title(title)
        self.parent = parent
        self.is_open = True
        self.render()

    def on_close(self, window):
        self.is_open = False
        window.destroy()

    def Closed(self):
        return not self.is_open

    def focus(self):
        self.main_window.focus_force()

    def render(self):
        for item in self.main_window.winfo_children():
            item.destroy()
