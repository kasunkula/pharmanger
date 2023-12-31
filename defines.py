from enum import Enum

col_index_inventory_name = 0
col_index_inventory_stock = 1
col_index_inventory_cost = 2
col_index_inventory_alert = 3
col_index_inventory_critical_alert = 4
col_index_inventory_id = 5

col_index_bills_id = 4

col_index_bill_detail_bill_id = 4


class DataType(Enum):
    TEXT = 1
    INT = 2
    DOUBLE = 3
    SEARCH_BOX = 4
