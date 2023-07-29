import tkinter
from tkinter import *
import uuid
import tkinter.messagebox
import sql_setup
from components.Form import Form
from defines import DataType
from windows.Window import Window


class AddEntityInstance(Window):
    def __init__(self, parent, entity_name, inventory, db_con, inventory_dirty_callback):
        self.db_con = db_con
        self.inventory_dirty_callback = inventory_dirty_callback
        self.inventory = inventory
        self.entity_name = entity_name
        self.fields = [["Name", DataType.TEXT, True, True],  # ["Name", DataType, MustFill, Enabled]
                       ["SLMC Reg Number", DataType.TEXT, True, True],
                       ["Specialization", DataType.TEXT, True, True],
                       ["Description", DataType.TEXT, True, True]]
        Window.__init__(self, parent, "Add New " + entity_name)

    def render(self):
        self.form = Form(self.main_window, self.fields, "Add New " + self.entity_name,
                         submit_callback=self.on_add_new_item)

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
