import tkinter
import tkinter.messagebox
from components.Form import Form
from defines import DataType
from windows.Window import Window


class AddInventoryItemWindow(Window):
    def __init__(self, parent, inventory, db_con, inventory_dirty_callback):
        self.db_con = db_con
        self.inventory_dirty_callback = inventory_dirty_callback
        self.inventory = inventory
        self.form = None
        self.fields = [["Name", DataType.TEXT, True, True],
                       ["Stock", DataType.INT, True, True],
                       ["Cost", DataType.INT, True, True],
                       ["Cost", DataType.DOUBLE, True, True],
                       ["Stock Alert", DataType.INT, True, True],
                       ["Critical Stock Alert", DataType.INT, True, True]]
        Window.__init__(self, parent, "Add New Inventory Item")

    def render(self):
        self.form = Form(self.main_window, self.fields, "Add New Item", submit_callback=self.on_add_new_item)

    def on_add_new_item(self, item):
        if self.inventory.add_new_item(item):
            msg = "New Item Added to the inventory as [" + item[0] + "] with initial stock of [" + str(item[1]) + "]"
            tkinter.messagebox.showinfo("Item Add Successful", msg)
            self.form.render()
        else:
            msg = "Adding new item to inventory as [" + item[0] + "] failed. Please retry"
            tkinter.messagebox.showinfo("Item Add Unsuccessful", msg)
