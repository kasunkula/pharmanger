from tkinter import *

import Grid
from Window import Window


class ViewBillsWindow(Window):
    def __init__(self, parent, db_con):
        self.db_con = db_con
        Window.__init__(self, parent, "View Bills")


    def render(self):
        Window.render(self)
        self.load_bills_from_db()
        self.inventory_grid = Grid.GridEx(self.main_window, 0, 0,
                                          ['Date', 'Time', 'Doctor Name', 'Amount', 'Id'],
                                          self.bills,
                                          [True, False, True, False, False, False])


    def load_bills_from_db(self):
        cursor = self.db_con.cursor()
        statement = '''SELECT DATE, DATETIME, DOCTOR, AMOUNT, ID FROM BILL ORDER BY DATETIME DESC'''
        cursor.execute(statement)
        self.bills = cursor.fetchall()
        cursor.close()
