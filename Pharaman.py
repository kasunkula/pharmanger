import os
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
import sqlite3
import configparser

import defines
import sql_setup
from AddInventoryItemWindow import AddInventoryItemWindow
from StockUpdateWindow import StockUpdateWindow
from BillingWindow import BillingWindow
from InventoryWindow import InventoryWindow
from ViewBillsWindow import ViewBillsWindow

db_file_name = None
db_con = None
dashboard = tkinter.Tk()

inventory = {}

inventory_window = None
update_stock_window = None
billing_window = None
add_new_item_window = None
view_bills_window = None

doctors = ["Upali Sirimanna", "Sunethra De Alwis", "Ama Sirimanna", "Amanda Sirimanna", "Himashi Sirimanna",
           "Yara Kulathilaka"]


def render_view_registry_window():
    global inventory_window
    if inventory_window is not None and not inventory_window.Closed():
        inventory_window.focus()
    else:
        inventory_window = InventoryWindow(dashboard, inventory)


def render_update_stock_window():
    global update_stock_window, db_con
    if update_stock_window is not None and not update_stock_window.Closed():
        update_stock_window.focus()
    else:
        update_stock_window = StockUpdateWindow(dashboard, inventory, db_con, inventory_dirty_callback)


def render_billing_window():
    global billing_window, db_con
    if billing_window is not None and not billing_window.Closed():
        billing_window.focus()
    else:
        billing_window = BillingWindow(dashboard, inventory, db_con, doctors)


def render_view_bills_window():
    global view_bills_window, db_con
    if view_bills_window is not None and not view_bills_window.Closed():
        view_bills_window.focus()
    else:
        view_bills_window = ViewBillsWindow(dashboard, db_con)


def render_add_new_item_window():
    global add_new_item_window, db_con

    if add_new_item_window is not None and not add_new_item_window.Closed():
        add_new_item_window.focus()
    else:
        add_new_item_window = AddInventoryItemWindow(dashboard, inventory, db_con, inventory_dirty_callback)


def inventory_dirty_callback(sender):
    print("Inventory Marked as Dirty by {}".format(sender))
    load_inventory(db_con)
    global inventory_window, update_stock_window, billing_window

    if inventory_window is not None:
        inventory_window.update_inventory(inventory)
    if update_stock_window is not None:
        update_stock_window.update_inventory(inventory)
    if billing_window is not None:
        update_stock_window.update_inventory(inventory)


def load_inventory(conn):
    cursor = conn.cursor()
    statement = '''SELECT NAME, UNITS, SUPPLIER, CONTACT_NUMBER, EMAIL, ID FROM INVENTORY'''
    cursor.execute(statement)

    global inventory

    if inventory is not None:
        inventory.clear()

    records = cursor.fetchall()
    for record in records:
        inventory[record[defines.col_index_inventory_name]] = record

    cursor.close()


def render_dashboard():
    global db_file_name, db_con
    config = configparser.ConfigParser()
    config.read('config.txt')
    db_file_name = config['DATABASE']['db_file_name']
    db_con = None
    if os.path.isfile(db_file_name):
        print("Database [{}] exists...".format(db_file_name))
        db_con = sqlite3.connect(db_file_name)
    else:
        print("Database [{}] does not exists.hence setting up with sample data".format(db_file_name))
        db_con = sqlite3.connect(db_file_name)
        sql_setup.drop_and_create_all_tables(db_con)

    load_inventory(db_con)
    print("Rendering DashBoard ...")

    dashboard.title('Dashboard')

    top_frame = Frame(dashboard)
    top_frame.grid(row=0, column=0)

    body_frame = Frame(dashboard)
    body_frame.grid(row=1)

    left_column_frame = Frame(body_frame, width=200, height=400)
    left_column_frame.grid(row=0, column=0, padx=10, pady=5)

    # Create left and right frames
    right_column_frame = Frame(body_frame, width=200, height=400)
    right_column_frame.grid(row=0, column=1, padx=10, pady=5)

    button1 = tkinter.Button(left_column_frame, text='View Registry', command=render_view_registry_window)
    button2 = tkinter.Button(left_column_frame, text='Update Stock', command=render_update_stock_window)
    button3 = tkinter.Button(left_column_frame, text='Add Registry Item', command=render_add_new_item_window)
    button4 = tkinter.Button(right_column_frame, text='Bill', command=render_billing_window)
    button5 = tkinter.Button(right_column_frame, text='View Bills', command=render_view_bills_window)

    button1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    button2.grid(row=1, column=0, padx=10, pady=5, sticky=W)
    button3.grid(row=2, column=0, padx=10, pady=5, sticky=W)
    button4.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    button5.grid(row=2, column=0, padx=10, pady=5, sticky=W)

    dashboard.mainloop()


if __name__ == "__main__":
    print("=======================================================")
    print("======================== START ========================")
    print("=======================================================")
    render_dashboard()
