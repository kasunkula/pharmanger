create_table_inventory = '''CREATE TABLE INVENTORY
                            (ID            TEXT    NOT NULL,
                            NAME            TEXT    NOT NULL PRIMARY KEY,
                            UNITS            INT    NOT NULL,
                            SUPPLIER        TEXT    NOT NULL,
                            CONTACT_NUMBER    TEXT    NOT NULL,
                            EMAIL            TEXT    NOT NULL)'''

insert_statement_inventory = '''INSERT INTO INVENTORY(ID,NAME,UNITS,SUPPLIER,CONTACT_NUMBER,EMAIL) 
                                VALUES (?,?,?,?,?,?) '''
update_statement_inventory = '''UPDATE INVENTORY SET UNITS = ? WHERE ID = ?'''

create_table_stock_update = ''' CREATE TABLE STOCK_UPDATE
                                (ID            TEXT    NOT NULL PRIMARY KEY,
                                ITEM_NAME        TEXT        NOT NULL,
                                ITEM_ID        TEXT        NOT NULL,
                                UNITS          INT     NOT NULL,
                                SUPPLIER       TEXT    NOT NULL,
                                UNIT_PRICE    REAL    NOT NULL,
                                TOTAL_AMOUNT   REAL    NOT NULL)'''

insert_statement_stock_update = ''' INSERT INTO STOCK_UPDATE(ID, ITEM_NAME, ITEM_ID, UNITS, SUPPLIER, UNIT_PRICE, TOTAL_AMOUNT) 
                                    VALUES (?,?,?,?,?,?,?) '''

create_table_bill = ''' CREATE TABLE BILL
                        (ID            TEXT    NOT NULL PRIMARY KEY,
                        DATE            TEXT    NOT NULL,
                        DATETIME       TEXT    NOT NULL,
                        DOCTOR        TEXT    NOT NULL,
                        AMOUNT        REAL    NOT NULL)'''

insert_statement_bill = '''INSERT INTO BILL(ID, DATE, DATETIME, DOCTOR, AMOUNT) VALUES (?,?,?,?,?) '''

create_table_bill_detail = '''  CREATE TABLE BILL_DETAIL
                                (ID            INT    NOT NULL PRIMARY KEY,
                                BILL_ID        TEXT    NOT NULL,
                                ITEM_ID        TEXT    NOT NULL,
                                ITEM_NAME        TEXT        NOT NULL,
                                UNITS        INT    NOT NULL,
                                UNIT_PRICE     REAL    NOT NULL,
                                TOTAL_AMOUNT    REAL    NOT NULL)'''

insert_statement_bill_detail = '''  INSERT INTO BILL_DETAIL(ID, BILL_ID, ITEM_ID, ITEM_NAME, UNITS, UNIT_PRICE, 
                                    TOTAL_AMOUNT) 
                                    VALUES (?,?,?,?,?,?,?) '''

inventory = [['39dd566c-134d-4285-bd23-b091f3346f36', 'Aspirin', 20, 'ABC Pharma', '1234567890', 'abc@example.com'],
             ['cd28faf7-d03c-438a-8a5f-25b7a58bf741', 'Paracetamol', 30, 'XYZ Medical Supplies', '987654321', 'xyz@example.com'],
             ['4f1a0b69-6b62-42e0-9b5d-dedb70de82c9', 'Amoxicillin', 7, 'PharmaCorp', '1122334455', 'info@pharmacorp.com'],
             ['72359153-61b6-43f3-b63e-48334cdac781', 'Lisinopril', 30, 'MediMart', '9876543210', 'info@medimart.com'],
             ['174ca177-f3f5-427e-84f6-a4f182fa992b', 'Insulin', 10, 'HealthCare Solutions', '5566778899', 'contact@healthcaresolutions.com']]

stock_updates = [['f1781e88-96e4-4c1b-8197-1578e4d55c89', 'Aspirin', '39dd566c-134d-4285-bd23-b091f3346f36', 20, 'ABC Pharma', 6.5, 130],
                 ['f34b68b5-dadf-4c6b-9d7a-123456789012', 'Aspirin', '39dd566c-134d-4285-bd23-b091f3346f36', 10, 'ABC Pharma', 7.0, 70],
                 ['a7f41f0a-786b-4c3d-89fd-987654321098', 'Paracetamol', 'cd28faf7-d03c-438a-8a5f-25b7a58bf741', 30, 'XYZ Medical Supplies', 12.0,
                  360],
                 ['d4e2f4b2-10a7-4b3c-8d7e-901234567890', 'Paracetamol', 'cd28faf7-d03c-438a-8a5f-25b7a58bf741', 20, 'XYZ Medical Supplies', 15, 300],
                 ['c8d9e0f1-2103-4b5c-6d7e-987654321012', 'Amoxicillin', '4f1a0b69-6b62-42e0-9b5d-dedb70de82c9', 5, 'PharmaCorp', 1.0, 5],
                 ['f0e1d2c3-9087-4b6c-2d4e-765432109876', 'Amoxicillin', '4f1a0b69-6b62-42e0-9b5d-dedb70de82c9', 8, 'PharmaCorp', 2.0, 16],
                 ['b3c4d5e6-4567-4c8d-1e2f-543210987654', 'Lisinopril', '72359153-61b6-43f3-b63e-48334cdac781', 12, 'MediMart', 1.50, 18.0],
                 ['a2b3c4d5-6789-4c0d-3e4f-432109876543', 'Lisinopril', '72359153-61b6-43f3-b63e-48334cdac781', 18, 'MediMart', 1.0, 18],
                 ['d1e2f3a4-3456-4b7c-8d9e-321098765432', 'Insulin', '174ca177-f3f5-427e-84f6-a4f182fa992b', 5, 'HealthCare Solutions', 110, 550],
                 ['b4c5d6e7-9876-4c3d-2e1f-210987654321', 'Insulin', '174ca177-f3f5-427e-84f6-a4f182fa992b', 5, 'HealthCare Solutions', 100.0, 500]]

bills = [['c413a6f6-125c-4e80-9f14-345678901234', '2023/06/18', '9:00:00', 'Dr. Smith', 167.50],
         ['e4f5a6b7-9876-4c5d-6e7f-543210987654', '2023/06/19', '14:30:00', 'Dr. Johnson', 95.50],
         ['d7e8f9a0-0123-4b5c-6d7e-890123456789', '2023/06/20', '11:45:00', 'Dr. Williams', 105.50]]

bill_details = [[1, 'c413a6f6-125c-4e80-9f14-345678901234', '39dd566c-134d-4285-bd23-b091f3346f36', 'Aspirin', 5, 8, 40.0],
                [2, 'c413a6f6-125c-4e80-9f14-345678901234', 'cd28faf7-d03c-438a-8a5f-25b7a58bf741', 'Paracetamol', 10, 12, 120.0],
                [3, 'c413a6f6-125c-4e80-9f14-345678901234', '4f1a0b69-6b62-42e0-9b5d-dedb70de82c9', 'Amoxicillin', 3, 3.50, 7.50],
                [4, 'e4f5a6b7-9876-4c5d-6e7f-543210987654', '39dd566c-134d-4285-bd23-b091f3346f36', 'Aspirin', '2', 8, 20],
                [5, 'e4f5a6b7-9876-4c5d-6e7f-543210987654', 'cd28faf7-d03c-438a-8a5f-25b7a58bf741', 'Paracetamol', 4, 13, 72.0],
                [6, 'e4f5a6b7-9876-4c5d-6e7f-543210987654', '4f1a0b69-6b62-42e0-9b5d-dedb70de82c9', 'Amoxicillin', 1, 3.50, 3.50],
                [7, 'd7e8f9a0-0123-4b5c-6d7e-890123456789', '39dd566c-134d-4285-bd23-b091f3346f36', 'Aspirin', 3, 8.50, 25.50],
                [8, 'd7e8f9a0-0123-4b5c-6d7e-890123456789', 'cd28faf7-d03c-438a-8a5f-25b7a58bf741', 'Paracetamol', 6, 12, 72.0],
                [9, 'd7e8f9a0-0123-4b5c-6d7e-890123456789', '4f1a0b69-6b62-42e0-9b5d-dedb70de82c9', 'Amoxicillin', 2, 4, 8.0]]


def drop_table_if_exists(conn, table_name):
    try:
        conn.execute("DROP TABLE " + table_name)
    except Exception as e:
        print("exception encountered drop_table_if_exists [{0}]".format(e))


def insert_sample_data(conn):
    insert_data(conn, insert_statement_inventory, inventory)
    insert_data(conn, insert_statement_stock_update, stock_updates)
    insert_data(conn, insert_statement_bill, bills)
    insert_data(conn, insert_statement_bill_detail, bill_details)


def insert_data(conn, insert_statement, data):
    cur = conn.cursor()
    for item in data:
        cur.execute(insert_statement, item)
        conn.commit()


def drop_tables(db_conn):
    drop_table_if_exists(db_conn, "INVENTORY")
    drop_table_if_exists(db_conn, "STOCK_UPDATE")
    drop_table_if_exists(db_conn, "BILL")
    drop_table_if_exists(db_conn, "BILL_DETAIL")


def create_tables(db_conn):
    db_conn.execute(create_table_inventory)
    db_conn.execute(create_table_stock_update)
    db_conn.execute(create_table_bill)
    db_conn.execute(create_table_bill_detail)


def configure_sample_data(db_conn):
    insert_sample_data(db_conn)
