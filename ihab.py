# import PyQt5
import yaml
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
        "FOREIGN KEY(account_from) REFERENCES accounts(account_id),"
        "FOREIGN KEY(transaction_category) REFERENCES categories(category_id))")
    #account table for bank/credit accounts
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts ("
        "account_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "account_name TEXT UNIQUE," 
        "type TEXT," 
        "starting_account_balance REAL," 
        "current_account_balance REAL," 
        "account_comment TEXT)")
    #budget category table
    cursor.execute("CREATE TABLE IF NOT EXISTS categories ("
        "category_id INTEGER PRIMARY KEY AUTOINCREMENT," 
        "category_name TEXT UNIQUE," 
        "starting_category_balance REAL," 
        "current_category_balance REAL," 
        "parent INTEGER," 
        "is_hidden BOOLEAN,"
        "FOREIGN KEY(parent) REFERENCES categories(category_id))")
    #table for transfers between categories
    cursor.execute("CREATE TABLE IF NOT EXISTS category_transfers("
        "transfer_id INTEGER PRIMARY KEY AUTOINCREMENT," 
        "transfer_date TEXT,"
        "category_from INTEGER," 
        "category_to INTEGER,"
        "transfer_amount REAL,"
        "FOREIGN KEY(category_from) REFERENCES categories(category_id),"
        "FOREIGN KEY(category_to) REFERENCES categories(category_id))")
    connection.commit()
    connection.close()

def make_transaction(db, date, category, account, amount, comments):
    data = (date, category, account, amount, comments)
    connection = create_connection(db)
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO ledger (transaction_date, transaction_category,'
            'account_from, transaction_amount, transaction_comment)'
            'VALUES (?, ?, ?, ?, ?)'
            , data)
    except Error as e:
        print(e)
    connection.commit()
    connection.close()

def make_category_transfer(db, date, category_from, category_to, amount):
    data = (date, category_from, category_to, amount)
    connection = create_connection(db)
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO category_transfers (transfer_date, category_from,'
            'category_to, transfer_amount)'
            'VALUES (?, ?, ?, ?)', data)
    except Error as e:
        print(e)
    connection.commit()
    connection.close()

def create_account(db, name, account_type, starting_balance, current_balance, comments):
    data = (name, account_type, starting_balance, current_balance, comments)
    connection = create_connection(db)
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO categories (category_name, type,'
            'starting_account_balance, current_account_balance, account_comment)'
            'VALUES (?, ?, ?, ?, ?)', data)
    except Error as e:
        print(f"Error {e}")
    connection.commit()
    connection.close()

def create_category(db, name, parent_category, balance):
    data = (name, balance, balance, parent_category)
    connection = create_connection(db)
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO categories (category_name, starting_category_balance,'
            'current_category_balance, parent, is_hidden)'
            'VALUES (?, ?, ?, ?, FALSE)',data)
    except Error as e:
        print(e)
    connection.commit()
    connection.close()

def set_category_is_hidden(db, category_name, is_hidden):
    connection = create_connection(db)
    cursor = connection.cursor()
    cursor.execute("UPDATE categories "
        "SET is_hidden = ? "
        "WHERE category_name = ? OR "
        "( ? AND "
        "category_id = (SELECT category_id FROM categories "
        "WHERE parent = (SELECT category_id FROM categories "
        "WHERE category_name = ?)))", 
        (is_hidden, category_name, is_hidden, category_name))
    connection.commit()
    connection.close()

def make_account_transfer(db, date, account_from, account_to, amount, comments):
    make_transaction(db, date, "transfer", account_from, -1.0*amount, comments)
    make_transaction(db, date, "transfer", account_to, amount, comments)

def setup_budget_from_file(config_file):
    with open(config_file, 'r') as file:
        budget = yaml.safe_load(file)
    print(budget)
    for parent in budget['budget']:
        for child in parent['children']:
            print(parent['parent_category']+': '+child['category']


init_databases("./test.db")
#create_category("./test.db", "groceries", None, 100.00)
#create_category("./test.db", "eggs", 1, 20.00)
#set_category_is_hidden("./test.db", "groceries", True)
#set_category_is_hidden("./test.db", "groceries", False)
connection = create_connection("./test.db");
cursor = connection.cursor();
cursor.execute("SELECT * FROM categories");
print(cursor.fetchall())
setup_budget_from_file("budget.yaml")
