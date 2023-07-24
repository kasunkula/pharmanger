from tkinter import *
import tkinter
import utils
from components.TextInput import IntegerInput, TextInput, DoubleInput
from defines import DataType


class Form:
    def __init__(self, parent, items, button_text, submit_callback=None, values=None):
        self.parent = parent
        self.items = items
        self.button_text = button_text
        self.submit_callback = submit_callback
        self.values = values
        self.frame = None
        self.render()

    def render(self):
        if self.frame is None:
            self.frame = Frame(self.parent)
            self.frame.grid()
        else:
            for item in self.frame.winfo_children():
                item.destroy()
        self.text_boxes = []

        next_row = None
        for index in range(len(self.items)):
            field = self.items[index]
            if field[1] is DataType.INT:
                text_box = IntegerInput(self.frame, index, 0, field[0], must_fill=field[2], enabled=field[3],
                                        value=self.values[index] if self.values is not None else None)
            if field[1] is DataType.DOUBLE:
                text_box = DoubleInput(self.frame, index, 0, field[0], must_fill=field[2], enabled=field[3],
                                       value=self.values[index] if self.values is not None else None)
            if field[1] is DataType.TEXT:
                text_box = TextInput(self.frame, index, 0, field[0], must_fill=field[2], enabled=field[3],
                                     value=self.values[index] if self.values is not None else None)
            self.text_boxes.append(text_box)
            next_row = index + 1

        self.submit_button = tkinter.Button(self.frame, text=self.button_text, width=20,
                                            font=('Arial', 16, 'bold'),
                                            command=self.on_submit)

        self.submit_button.grid(sticky=E, row=next_row, column=1, pady=5, padx=5)

    def on_submit(self):
        print("OnSubmit Click")
        submitted_values = []
        for text_box in self.text_boxes:
            ok, reason = text_box.finalize()
            if not ok:
                tkinter.messagebox.showerror("Input Error", reason)
                return
            submitted_values.append(text_box.get())

        if self.submit_callback is not None:
            self.submit_callback(submitted_values)
