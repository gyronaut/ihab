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

#FOREIGN KEY(account_from) REFERENCES account(account_id),
#FOREIGN KEY(transaction_category) REFERENCES category(category_id))

def init_databases(path):
    connection = create_connection(path)
    cursor = connection.cursor()

   
    cursor.execute("CREATE TABLE IF NOT EXISTS ledger(" 
        "transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,"  
        "transaction_date TEXT," 
        "transaction_category INTEGER," 
        "account_from INTEGER," 
        "transaction_amount REAL,"
        "transaction_comment TEXT,"
        "FOREIGN KEY(account_from) REFERENCES account(account_id),"
        "FOREIGN KEY(transaction_category) REFERENCES category(category_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS account ("
        "account_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "account_name TEXT," 
        "type TEXT," 
        "starting_account_balance REAL," 
        "current_account_balance REAL," 
        "account_comment TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS category("
        "category_id INTEGER PRIMARY KEY AUTOINCREMENT," 
        "category_name TEXT," 
        "starting_category_balance REAL," 
        "current_category_balance REAL," 
        "parent INTEGER," 
        "is_hidden BOOLEAN,"
        "FOREIGN KEY(parent) REFERENCES category(category_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS category_transfer("
        "transfer_id INTEGER PRIMARY KEY AUTOINCREMENT," 
        "transfer_date TEXT,"
        "category_from INTEGER," 
        "category_to INTEGER,"
        "transfer_amount REAL,"
        "FOREIGN KEY(category_from) REFERENCES category(category_id),"
        "FOREIGN KEY(category_to) REFERENCES category(category_id))")

def add_entry(cursor, table_name, data_string):
    return 0

def remove_entry(cursor, table_name, entry_id):
    return 0

def edit_entry(cursor, tablie_name, entry_name, data_string):
    return 0

init_databases("./test.db")
