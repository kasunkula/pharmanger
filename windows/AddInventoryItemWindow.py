import tkinter
from tkinter import *
import uuid
import tkinter.messagebox
import sql_setup
from components.Form import Form
from defines import DataType
from windows.Window import Window


class AddInventoryItemWindow(Window):
    def __init__(self, parent, inventory, db_con, inventory_dirty_callback):
        self.db_con = db_con
        self.inventory_dirty_callback = inventory_dirty_callback
        self.inventory = inventory
        Window.__init__(self, parent, "Add New Inventory Item")

    def render(self):
        self.fields = [["Name", DataType.TEXT, True, True],
                       ["Stock", DataType.INT, True, True],
                       ["Supplier", DataType.TEXT, True, True],
                       ["Contact Number", DataType.TEXT, True, True],
                       ["Email", DataType.TEXT, True, True],
                       ]
        self.form = Form(self.main_window, self.fields, "Add New Item", submit_callback=self.on_add_new_item)

    def render_ex(self):
        Window.render(self)
        Label(self.main_window, text="Name", width=20, font=('Arial', 16, 'bold')).grid(sticky=W,
                                                                                        row=0,
                                                                                        column=0,
                                                                                        pady=5,
                                                                                        padx=5)
        self.add_item_name = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.add_item_name.grid(sticky=W, row=0, column=1, pady=5, padx=5)

        Label(self.main_window, text="Stock", width=20, font=('Arial', 16, 'bold')).grid(sticky=W,
                                                                                         row=1,
                                                                                         column=0,
                                                                                         pady=5,
                                                                                         padx=5)
        self.add_item_stock = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.add_item_stock.grid(sticky=W, row=1, column=1, pady=5, padx=5)

        Label(self.main_window, text="Supplier", width=20, font=('Arial', 16, 'bold')).grid(sticky=W,
                                                                                            row=2,
                                                                                            column=0,
                                                                                            pady=5,
                                                                                            padx=5)
        self.add_item_supplier = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.add_item_supplier.grid(sticky=W, row=2, column=1, pady=5, padx=5)

        Label(self.main_window, text="Contact Number", width=20, font=('Arial', 16, 'bold')).grid(
            sticky=W, row=3,
            column=0, pady=5,
            padx=5)
        self.add_item_contact_number = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.add_item_contact_number.grid(sticky=W, row=3, column=1, pady=5, padx=5)

        Label(self.main_window, text="Email", width=20, font=('Arial', 16, 'bold')).grid(sticky=W,
                                                                                         row=4,
                                                                                         column=0,
                                                                                         pady=5,
                                                                                         padx=5)
        self.add_item_email = Entry(self.main_window, width=40, font=('Arial', 16, 'bold'))
        self.add_item_email.grid(sticky=W, row=4, column=1, pady=5, padx=5)

        self.add_item_button = tkinter.Button(self.main_window, text="Add", width=20,
                                              font=('Arial', 16, 'bold'),
                                              command=self.on_add_new_item)
        self.add_item_button.grid(sticky=E, row=5, column=0, pady=5, padx=5)

    def on_add_new_item_ex(self):
        name = self.add_item_name.get()
        stock = self.add_item_stock.get()
        supplier = self.add_item_supplier.get()
        number = self.add_item_contact_number.get()
        email = self.add_item_email.get()
        status = None
        if name is None or len(name) == 0:
            status = "Specified Name Invalid"
        elif name in self.inventory:
            status = "Inventory item with name [" + name + "] already exists"
        elif stock is None or len(stock) == 0 or not stock.isnumeric() or (stock != str(int(stock))):
            status = "Specified Stock Invalid"
        elif supplier is None or len(supplier) == 0:
            status = "Specified Supplier Invalid"
        elif number is None or len(number) == 0:
            status = "Specified Mobile Number Invalid"
        elif email is None or len(email) == 0:
            status = "Specified E-mail Invalid"

        if status is not None:
            tkinter.messagebox.showerror("Data Input Error", status)
        else:
            uid = uuid.uuid4()
            cur = self.db_con.cursor()
            new_item = [str(uid), name, int(stock), supplier, number, email]
            print(new_item)
            cur.execute(sql_setup.insert_statement_inventory, new_item)
            self.db_con.commit()
            status = "New Item Added to the inventory as [" + name + "] with initial stock of [" + stock + "]"
            tkinter.messagebox.showinfo("Item Add Successful", status)
            self.inventory_dirty_callback("AddInventoryItemWindow")

    def on_add_new_item(self, item):
        uid = uuid.uuid4()
        cur = self.db_con.cursor()
        new_item = [str(uid)]
        new_item.extend(item)
        print(new_item)
        cur.execute(sql_setup.insert_statement_inventory, new_item)
        self.db_con.commit()
        self.inventory_dirty_callback("AddInventoryItemWindow")
        msg = "New Item Added to the inventory as [" + item[0] + "] with initial stock of [" + str(item[1]) + "]"
        tkinter.messagebox.showinfo("Item Add Successful", msg)
        self.form.render()
