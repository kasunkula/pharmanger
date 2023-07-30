from tkinter import *
import tkinter
import utils
from components.SearchBox import SearchBox
from components.TextInput import IntegerInput, TextInput, DoubleInput
from defines import DataType


class FormField:
    def __init__(self, field_name, data_type, must_fill=True, is_enabled=True, data=None):
        self.field_name = field_name
        self.data_type = data_type
        self.must_fill = must_fill
        self.is_enabled = is_enabled
        self.data = data


class Form:
    def __init__(self, parent, form_fields, submit_button_text, submit_callback=None, values_to_populate=None):
        self.parent = parent
        self.form_fields = form_fields
        self.submit_button_text = submit_button_text
        self.submit_callback = submit_callback
        self.values_to_populate = values_to_populate
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
        for index in range(len(self.form_fields)):
            field = self.form_fields[index]
            label = field[0]
            data_type = field[1]
            must_fill = field[2]
            enabled = field[3]
            if data_type is DataType.INT:
                text_box = IntegerInput(self.frame, index, 0, label, must_fill, enabled,
                                        value=self.values_to_populate[index] if self.values_to_populate is not None else None)
            elif data_type is DataType.DOUBLE:
                text_box = DoubleInput(self.frame, index, 0, label, must_fill, enabled,
                                       value=self.values_to_populate[index] if self.values_to_populate is not None else None)
            elif data_type is DataType.TEXT:
                text_box = TextInput(self.frame, index, 0, label, must_fill, enabled,
                                     value=self.values_to_populate[index] if self.values_to_populate is not None else None)
            elif data_type is DataType.SEARCH_BOX:
                names = field[4]
                text_box = SearchBox(self.frame, index, 0, label, names, must_fill)

            self.text_boxes.append(text_box)
            next_row = index + 1

        self.submit_button = tkinter.Button(self.frame, text=self.submit_button_text, width=20,
                                            font=('Arial', 16, 'bold'),
                                            command=self.on_submit)

        self.submit_button.grid(sticky=E, row=next_row, column=1, pady=5, padx=0)

    def on_submit(self):
        submitted_values = []
        for text_box in self.text_boxes:
            ok, reason = text_box.finalize()
            if not ok:
                tkinter.messagebox.showerror("Input Error", reason)
                return
            submitted_values.append(text_box.get())

        if self.submit_callback is not None:
            self.submit_callback(submitted_values)
