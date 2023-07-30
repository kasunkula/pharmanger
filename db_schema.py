create_table_inventory = '''CREATE TABLE INVENTORY
                            (ID            TEXT    NOT NULL,
                            NAME            TEXT    NOT NULL PRIMARY KEY,
                            UNITS           INT    NOT NULL,
                            AVG_PRICE       REAL,
                            COST            REAL,
                            ALERT         INT,
                            CRITICAL_ALERT   INT)'''

insert_statement_inventory = '''INSERT INTO INVENTORY(ID, NAME, UNITS, AVG_PRICE, COST, ALERT, CRITICAL_ALERT) VALUES (?,?,?,?,?,?,?) '''
update_statement_inventory = '''UPDATE INVENTORY SET UNITS = ?, AVG_PRICE = ?, COST = ?  WHERE ID = ?'''

create_table_stock_update = ''' CREATE TABLE STOCK_UPDATE
                                (ID            TEXT    NOT NULL PRIMARY KEY,
                                ITEM_ID        TEXT        NOT NULL,
                                ITEM_NAME        TEXT        NOT NULL,                                
                                UNITS          INT     NOT NULL,
                                COST   REAL    NOT NULL)'''

insert_statement_stock_update = ''' INSERT INTO STOCK_UPDATE(ID, ITEM_ID, ITEM_NAME, UNITS, COST) VALUES (?,?,?,?,?) '''

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

create_table_medical_professional = '''CREATE TABLE MEDICAL_PROFESSIONAL
                            (ID            TEXT    NOT NULL,
                            NAME            TEXT    NOT NULL PRIMARY KEY,
                            SLMC            TEXT    NOT NULL PRIMARY KEY,
                            NAME            TEXT    NOT NULL PRIMARY KEY,
                            DESCRIPTION     TEXT    )'''
insert_statement_medical_professional = '''INSERT INTO MEDICAL_PROFESSIONAL(ID,NAME,UNITS) VALUES (?,?,?) '''


def drop_table_if_exists(conn, table_name):
    try:
        conn.execute("DROP TABLE " + table_name)
    except Exception as e:
        print("exception encountered drop_table_if_exists [{0}]".format(e))


def insert_sample_data(conn):
    import sample_data
    insert_data(conn, insert_statement_inventory, sample_data.inventory)
    insert_data(conn, insert_statement_stock_update, sample_data.stock_updates)
    insert_data(conn, insert_statement_bill, sample_data.bills)
    insert_data(conn, insert_statement_bill_detail, sample_data.bill_details)


def insert_data(conn, insert_statement, data):
    cur = conn.cursor()
    for item in data:
        try:
            cur.execute(insert_statement, item)
            conn.commit()
        except Exception as e:
            print(e)
            raise e


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
