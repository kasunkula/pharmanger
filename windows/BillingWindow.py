from datetime import datetime
import tkinter
import uuid
from tkinter import *
import tkinter.messagebox

# local
from components import SearchBox, Grid
import defines
import sql_setup
import utils
from windows.Window import Window


class BillingWindow(Window):
    def __init__(self, parent, inventory, db_con, doctors):
        self.inventory = inventory
        self.doctors = doctors
        self.db_con = db_con
        Window.__init__(self, parent, "Billing")

    def update_inventory(self, inventory):
        self.inventory = inventory
        self.render()

    def render(self):
        Window.render(self)
        self.top_frame = Frame(self.main_window, bd=10)
        self.top_frame.grid(row=0, column=0)

        self.doctor_name_search_box = SearchBox.SearchBox(self.top_frame, 0, 0, "දොස්තර", self.doctors)

        self.add_entry_frame = Frame(self.main_window, bd=10, highlightthickness=2, highlightbackground="black")
        self.add_entry_frame.grid(row=1, column=0, columnspan=2)
        Label(self.add_entry_frame, text="Add Bill Entries below").grid(row=0, column=0)

        self.name_search_box = SearchBox.SearchBox(self.add_entry_frame, 1, 0, "Name",
                                                   [item[defines.col_index_inventory_name] for item in
                                                    list(self.inventory.values())])

        self.label_issued_units = Label(self.add_entry_frame, text="Issued Units", width=20, font=('Arial', 16, 'bold'))
        self.label_issued_units.grid(sticky=W, row=2, column=0, pady=5, padx=5)
        self.issued_units = Entry(self.add_entry_frame, width=40, font=('Arial', 16, 'bold'))
        self.issued_units.grid(sticky=W, row=2, column=1, pady=5, padx=5)

        self.label_unit_price = Label(self.add_entry_frame, text="Unit Price", width=20, font=('Arial', 16, 'bold'))
        self.label_unit_price.grid(sticky=W, row=3, column=0, pady=5, padx=5)
        self.unit_price = Entry(self.add_entry_frame, width=40, font=('Arial', 16, 'bold'))
        self.unit_price.grid(sticky=W, row=3, column=1, pady=5, padx=5)

        self.add_item_to_bill_button = tkinter.Button(self.add_entry_frame, text="Add Item To Bill", width=20,
                                                      font=('Arial', 16, 'bold'),
                                                      command=self.on_add_bill_entry)
        self.add_item_to_bill_button.grid(sticky=E, row=5, column=1, pady=5, padx=5)

        self.bill_entries_frame = Frame(self.main_window, bd=10, highlightthickness=2, highlightbackground="black")
        self.bill_entries_frame.grid(row=3, column=0)
        Label(self.bill_entries_frame, text="Bill Entries").grid(row=0, column=0)

        self.bill_entries = []

        self.bill_entries_grid = Grid.Grid(self.bill_entries_frame, 1, 0,
                                           ["Item", "Units", "Unit Price", "Cost"], self.bill_entries,
                                           row_delete_enabled=True)

        self.add_bill_button = tkinter.Button(self.main_window, text="Add Bill", width=20,
                                              font=('Arial', 16, 'bold'),
                                              command=self.on_add_bill)
        self.add_bill_button.grid(sticky=E, row=4, column=0, pady=5, padx=5)

        self.status_label = Label(self.main_window, text="", font=('Arial', 14, 'bold'))
        self.status_label.grid(sticky=W, row=5, column=0, pady=5, padx=10)

    def on_add_bill_entry(self):
        print("on_add_bill_entry")
        status = None
        if self.name_search_box.get_selection() is None:
            status = "Item Selection invalid"
        elif len(self.issued_units.get()) == 0 or not utils.is_int(self.issued_units.get()):
            status = "Specified Issued Units invalid"
        elif len(self.unit_price.get()) == 0 or not utils.is_float(self.unit_price.get()):
            status = "Specified Unit Price invalid"
        else:
            new_entry = [self.name_search_box.get_selection(),
                         int(self.issued_units.get()),
                         float(self.unit_price.get()),
                         round(int(self.issued_units.get()) * float(self.unit_price.get()), 2)]
            self.bill_entries.append(new_entry)
            self.bill_entries_grid.update_data(self.bill_entries)
        if status is not None:
            tkinter.messagebox.showerror("Input Error", status)

    def on_add_bill(self):
        status = None
        if self.doctor_name_search_box.get_selection() is None:
            status = "Doctor Name Selection invalid"

        if status is not None:
            tkinter.messagebox.showerror("Input Error", status)
        else:
            bill_id = str(uuid.uuid4())
            total_cost = 0
            bill_entries = []
            for entry in self.bill_entries:
                total_cost += entry[3]
                item_id = self.inventory[entry[0]][defines.col_index_inventory_id]
                bill_entries.append([str(uuid.uuid4()), bill_id, item_id, entry[0], entry[1], entry[2], entry[3]])
            total_cost = round(total_cost, 2)
            now = datetime.now()
            date = now.strftime("%Y/%m/%d")
            time = now.strftime("%Y/%m/%d-%H:%M:%S")
            bill = [bill_id, date, time, self.doctor_name_search_box.get_selection(), total_cost]
            print(bill)
            print(bill_entries)

            cur = self.db_con.cursor()
            cur.execute(sql_setup.insert_statement_bill, bill)
            for bill_entry in bill_entries:
                cur.execute(sql_setup.insert_statement_bill_detail, bill_entry)
            self.db_con.commit()
            self.generate_bill()
            status = "Bill Successful with {} items totaling to Rs.{}".format(len(bill_entries), total_cost)
            tkinter.messagebox.showinfo("Billing Successful", status)


    def generate_bill(self):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hello, World!", ln=True)
        pdf.output("output.pdf", 'F')
        self.print_pdf_ex("output.pdf")

    def print_pdf_ex(self, file_name):
        import win32print, win32api
        try:
            win32api.ShellExecute(0, "printto", file_name,
                                  '"%s"' % win32print.GetDefaultPrinter(),
                                  ".", 0)
            print("PDF sent to print successfully.")
        except Exception as e:
            print(f"An error occurred while printing: {str(e)}")

    def print_pdf_working(self, file_name):
        import pathlib
        import printfactory
        import subprocess
        printer = printfactory.Printer()

        acrobat = r'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
        cmd = '"{}" /N /T "{}" "{}"'.format(acrobat, file_name, "Foxit Editor PDF Printer")

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        exit_code = proc.wait()
        print(exit_code)

    def print_pdf(self, file_name):
        import os
        os.startfile(file_name)

