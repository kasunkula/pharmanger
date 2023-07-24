from tkinter import *
import tkinter
import utils


class TextInput:
    def __init__(self, parent, row, column, label_name, must_fill=True, enabled=True, value=None):
        self.enabled = enabled
        self.must_fill = must_fill
        self.label_name = label_name

        self.label = Label(parent, text=label_name, font=('Arial', 16, 'bold'))
        self.label.grid(sticky=W, row=row, column=column, pady=5, padx=0)

        self.text_box = Entry(parent, width=40, font=('Arial', 16, 'bold'))
        self.text_box.grid(sticky=W, row=row, column=column + 1, pady=5, padx=0)
        self.text_box.bind("<Key>", self.on_key_input)
        if value is not None:
            self.text_box.insert(END, value)
        if not enabled:
            self.text_box.config(state="disabled")

    def get(self):
        return self.text_box.get()

    def clear_text(self):
        self.text_box.delete(0, END)

    def on_key_input(self, e):
        None

    def is_empty(self):
        return len(self.text_box.get()) == 0

    def finalize(self):
        if self.must_fill and self.is_empty():
            return False, self.label_name + " can not be empty"
        return True, None


class IntegerInput(TextInput):
    def on_key_input(self, e):
        text = utils.transform_str_on_keyboard_input(self.text_box.get(), e.char)
        if not utils.is_int(text):
            tkinter.messagebox.showerror("Input Error", self.label_name + " must be a Number")

    def finalize(self):
        if not self.is_empty() and not utils.is_int(self.text_box.get()):
            return False, self.label_name + " must be a Integer"
        return TextInput.finalize(self)

    def get(self):
        return int(self.text_box.get())


class DoubleInput(TextInput):
    def on_key_input(self, e):
        text = utils.transform_str_on_keyboard_input(self.text_box.get(), e.char)
        if not utils.is_float(text):
            tkinter.messagebox.showerror("Input Error", self.label_name + " must be a Float")

    def finalize(self):
        if not self.is_empty() and not utils.is_float(self.text_box.get()):
            return False, self.label_name + " must be a Float"
        return TextInput.finalize(self)

    def get(self):
        return float(self.text_box.get())
