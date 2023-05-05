import PyQt5
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"Error '{e}' has occured")
    return connection

def init_databases():
    connection = create_connection("")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS transaction(id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_date TEXT, category INTEGER, account INTEGER, transaction_amount REAL, transaction_comment TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS account(id INTEGER PRIMARY KEY AUTOINCREMENT, account_name TEXT, type TEXT, starting_account_balance REAL, current_account_balance REAL, account_comment TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS category(id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT, starting_category_balance REAL, current_category_balance REAL, parent INTEGER, is_hidden BOOLEAN)")
    cursor.execute("CREATE TABLE IF NOT EXISTS category_transfer(id INTEGER PRIMARY KEY AUTOINCREMENT, transfer_date TEXT, category_from INTEGER, category_to INTEGER, transfer_amount REAL)")

def add_entry(cursor, table_name, data_string):
    return 0

def remove_entry(cursor, table_name, entry_id):
    return 0

def edit_entry(cursor, tablie_name, entry_name, data_string):
    return 0

