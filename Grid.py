from tkinter import *


class Grid:
    def __init__(self, parent, row, column, header, data=[]):
        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column, columnspan=2)

        self.header_frame = Frame(self.frame)
        self.header_frame.grid(sticky=W, row=0, column=0)

        for column in range(len(header)):
            cell = Entry(self.header_frame, width=20, font=('Arial', 16, 'bold'))
            cell.grid(row=0, column=column)
            cell.insert(END, header[column])

        self.data_rows_frame = Frame(self.frame)
        self.data_rows_frame.grid(sticky=W, row=1, column=0)
        self.original_data = data
        self.data = self.original_data
        self.render_data()

    def render_data(self):
        for item in self.data_rows_frame.winfo_children():
            item.destroy()

        for row_index in range(len(self.data)):
            for column_index in range(len(self.data[row_index])):
                cell = Entry(self.data_rows_frame, width=20, font=('Arial', 16, 'bold'))
                cell.grid(row=row_index, column=column_index)
                cell.insert(END, self.data[row_index][column_index])

    def update_data(self, new_data):
        self.data = new_data
        self.render_data()


class GridEx(Grid):
    def __init__(self, parent, row, column, header, data=[], filter_enabled_columns=[]):
        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column, columnspan=2)

        self.top_filters_frame = Frame(self.frame)
        self.top_filters_frame.grid(row=0, column=0, columnspan=2)

        self.grid_data_frame = Frame(self.frame)
        self.grid_data_frame.grid(row=1, column=0, columnspan=2)

        Grid.__init__(self, self.grid_data_frame, row, column, header, data)
        self.filter_enabled_counts = filter_enabled_columns
        self.filter_text = None

        row = 0
        for index in range(len(filter_enabled_columns)):
            if filter_enabled_columns[index]:
                label_text = "Filter by " + header[index]
                Label(self.top_filters_frame, text=label_text).grid(row=row, column=0)
                self.filter_text_box = Entry(self.top_filters_frame)
                self.filter_text_box.grid(row=row, column=1)
                self.filter_text_box.bind("<Key>", self.filter_text_update)

    def filter_text_update(self, e):
        self.filter_text = self.filter_text_box.get()
        if e.char == "\b":  # if backspace remove last character
            self.filter_text = self.filter_text[:len(self.filter_text) - 1]
        else:
            self.filter_text = self.filter_text + e.char
        self.filter_data()
        self.render_data()

    def filter_data(self):
        if self.filter_text is None or len(self.filter_text) == 0:
            self.data = self.original_data
            return

        self.data = \
            list(filter(lambda x:
                        (str.lower(self.filter_text) in str.lower(x[0])), self.original_data))
