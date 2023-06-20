import tkinter
from tkinter import *
import search_box
import Grid
import defines
import utils
import tkinter.messagebox
import Grid


class InventoryWindow:
    def __init__(self, parent, inventory):
        self.inventory = inventory
        self.inventory_window = tkinter.Toplevel(parent)
        self.inventory_window.title("Inventory")
        self.inventory_grid = Grid.GridEx(self.inventory_window, 0, 0,
                                          ['Name', 'Stock', 'Supplier', 'Contact Number', 'Email', 'UID'],
                                          self.inventory,
                                          [True, False, False, False, False, False])
