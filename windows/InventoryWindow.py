from tkinter import *

from components import Grid
from windows.Window import Window


class InventoryWindow(Window):
    def __init__(self, parent, inventory):
        self.inventory = inventory
        Window.__init__(self, parent, "Inventory")


    def render(self):
        Window.render(self)
        self.inventory_grid = Grid.GridEx(self.main_window, 0, 0,
                                          ['Name', 'Stock', 'Supplier', 'Contact Number', 'Email', 'UID'],
                                          list(self.inventory.values()),
                                          [True, False, True, False, False, False])

    def update_inventory(self, inventory):
        self.inventory = inventory
        self.render()
