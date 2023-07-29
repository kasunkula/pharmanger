import os
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
import sqlite3
import configparser

import defines
import sql_setup
from data.Inventory import Inventory
from windows.AddEntityInstance import AddEntityInstance
from windows.AddInventoryItemWindow import AddInventoryItemWindow
from windows.StockUpdateWindow import StockUpdateWindow
from windows.BillingWindow import BillingWindow
from windows.InventoryWindow import InventoryWindow
from windows.ViewBillsWindow import ViewBillsWindow

db_file_name = None
db_con = None
dashboard = tkinter.Tk()

inventory = {}

inventory_window = None
update_stock_window = None
billing_window = None
add_new_item_window = None
add_new_doctor = None
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


def render_add_new_doctor():
    global add_new_doctor, db_con

    if add_new_doctor is not None and not add_new_doctor.Closed():
        add_new_doctor.focus()
    else:
        add_new_doctor = AddEntityInstance(dashboard, "Doctor", inventory, db_con, inventory_dirty_callback)


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
    statement = '''SELECT NAME, UNITS, ID FROM INVENTORY'''
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
    drop_tables_and_recreate = False if (
                str.lower(config['DATABASE']['drop_tables_and_recreate']) != str.lower('Yes')) else True
    config_sample_data = False if (str.lower(config['DATABASE']['config_sample_data']) != str.lower('Yes')) else True
    db_con = None

    # if sqllite DB does not exist create and create the tables
    if os.path.isfile(db_file_name):
        print("Database [{}] exists...".format(db_file_name))
        db_con = sqlite3.connect(db_file_name)
        if drop_tables_and_recreate:
            sql_setup.drop_tables(db_con)
            sql_setup.create_tables(db_con)
    else:
        print("Database [{}] does not exists.hence setting up with sample data".format(db_file_name))
        db_con = sqlite3.connect(db_file_name)
        sql_setup.create_tables(db_con)

    if config_sample_data:
        sql_setup.configure_sample_data(db_con)

    inventory = Inventory(db_con)
    load_inventory(db_con)

    dashboard.title('Dashboard')
    top_frame = Frame(dashboard)
    top_frame.grid(row=0, column=0)

    body_frame = Frame(dashboard)
    body_frame.grid(row=1)

    button1 = tkinter.Button(body_frame, text='View Registry', command=render_view_registry_window)
    button2 = tkinter.Button(body_frame, text='Update Stock', command=render_update_stock_window)
    button3 = tkinter.Button(body_frame, text='Add Registry Item', command=render_add_new_item_window)
    button4 = tkinter.Button(body_frame, text='Bill', command=render_billing_window)
    button5 = tkinter.Button(body_frame, text='View Bills', command=render_view_bills_window)
    button6 = tkinter.Button(body_frame, text='Add Doctor', command=render_add_new_doctor)

    button1.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    button2.grid(row=1, column=0, padx=10, pady=5, sticky=W)
    button3.grid(row=2, column=0, padx=10, pady=5, sticky=W)
    button4.grid(row=0, column=1, padx=10, pady=5, sticky=W)
    button5.grid(row=1, column=1, padx=10, pady=5, sticky=W)
    button6.grid(row=0, column=2, padx=10, pady=5, sticky=W)

    dashboard.mainloop()


if __name__ == "__main__":
    print("=======================================================")
    print("======================== START ========================")
    print("=======================================================")
    render_dashboard()
