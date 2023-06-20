import os
from tkinter import *
import tkinter.messagebox
from tkinter.ttk import *
import sqlite3
import configparser
import uuid

import sql_setup
import utils
import billing
import InventoryWindow

col_index_inventory_name = 0
col_index_inventory_stock = 1
col_index_inventory_supplier = 2
col_index_inventory_number = 3
col_index_inventory_email = 4
col_index_inventory_id = 5

db_file_name = None
db_con = None
dashboard = tkinter.Tk()

inventory = {}
display_inventory_items = None

inventory_search_text_box = None
view_registry_window = None
registry_grid_frame = None

update_stock_window = None
billing_window = None
add_new_item_window = None

add_item_name = None
add_item_stock = None
add_item_supplier = None
add_item_contact_number = None
add_item_email = None
add_item_status_label = None

stock_update_name = None
stock_update_stock = None
stock_update_supplier = None
stock_update_unit_price = None
stock_update_total_amount = None
stock_update_status_label = None
stock_update_lookup = None
stock_update_display_list = []
stock_update_search_text = None


def render_inventory_grid():
    for item in registry_grid_frame.winfo_children():
        item.destroy()

    header_frame = Frame(registry_grid_frame)
    header_frame.grid(sticky=W, row=0, column=0)
    column_names = ['NAME', 'UNITS', 'SUPPLIER', 'CONTACT_NUMBER', 'EMAIL', 'ID']
    for column in range(len(column_names)):
        cell = Entry(header_frame, width=20, font=('Arial', 16, 'bold'))
        cell.grid(row=0, column=column)
        cell.insert(END, column_names[column])

    data_rows_frame = Frame(registry_grid_frame)
    data_rows_frame.grid(sticky=W, row=1, column=0)
    for row in range(len(display_inventory_items)):
        for column in range(len(display_inventory_items[row])):
            cell = Entry(data_rows_frame, width=20, font=('Arial', 16, 'bold'))
            cell.grid(row=row, column=column)
            cell.insert(END, display_inventory_items[row][column])


def search_text_update(e):
    global display_inventory_items

    display_inventory_items.clear()

    search_text = inventory_search_text_box.get()
    if e.char == "\b":  # if backspace remove last character
        search_text = search_text[:len(search_text) - 1]
    else:
        search_text = inventory_search_text_box.get() + e.char

    display_inventory_items = \
        list(filter(lambda x: (str.lower(search_text) in str.lower(
            x[col_index_inventory_name]) or search_text == "" or search_text is None),
                    inventory.values()))
    print(search_text)
    print(display_inventory_items)
    render_inventory_grid()


def render_view_registry_window():
    global view_registry_window, inventory_search_text_box, registry_grid_frame
    if view_registry_window is not None:
        view_registry_window.destroy()

    view_registry_window = InventoryWindow.InventoryWindow(dashboard, list(inventory.values()))
    return

    view_registry_window = tkinter.Toplevel(dashboard)
    view_registry_window.title("Registry")

    top_frame = Frame(view_registry_window)
    top_frame.grid(sticky=W, row=0, column=0)
    Label(top_frame, text="Current Inventory is as below").grid()

    body_frame = Frame(view_registry_window)
    body_frame.grid(sticky=W, row=1, column=0)

    filter_frame = Frame(body_frame, )
    filter_frame.grid(sticky=W, row=0)
    Label(filter_frame, text="Filter by Name").grid(row=0, column=0)
    inventory_search_text_box = Entry(filter_frame)
    inventory_search_text_box.grid(row=0, column=1)
    inventory_search_text_box.bind("<Key>", search_text_update)

    registry_grid_frame = Frame(body_frame)
    registry_grid_frame.grid(row=1)
    render_inventory_grid()


def search_by_name_on_stock_update(e):
    global stock_update_search_text, stock_update_name, update_stock_window
    stock_update_search_text = stock_update_name.get()
    if e.char == "\b":  # if backspace remove last character
        stock_update_search_text = stock_update_search_text[:len(stock_update_search_text) - 1]
    else:
        stock_update_search_text = stock_update_search_text + e.char
    refine_stock_update_display_list()
    render_stock_update_lookup(update_stock_window)


def refine_stock_update_display_list():
    global stock_update_display_list, stock_update_search_text

    if stock_update_search_text is None or len(stock_update_search_text) == 0:
        stock_update_display_list = list(inventory.values())
        return

    stock_update_display_list = \
        list(filter(lambda x:
                    (str.lower(stock_update_search_text) in str.lower(x[col_index_inventory_name])),
                    inventory.values()))
    print(stock_update_search_text)
    print(stock_update_display_list)


def render_stock_update_lookup(parent):
    global stock_update_lookup
    stock_update_lookup = Listbox(parent, width=40, selectmode=SINGLE)
    refine_stock_update_display_list()
    for index in range(len(stock_update_display_list)):
        stock_update_lookup.insert(index, stock_update_display_list[index][col_index_inventory_name])
    stock_update_lookup.grid(sticky=W, row=1, column=1, pady=5, padx=5)


def on_add_stock_update():
    global stock_update_name, stock_update_stock, stock_update_supplier, \
        stock_update_unit_price, stock_update_total_amount, stock_update_search_text

    stock = stock_update_stock.get()
    supplier = stock_update_supplier.get()
    unit_price = stock_update_unit_price.get()
    total_amount = stock_update_total_amount.get()
    status = ""
    if len(stock_update_lookup.curselection()) == 0:
        status = "Selected Name Invalid"
    elif stock is None or len(stock) == 0 or not stock.isnumeric() or (stock != str(int(stock))):
        status = "Specified Stock Invalid"
    elif supplier is None or len(supplier) == 0:
        status = "Specified Supplier Invalid"
    elif unit_price is None or len(unit_price) == 0 or not unit_price.isnumeric() or not utils.is_float(unit_price):
        status = "Specified Unit Price Invalid"
    elif total_amount is None or len(total_amount) == 0 or \
            not total_amount.isnumeric() or not utils.is_float(total_amount):
        status = "Specified Total Amount Invalid"
    else:
        selected_index = stock_update_lookup.curselection()[0]
        name = stock_update_display_list[selected_index][col_index_inventory_name]
        existing_stock = inventory[name][col_index_inventory_stock]
        new_stock = existing_stock + int(stock)
        uid = uuid.uuid4()
        global db_con
        cur = db_con.cursor()
        new_item = [str(uid), name, inventory[name][col_index_inventory_id], int(stock), supplier, float(unit_price), float(total_amount)]
        print(new_item)
        cur.execute(sql_setup.insert_statement_stock_update, new_item)
        cur.execute(sql_setup.update_statement_inventory, [new_stock, inventory[name][col_index_inventory_id]])
        db_con.commit()
        load_inventory(db_con)
        status = "Stock of [" + stock + "] Added to the inventory against [" + name + "] - current stock [" + str(new_stock) + "]"
        stock_update_status_label.config(text=status)

        stock_update_search_text = None
        refine_stock_update_display_list()
        render_update_stock_window()




def render_update_stock_window():
    global update_stock_window, stock_update_name, stock_update_stock, stock_update_supplier, \
        stock_update_unit_price, stock_update_total_amount, stock_update_status_label, stock_update_display_list

    if update_stock_window is not None:
        update_stock_window.destroy()

    update_stock_window = tkinter.Toplevel(dashboard)
    update_stock_window.title("Update Stock")

    Label(update_stock_window, text="Name", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=0, column=0,
                                                                                       pady=5, padx=5)
    stock_update_name = Entry(update_stock_window, width=40, font=('Arial', 16, 'bold'))
    stock_update_name.bind("<Key>", search_by_name_on_stock_update)
    stock_update_name.grid(sticky=W, row=0, column=1, pady=5, padx=5)
    render_stock_update_lookup(update_stock_window)

    Label(update_stock_window, text="Stock", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=2, column=0,
                                                                                        pady=5, padx=5)
    stock_update_stock = Entry(update_stock_window, width=40, font=('Arial', 16, 'bold'))
    stock_update_stock.grid(sticky=W, row=2, column=1, pady=5, padx=5)

    Label(update_stock_window, text="Supplier", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=3, column=0,
                                                                                           pady=5, padx=5)
    stock_update_supplier = Entry(update_stock_window, width=40, font=('Arial', 16, 'bold'))
    stock_update_supplier.grid(sticky=W, row=3, column=1, pady=5, padx=5)

    Label(update_stock_window, text="Unit Price", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=4,
                                                                                             column=0, pady=5,
                                                                                             padx=5)
    stock_update_unit_price = Entry(update_stock_window, width=40, font=('Arial', 16, 'bold'))
    stock_update_unit_price.grid(sticky=W, row=4, column=1, pady=5, padx=5)

    Label(update_stock_window, text="Total Amount", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=5,
                                                                                               column=0,
                                                                                               pady=5, padx=5)
    stock_update_total_amount = Entry(update_stock_window, width=40, font=('Arial', 16, 'bold'))
    stock_update_total_amount.grid(sticky=W, row=5, column=1, pady=5, padx=5)

    add_item_button = tkinter.Button(update_stock_window, text="Add Stock", width=20, font=('Arial', 16, 'bold'),
                                     command=on_add_stock_update)
    add_item_button.grid(sticky=E, row=6, column=0, pady=5, padx=5)

    stock_update_status_label = Label(update_stock_window, text="", font=('Arial', 14, 'bold'))
    stock_update_status_label.grid(sticky=W, row=7, column=0, pady=5, padx=10)


def render_billing_window():
    global billing_window

    if billing_window is not None:
        billing_window.destroy()

    billing_window = billing.BillWindow(dashboard, inventory.values())


def on_add_new_item():
    global add_item_name, add_item_stock, add_item_supplier, add_item_contact_number, add_item_email, add_item_status_label
    name = add_item_name.get()
    stock = add_item_stock.get()
    supplier = add_item_supplier.get()
    number = add_item_contact_number.get()
    email = add_item_email.get()
    status = ""
    if name is None or len(name) == 0:
        status = "Specified Name Invalid"
    elif name in inventory:
        status = "Inventory item with name [" + name + "] already exists"
    elif stock is None or len(stock) == 0 or not stock.isnumeric() or (stock != str(int(stock))):
        status = "Specified Stock Invalid"
    elif supplier is None or len(supplier) == 0:
        status = "Specified Supplier Invalid"
    elif number is None or len(number) == 0:
        status = "Specified Mobile Number Invalid"
    elif email is None or len(email) == 0:
        status = "Specified E-mail Invalid"
    else:
        status = "New Item Added to the inventory as [" + name + "] with initial stock of [" + stock + "]"
        uid = uuid.uuid4()
        global db_con
        cur = db_con.cursor()
        new_item = [str(uid), name, int(stock), supplier, number, email]
        print(new_item)
        cur.execute(sql_setup.insert_statement_inventory, new_item)
        db_con.commit()
        load_inventory(db_con)
    add_item_status_label.config(text=status)


def render_add_new_item_window():
    global add_new_item_window

    if add_new_item_window is not None:
        add_new_item_window.destroy()

    add_new_item_window = tkinter.Toplevel(dashboard)
    add_new_item_window.title("Add New Inventory Item")

    global add_item_name, add_item_stock, add_item_supplier, add_item_contact_number, add_item_email, add_item_status_label

    Label(add_new_item_window, text="Name", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=0, column=0,
                                                                                       pady=5, padx=5)
    add_item_name = Entry(add_new_item_window, width=40, font=('Arial', 16, 'bold'))
    add_item_name.grid(sticky=W, row=0, column=1, pady=5, padx=5)

    Label(add_new_item_window, text="Stock", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=1, column=0,
                                                                                        pady=5, padx=5)
    add_item_stock = Entry(add_new_item_window, width=40, font=('Arial', 16, 'bold'))
    add_item_stock.grid(sticky=W, row=1, column=1, pady=5, padx=5)

    Label(add_new_item_window, text="Supplier", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=2, column=0,
                                                                                           pady=5, padx=5)
    add_item_supplier = Entry(add_new_item_window, width=40, font=('Arial', 16, 'bold'))
    add_item_supplier.grid(sticky=W, row=2, column=1, pady=5, padx=5)

    Label(add_new_item_window, text="Contact Number", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=3,
                                                                                                 column=0, pady=5,
                                                                                                 padx=5)
    add_item_contact_number = Entry(add_new_item_window, width=40, font=('Arial', 16, 'bold'))
    add_item_contact_number.grid(sticky=W, row=3, column=1, pady=5, padx=5)

    Label(add_new_item_window, text="Email", width=20, font=('Arial', 16, 'bold')).grid(sticky=W, row=4, column=0,
                                                                                        pady=5, padx=5)
    add_item_email = Entry(add_new_item_window, width=40, font=('Arial', 16, 'bold'))
    add_item_email.grid(sticky=W, row=4, column=1, pady=5, padx=5)

    add_item_button = tkinter.Button(add_new_item_window, text="Add", width=20, font=('Arial', 16, 'bold'),
                                     command=on_add_new_item)
    add_item_button.grid(sticky=E, row=5, column=0, pady=5, padx=5)

    add_item_status_label = Label(add_new_item_window, text="", font=('Arial', 14, 'bold'))
    add_item_status_label.grid(sticky=W, row=6, column=0, pady=5, padx=10)


def load_inventory(conn):
    cursor = conn.cursor()
    query = 'select sqlite_version();'
    cursor.execute(query)
    result = cursor.fetchall()
    print('SQLite Version is {}'.format(result))

    cursor = conn.cursor()
    statement = '''SELECT NAME, UNITS, SUPPLIER, CONTACT_NUMBER, EMAIL, ID FROM INVENTORY'''
    cursor.execute(statement)

    global inventory, display_inventory_items

    records = cursor.fetchall()
    for record in records:
        inventory[record[col_index_inventory_name]] = record

    display_inventory_items = records.copy()
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
    button5 = tkinter.Button(right_column_frame, text='View Bills')

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
