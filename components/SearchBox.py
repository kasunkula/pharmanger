from tkinter import *
import utils

class SearchBox:
    def __init__(self, parent, row, column, label, data):
        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column, columnspan=2, sticky=W)
        Label(self.frame, text=label, width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=0, column=0,
                                                                                 pady=5, padx=5)

        self.text_box = Entry(self.frame, width=40, font=('Arial', 16, 'bold'))
        self.text_box.bind("<Key>", self.on_filter_text_change)
        self.text_box.grid(sticky=W, row=0, column=1, pady=5, padx=5)
        self.filter_text = None
        self.list = Listbox(self.frame, width=40, selectmode=SINGLE)
        self.list.grid(sticky=W, row=1, column=1, pady=5, padx=5)
        self.original_data = data
        self.data = self.original_data
        self.populate_list()

    def populate_list(self):
        self.list.delete(0, len(self.original_data))
        for index in range(len(self.data)):
            self.list.insert(index, self.data[index])

    def refine_list(self):
        if self.filter_text is None or len(self.filter_text) == 0:
            self.data = self.original_data
            return

        self.data = \
            list(filter(lambda x:
                        (str.lower(self.filter_text) in str.lower(x)), self.original_data))

    def on_filter_text_change(self, e):
        self.filter_text = utils.transform_str_on_keyboard_input(self.text_box.get(), e.char)
        self.refine_list()
        self.populate_list()

    def get_selection(self):
        if len(self.list.curselection()) == 0:
            return None
        return self.data[self.list.curselection()[0]]

