from tkinter import *

import defines
from components import Grid
from windows.Window import Window


class ViewBillDetailsWindow(Window):
    def __init__(self, parent, bill_detail_entries):
        Window.__init__(self, parent, "View Bill Details")
        self.bills_grid = Grid.GridEx(self.main_window, 0, 0,
                                      ['Item', 'Unit Price', 'Issued Units', 'Amount'],
                                      bill_detail_entries,
                                      [True, False, False, False],
                                      False, False)


class ViewBillsWindow(Window):
    def __init__(self, parent, db_con):
        self.db_con = db_con
        Window.__init__(self, parent, "View Bills")

    def render(self):
        Window.render(self)
        self.load_bills_from_db()
        self.load_bill_entries_from_db()
        self.bills_grid = Grid.GridEx(self.main_window, 0, 0,
                                      ['Date', 'Time', 'Doctor Name', 'Amount', 'Id'],
                                      self.bills,
                                      [True, False, True, False, False, False],
                                      row_delete_enabled=False, on_row_delete=None,
                                      row_expand_enabled=True, on_row_expand=self.on_bill_expand)

    def load_bills_from_db(self):
        cursor = self.db_con.cursor()
        statement = '''SELECT DATE, DATETIME, DOCTOR, AMOUNT, ID FROM BILL ORDER BY DATETIME DESC'''
        cursor.execute(statement)
        self.bills = cursor.fetchall()
        cursor.close()

    def load_bill_entries_from_db(self):
        cursor = self.db_con.cursor()
        statement = '''SELECT  ITEM_NAME, UNIT_PRICE, UNITS, TOTAL_AMOUNT, BILL_ID, ITEM_ID FROM BILL_DETAIL'''
        cursor.execute(statement)
        bill_entries = cursor.fetchall()
        self.bill_entries_by_bill_id = {}
        for record in bill_entries:
            if record[defines.col_index_bill_detail_bill_id] not in self.bill_entries_by_bill_id:
                self.bill_entries_by_bill_id[record[defines.col_index_bill_detail_bill_id]] = []
            self.bill_entries_by_bill_id[record[defines.col_index_bill_detail_bill_id]].append(record)
        cursor.close()
        print(self.bill_entries_by_bill_id)

    def on_bill_expand(self, bill):
        bill_id = bill[defines.col_index_bills_id]
        bill_detail_entries = self.bill_entries_by_bill_id[bill_id]
        self.bill_details_window = ViewBillDetailsWindow(self.main_window, bill_detail_entries)

