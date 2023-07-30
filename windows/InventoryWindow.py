from tkinter import *

from components import Grid
from data.Inventory import InventoryObserver
from windows.Window import Window


class InventoryWindow(Window, InventoryObserver):
    def __init__(self, parent, inventory):
        self.inventory = inventory
        self.inventory.observe(self)
        self.inventory_grid = None
        Window.__init__(self, parent, "Inventory")

    def render(self):
        Window.render(self)
        self.inventory_grid = Grid.GridEx(self.main_window, 0, 0,
                                          ['Name', 'Stock'],
                                          self.inventory.get_items(),
                                          [True, False])

    def onInventoryUpdate(self, inventory):
        self.inventory = inventory
        self.render()
