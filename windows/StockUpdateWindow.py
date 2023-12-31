import tkinter
from tkinter import *
import uuid
import tkinter.messagebox

import db_schema
import defines
from components import SearchBox
import utils
from components.Form import Form
from windows.Window import Window
from defines import DataType


class StockUpdateWindow(Window):
    def __init__(self, parent, inventory, db_con, inventory_dirty_callback):
        self.inventory = inventory
        self.db_con = db_con
        self.inventory_dirty_callback = inventory_dirty_callback
        self.fields = [["Name", DataType.SEARCH_BOX, True, None, self.inventory.get_item_names()],
                       ["Stock", DataType.INT, True, True],
                       ["Cost", DataType.TEXT, True, True]]
        self.form = None
        Window.__init__(self, parent, "Update Stock")

    def update_inventory(self, inventory):
        self.inventory = inventory
        self.render()

    def render(self):
        self.form = Form(self.main_window, self.fields, "Add New Stock", submit_callback=self.on_add_stock_update)
        # self.render_ex()

    def render_ex(self):
        Window.render(self)
        self.name_search_box = SearchBox.SearchBox(self.main_window, 1, 0, "Name", self.inventory.get_item_names())
        Label(self.main_window, text="Stock", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=2,
                                                                                         column=0,
                                                                                         pady=5, padx=0)
        self.stock_update_stock = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.stock_update_stock.grid(sticky=W, row=2, column=1, pady=5, padx=0)

        Label(self.main_window, text="Unit Price", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=4,
                                                                                              column=0, pady=5,
                                                                                              padx=0)
        self.stock_update_unit_price = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.stock_update_unit_price.grid(sticky=W, row=4, column=1, pady=5, padx=0)

        Label(self.main_window, text="Total Amount", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=5,
                                                                                                column=0,
                                                                                                pady=5, padx=0)
        self.stock_update_total_amount = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.stock_update_total_amount.grid(sticky=W, row=5, column=1, pady=5, padx=0)

        add_stock_button = tkinter.Button(self.main_window, text="Add Stock", width=20,
                                          font=('Arial', 16, 'bold'),
                                          command=self.on_add_stock_update)
        add_stock_button.grid(sticky=E, row=6, column=1, pady=5, padx=0)

        self.stock_update_status_label = Label(self.main_window, text="", font=('Arial', 14, 'bold'))
        self.stock_update_status_label.grid(sticky=W, row=7, column=0, pady=5, padx=0)

    def on_add_stock_update(self, item):
        self.inventory.add_stock(item)


    def on_add_stock_update_ex(self):
        stock = self.stock_update_stock.get()
        unit_price = self.stock_update_unit_price.get()
        total_amount = self.stock_update_total_amount.get()
        status = None

        if self.name_search_box.get_selection() is None:
            status = "Item Selection invalid"
        elif stock is None or len(stock) == 0 or not utils.is_int(stock):
            status = "Specified Stock Invalid"
        elif unit_price is None or len(unit_price) == 0 or not utils.is_float(unit_price):
            status = "Specified Unit Price Invalid"
        elif total_amount is None or len(total_amount) == 0 or \
                not total_amount.isnumeric() or not utils.is_float(total_amount):
            status = "Specified Total Amount Invalid"

        if status is not None:
            tkinter.messagebox.showerror("Data Input Error", status)
        else:
            inventory_item_name = self.name_search_box.get_selection()
            inventory_item_id = self.inventory[inventory_item_name][defines.col_index_inventory_id]
            existing_stock = self.inventory[inventory_item_name][defines.col_index_inventory_stock]
            new_stock = existing_stock + int(stock)

            status = "Stock of [" + stock + "] Added to the inventory against [" + inventory_item_name + "] - updated stock [" + str(
                new_stock) + "]"
            tkinter.messagebox.showinfo("Item Add Successful", status)
            self.inventory_dirty_callback("StockUpdateWindow")
