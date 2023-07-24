from tkinter import *
from functools import partial
import utils


class Grid:
    def __init__(self, parent, row, column, header, data=[],
                 row_delete_enabled=False, on_row_delete=False,
                 row_expand=False, on_row_expand=None):
        self.row_delete_enabled = row_delete_enabled
        self.row_expand = row_expand
        self.header = header
        self.original_data = data
        self.data = self.original_data
        self.parent = parent
        self.on_row_expand = on_row_expand
        self.on_row_delete = on_row_delete

        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column, columnspan=2)

        self.header_frame = Frame(self.frame)
        self.header_frame.grid(sticky=W, row=0, column=0)

        for column in range(len(header)):
            cell = Entry(self.header_frame, width=20, font=('Arial', 16, 'bold'))
            cell.grid(row=0, column=column)
            cell.insert(END, header[column])
            cell.config(state="disabled")

        self.data_rows_frame = Frame(self.frame)
        self.data_rows_frame.grid(sticky=W, row=1, column=0)
        self.render_data()

    def render_data(self):
        for item in self.data_rows_frame.winfo_children():
            item.destroy()

        last_grid_column_index = 0
        for row_index in range(len(self.data)):
            for column_index in range(len(self.header)):
                cell = Entry(self.data_rows_frame, width=20, font=('Arial', 16, 'bold'))
                cell.insert(END, self.data[row_index][column_index])
                cell.config(state="disabled")
                cell.grid(row=row_index, column=column_index)
                last_grid_column_index = column_index
            if self.row_expand:
                last_grid_column_index += 1
                expand_row_button = Button(self.data_rows_frame, text="View", width=6,
                                           font=('Arial', 12),
                                           command=partial(self.on_expand_grid_entry, row_index))
                expand_row_button.grid(sticky=E, row=row_index, column=last_grid_column_index, pady=5, padx=5)

            if self.row_delete_enabled:
                last_grid_column_index += 1
                delete_row_button = Button(self.data_rows_frame, text="Remove", width=6,
                                           font=('Arial', 12),
                                           command=partial(self.on_delete_grid_entry, row_index))
                delete_row_button.grid(sticky=E, row=row_index, column=last_grid_column_index, pady=5, padx=5)

    def update_data(self, new_data):
        self.data = new_data
        self.render_data()

    def on_delete_grid_entry(self, row_index):
        self.data.pop(row_index)
        if self.on_row_delete is not None:
            self.on_row_delete(self.data[row_index])
        self.render_data()

    def on_expand_grid_entry(self, row_index):
        if self.on_row_expand is not None:
            self.on_row_expand(self.data[row_index])


class GridEx(Grid):
    def __init__(self, parent, row, column, header, data=[], filter_enabled_columns=[],
                 row_delete_enabled=False, on_row_delete=None,
                 row_expand_enabled=False, on_row_expand=None):
        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column, columnspan=2)

        self.top_filters_frame = Frame(self.frame)
        self.top_filters_frame.grid(row=0, column=0, columnspan=2, sticky=W)

        self.grid_data_frame = Frame(self.frame)
        self.grid_data_frame.grid(row=1, column=0, columnspan=2)

        Grid.__init__(self, self.grid_data_frame, row, column, header, data,
                      row_delete_enabled, on_row_delete,
                      row_expand_enabled, on_row_expand)
        self.filter_enabled_columns = filter_enabled_columns
        self.filter_texts = [None] * len(header)
        self.filter_text_boxes = [None] * len(header)

        row = 0
        for index in range(len(filter_enabled_columns)):
            if filter_enabled_columns[index]:
                label_text = "Filter by " + header[index]
                Label(self.top_filters_frame, text=label_text).grid(row=row, column=0, sticky=W)
                filter_text_box = Entry(self.top_filters_frame)
                filter_text_box.grid(row=row, column=1, sticky=W)
                filter_text_box.bind("<Key>", partial(self.filter_text_update, index))
                self.filter_text_boxes[index] = filter_text_box
                row += 1

    def filter_text_update(self, index, e):
        self.filter_texts[index] = utils.transform_str_on_keyboard_input(self.filter_text_boxes[index].get(), e.char)
        self.filter_data()
        self.render_data()

    def filter_data(self):
        self.data = self.original_data
        print("Grid Filter Data {}".format(self.filter_texts))
        for index in range(len(self.filter_texts)):
            if self.filter_texts[index] is None or len(self.filter_texts[index]) == 0:
                continue

            self.data = \
                list(filter(lambda x:
                            (str.lower(self.filter_texts[index]) in str.lower(x[index])), self.data))
