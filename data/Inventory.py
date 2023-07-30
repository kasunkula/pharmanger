import uuid

import defines
from defines import DataType
import db_schema
from abc import ABC, abstractmethod


class InventoryObserver(ABC):
    @abstractmethod
    def onInventoryUpdate(self):
        pass


class EntityDef:
    def __init__(self):
        self.name = None
        self.db_table = None
        self.primary_key_fields = None
        self.fields = []
        self.field_displayNames = []
        self.insert_statement = None
        self.update_statement = None
        self.load_up_query = None


class DoctorDef(EntityDef):
    def __init__(self):
        self.name = "Medical Professional"
        self.db_table = 'MEDICAL_PROFESSIONAL'
        self.primary_key_fields = ['Id', 'Name', 'Registration Number']
        self.fields = []
        self.field_displayNames = []
        self.insert_statement = None
        self.update_statement = None
        self.load_up_query = None
        EntityDef.__init__(self, "Medical Professional", 'MEDICAL_PROFESSIONAL', ['ID', 'NAME', 'REGISTRATION_NUMBER'])
        self.fields = [["Id", DataType.TEXT, True, True, False],
                       ["Name", DataType.TEXT, True, True, True],
                       ["Registration Number", DataType.TEXT, True, True, True],
                       ["Speciality", DataType.TEXT, True, True, True],
                       ["Description", DataType.INT, True, True, True]]
        self.uid = None
        self.name = None
        self.registration_number = None
        self.designation = None


class Inventory:
    def __init__(self, db_con):
        self.db_con = db_con
        self.items_by_name = {}
        self.items_by_id = {}
        self.item_names = []
        self.items = []
        self.observers = []
        self.load_inventory()

    def load_inventory(self):
        cursor = self.db_con.cursor()
        statement = '''SELECT NAME, UNITS, AVG_PRICE, COST, ALERT, CRITICAL_ALERT, ID FROM INVENTORY'''
        cursor.execute(statement)

        self.items_by_name.clear()
        self.items_by_id.clear()
        self.item_names.clear()
        self.items.clear()

        records = cursor.fetchall()
        for record in records:
            self.add_item(record)
        cursor.close()
        self.on_change()

    def observe(self, observer):
        self.observers.append(observer)

    def add_item(self, item):
        self.items_by_name[item[defines.col_index_inventory_name]] = item
        self.items_by_id[item[defines.col_index_inventory_id]] = item
        self.item_names.append(item[defines.col_index_inventory_name])
        self.items.append(item)
        print(item)
        self.on_change()

    def on_change(self):
        self.item_names.sort()
        self.items.sort(key=lambda x: x[defines.col_index_inventory_name])
        for observer in self.observers:
            observer.onInventoryUpdate(self)

    def get_item_names(self):
        return self.item_names

    def get_items(self):
        return self.items

    def add_new_item(self, item):
        try:
            uid = uuid.uuid4()
            cur = self.db_con.cursor()
            item.append(str(uid))
            self.add_item(item)
            cur.execute(db_schema.insert_statement_inventory, item)
            self.db_con.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            return False

    def add_stock(self, stock_update):
        # Name, Stock, Cost
        name, new_stock, new_cost = stock_update
        current_snapshot = self.items_by_name[name]
        item_id = current_snapshot[defines.col_index_inventory_id]
        existing_stock = current_snapshot[defines.col_index_inventory_stock]
        existing_cost = current_snapshot[defines.col_index_inventory_cost]

        cur = self.db_con.cursor()
        stock_update.append(str(uuid.uuid4()))
        stock_update.append(current_snapshot[defines.col_index_inventory_id])
        print(stock_update)
        cur.execute(db_schema.insert_statement_stock_update, stock_update)
        self.db_con.commit()
        cur.close()

        if existing_cost is None:
            existing_cost = 0.0

        stock = existing_stock + new_stock
        cost = round(existing_cost + new_cost, 2)
        avg_price = round(cost / stock, 2)

        cur = self.db_con.cursor()
        cur.execute(db_schema.update_statement_inventory, [stock, avg_price, cost, item_id])
        self.db_con.commit()
        cur.close()

    def add_bill(self, bill):
        None


class Item:
    def __init__(self):
        self.uid = None
        self.name = None
        self.stock = None
        self.supplier = None


class Bill:
    def __init__(self):
        self.uid = None
        self.doctor = None
        self.amount = None
        self.bill_entries = []


class BillEntry:
    def __init__(self):
        self.uid = None
        self.item_uid = None
        self.item_name = None
        self.issued_units = None
        self.unit_price = None
        self.amount = None


class Doctor():
    def __init__(self, entity_def):
        self.entity_def = entity_def
        EntityDef.__init__("Medical Professional", 'MEDICAL_PROFESSIONALS', ['ID', 'NAME', 'REGISTRATION_NUMBER'])
        self.fields = [["Id", DataType.TEXT, True, True, False],
                       ["Name", DataType.TEXT, True, True, True],
                       ["Registration Number", DataType.TEXT, True, True, True],
                       ["Speciality", DataType.TEXT, True, True, True],
                       ["Description", DataType.INT, True, True, True]]
        self.uid = None
        self.name = None
        self.registration_number = None
        self.designation = None


class Supplier:
    def __init__(self):
        self.uid = None
        self.name = None
        self.company = None
        self.contact_number = None
        self.email = None
