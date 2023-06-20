import tkinter
from tkinter import *
import search_box
import Grid
import defines
import utils
import tkinter.messagebox


class BillWindow:
    def __init__(self, parent, inventory):
        self.inventory = inventory
        self.billing_window = tkinter.Toplevel(parent)
        self.billing_window.title("Billing")

        self.top_frame = Frame(self.billing_window, bd=10)
        self.top_frame.grid(row=0, column=0)
        self.label_doctor_name = Label(self.top_frame, text="Doctor Name", width=20, font=('Arial', 16, 'bold'))
        self.label_doctor_name.grid(sticky=W, row=0, column=0, pady=5, padx=5)
        self.doctor = Entry(self.top_frame, width=40, font=('Arial', 16, 'bold'))
        self.doctor.grid(sticky=W, row=0, column=1, pady=5, padx=5)
        self.label_amount = Label(self.top_frame, text="Amount", width=20, font=('Arial', 16, 'bold'))
        self.label_amount.grid(sticky=W, row=1, column=0, pady=5, padx=5)
        self.amount = Entry(self.top_frame, width=40, font=('Arial', 16, 'bold'))
        self.amount.grid(sticky=W, row=1, column=1, pady=5, padx=5)

        self.add_entry_frame = Frame(self.billing_window, bd=10, highlightthickness=2, highlightbackground="black")
        self.add_entry_frame.grid(row=1, column=0, columnspan=2)
        Label(self.add_entry_frame, text="Add Bill Entries below").grid(row=0, column=0)

        self.name_search_box = search_box.SearchBox(self.add_entry_frame, 1, 0, "Name",
                                                    [item[defines.col_index_inventory_name] for item in self.inventory])

        self.label_issued_units = Label(self.add_entry_frame, text="Issued Units", width=20, font=('Arial', 16, 'bold'))
        self.label_issued_units.grid(sticky=W, row=2, column=0, pady=5, padx=5)
        self.issued_units = Entry(self.add_entry_frame, width=40, font=('Arial', 16, 'bold'))
        self.issued_units.grid(sticky=W, row=2, column=1, pady=5, padx=5)

        self.label_unit_price = Label(self.add_entry_frame, text="Unit Price", width=20, font=('Arial', 16, 'bold'))
        self.label_unit_price.grid(sticky=W, row=3, column=0, pady=5, padx=5)
        self.unit_price = Entry(self.add_entry_frame, width=40, font=('Arial', 16, 'bold'))
        self.unit_price.grid(sticky=W, row=3, column=1, pady=5, padx=5)

        self.label_total_amount = Label(self.add_entry_frame, text="Total Amount", width=20, font=('Arial', 16, 'bold'))
        self.label_total_amount.grid(sticky=W, row=4, column=0, pady=5, padx=5)
        self.total_amount = Entry(self.add_entry_frame, width=40, font=('Arial', 16, 'bold'))
        self.total_amount.grid(sticky=W, row=4, column=1, pady=5, padx=5)

        self.add_item_to_bill_button = tkinter.Button(self.add_entry_frame, text="Add Item To Bill", width=20,
                                                      font=('Arial', 16, 'bold'),
                                                      command=self.on_add_bill_entry)
        self.add_item_to_bill_button.grid(sticky=E, row=5, column=1, pady=5, padx=5)

        self.bill_entries_frame = Frame(self.billing_window, bd=10, highlightthickness=2, highlightbackground="black")
        self.bill_entries_frame.grid(row=3, column=0)
        Label(self.bill_entries_frame, text="Bill Entries").grid(row=0, column=0)

        self.bill_entries = []

        self.bill_entries_grid = Grid.Grid(self.bill_entries_frame, 1, 0,
                                           ["Item", "Units", "Unit Price", "Total Amount"], self.bill_entries)

        self.add_bill_button = tkinter.Button(self.billing_window, text="Add Bill", width=20,
                                              font=('Arial', 16, 'bold'),
                                              command=self.on_add_bill)
        self.add_bill_button.grid(sticky=E, row=4, column=0, pady=5, padx=5)

        self.status_label = Label(self.billing_window, text="", font=('Arial', 14, 'bold'))
        self.status_label.grid(sticky=W, row=5, column=0, pady=5, padx=10)

    def destroy(self):
        self.billing_window.destroy()

    def on_add_bill_entry(self):
        print("on_add_bill_entry")
        status = None
        if self.name_search_box.get_selection() is None:
            status = "Item Selection invalid"
        elif len(self.issued_units.get()) == 0 or not utils.is_int(self.issued_units.get()):
            status = "Specified Issued Units invalid"
        elif len(self.unit_price.get()) == 0 or not utils.is_float(self.unit_price.get()):
            status = "Specified Unit Price invalid"
        elif len(self.total_amount.get()) == 0 or not utils.is_float(self.total_amount.get()):
            status = "Specified Total Amount Invalid"
        else:
            new_entry = [self.name_search_box.get_selection(),
                         int(self.issued_units.get()),
                         float(self.unit_price.get()),
                         float(self.total_amount.get())]
            self.bill_entries.append(new_entry)
            self.bill_entries_grid.update_data(self.bill_entries)
        if status is not None:
            tkinter.messagebox.showerror("Input Error", status)

    def on_add_bill(self):
        print("Add Bill entry for {0}".format(self.name_search_box.get_selection()))
