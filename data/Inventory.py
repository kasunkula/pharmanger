import uuid

import defines
from defines import DataType
import sql_setup


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
        self.items_by_name = None

    def load_inventory(self):
        cursor = self.db_con.conn.cursor()
        statement = '''SELECT NAME, UNITS, SUPPLIER, CONTACT_NUMBER, EMAIL, ID FROM INVENTORY'''
        cursor.execute(statement)

        if self.items_by_name is not None:
            self.items_by_name.clear()
        else:
            self.items_by_name = {}

        records = cursor.fetchall()
        for record in records:
            self.items_by_name[record[defines.col_index_inventory_name]] = record
        cursor.close()

    def add_new_item(self, item):
        try:
            uid = uuid.uuid4()
            cur = self.db_con.cursor()
            new_item = [str(uid)]
            new_item.extend(item)
            print(new_item)
            cur.execute(sql_setup.insert_statement_inventory, new_item)
            self.db_con.commit()
            self.inventory_dirty_callback("AddInventoryItemWindow")
            return True
        except Exception as e:
            return False

    def add_stock(self, stock_update):
        None

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
