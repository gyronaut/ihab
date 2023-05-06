# import PyQt5
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"Error {e} has occured")
    return connection

def init_databases(path):
    connection = create_connection(path)
    cursor = connection.cursor()
    #ledger table for transactions
    cursor.execute("CREATE TABLE IF NOT EXISTS ledger(" 
        "transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,"  
        "transaction_date TEXT," 
        "transaction_category INTEGER," 
        "account_from INTEGER," 
        "transaction_amount REAL,"
        "transaction_comment TEXT,"
        "FOREIGN KEY(account_from) REFERENCES account(account_id),"
        "FOREIGN KEY(transaction_category) REFERENCES category(category_id))")
    #account table for bank/credit accounts
    cursor.execute("CREATE TABLE IF NOT EXISTS account ("
        "account_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "account_name TEXT," 
        "type TEXT," 
        "starting_account_balance REAL," 
        "current_account_balance REAL," 
        "account_comment TEXT)")
    #budget category table
    cursor.execute("CREATE TABLE IF NOT EXISTS category("
        "category_id INTEGER PRIMARY KEY AUTOINCREMENT," 
        "category_name TEXT," 
        "starting_category_balance REAL," 
        "current_category_balance REAL," 
        "parent INTEGER," 
        "is_hidden BOOLEAN,"
        "FOREIGN KEY(parent) REFERENCES category(category_id))")
    #table for transfers between categories
    cursor.execute("CREATE TABLE IF NOT EXISTS category_transfer("
        "transfer_id INTEGER PRIMARY KEY AUTOINCREMENT," 
        "transfer_date TEXT,"
        "category_from INTEGER," 
        "category_to INTEGER,"
        "transfer_amount REAL,"
        "FOREIGN KEY(category_from) REFERENCES category(category_id),"
        "FOREIGN KEY(category_to) REFERENCES category(category_id))")
    connection.close()

def add_entry(cursor, table_name, data_string):
    return 0

def remove_entry(cursor, table_name, entry_id):
    return 0

def edit_entry(cursor, table_name, entry_name, data_string):
    return 0

def make_transaction(db, date, category, account, amount, comments):
    data = (date, category, account, amount, comments)
    connection = create_connection(db)
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO ledger (transaction_date, transaction_category, account_from, transaction_amount, transaction_comment) VALUES (?, ?, ?, ?, ?)', data)
    except Error as e:
        print(e)
    connection.commit();
    connection.close()
    return 0

def make_category_transfer(db, date, category_from, category_to, amount):
    return 0

def create_account(db, name, account_type, starting_balance, comments):
    return 0

def create_category(db, name, parent_name, balance):
    return 0

def hide_category(name):
    return 0



def make_account_transfer(db, date, account_from, account_to, amount, comments):
    make_transaction(db, date, "transfer", account_from, -1.0*amount, comments)
    make_transaction(db, date, "transfer", account_to, amount, comments)


init_databases("./test.db")
make_transaction("./test.db", "2023-05-06", None, None, 10.0, "test transaction")

connection = create_connection("./test.db");
cursor = connection.cursor();
cursor.execute("SELECT * FROM ledger");
print(cursor.fetchall())

