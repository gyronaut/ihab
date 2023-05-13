import typing
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QModelIndex, Qt
import yaml
import sys
import sqlite3
from sqlite3 import Error

qt_designer_file = 'mainwindow.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_designer_file)

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
        "FOREIGN KEY(parent) REFERENCES parent_categories(parent_id))")
    #budget parent category table
    cursor.execute("CREATE TABLE IF NOT EXISTS parent_categories ("
        "parent_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "parent_name TEXT UNIQUE,"
        "is_hidden BOOLEAN)")
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

def make_transaction(cursor, date, category, account, amount, comments):
    data = (date, category, account, amount, comments)
    try:
        cursor.execute('INSERT INTO ledger (transaction_date, transaction_category,'
            'account_from, transaction_amount, transaction_comment)'
            'VALUES (?, ?, ?, ?, ?)'
            , data)
    except Error as e:
        print(e)

def make_category_transfer(cursor, date, category_from, category_to, amount):
    data = (date, category_from, category_to, amount)
    try:
        cursor.execute('INSERT INTO category_transfers (transfer_date, category_from,'
            'category_to, transfer_amount)'
            'VALUES (?, ?, ?, ?)', data)
    except Error as e:
        print(e)

def create_account(cursor, name, account_type, starting_balance, current_balance, comments):
    data = (name, account_type, starting_balance, current_balance, comments)
    try:
        cursor.execute('INSERT INTO categories (category_name, type,'
            'starting_account_balance, current_account_balance, account_comment)'
            'VALUES (?, ?, ?, ?, ?)', data)
    except Error as e:
        print(f"Error {e}")

def create_category(cursor, name, parent_category, starting_balance):
    data = {"name": name, "balance": starting_balance, "parent": parent_category}
    try:
        cursor.execute('INSERT INTO categories (category_name, starting_category_balance,'
            'current_category_balance, parent, is_hidden)'
            'VALUES (:name, :balance, :balance, :parent, FALSE)',data)
    except Error as e:
        print(e)

def create_parent(cursor, name):
    try:
        cursor.execute('INSERT INTO parent_categories (parent_name, is_hidden) '
            'VALUES (?, ?)', (name, False))
    except Error as e:
        print(e)

def set_category_is_hidden(cursor, category_name, is_hidden):
    cursor.execute("UPDATE categories "
        "SET is_hidden = ? "
        "WHERE category_name = ?", 
        (is_hidden, category_name))

def set_parent_is_hidden(cursor, parent_name, is_hidden):
    data = {"parent": parent_name, "hidden": is_hidden}
    cursor.execute("UPDATE parent_categories "
            "SET is_hidden :hidden "
            "WHERE parent_name = :parent "
            "IF (:hidden) "
            "BEGIN "
                "UPDATE categories "
                "SET is_hidden :hidden "
                "WHERE parent_name = :parent"
            "END",
            data)

def make_account_transfer(cursor, date, account_from, account_to, amount, comments):
    make_transaction(cursor, date, "transfer", account_from, -1.0*amount, comments)
    make_transaction(cursor, date, "transfer", account_to, amount, comments)

def read_budget_from_file(config_file):
    with open(config_file, 'r') as file:
        budget = yaml.safe_load(file)
    print(budget)
    for parent in budget['budget']:
        for child in parent['children']:
            print(parent['parent_category']+': '+child['category'])
    return budget

def make_categories_from_budget(cursor, budget):
    for parent in budget['budget']:
        create_parent(cursor, parent['parent_category'])
        parent_id = cursor.execute("SELECT last_insert_rowid()").fetchone()[0]
        for child in parent['children']:
            create_category(cursor, child['category'], parent_id, 0.0)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = BudgetModel(budget=[{'test': 100.0}, {'other': 50.00}])
        self.budgetView.setModel(self.model)

class BudgetModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, budget=None, **kwargs):
        super(BudgetModel, self).__init__(*args, **kwargs)
        self.budget = budget or []

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.budget)
    
    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.budget[0])
    
    def data(self, index: QModelIndex, role: int = ...) -> any:
        if role == Qt.ItemDataRole.DisplayRole:
            #text = self.budget[index.row()][index.column()]
            #text = self.budget[index.row()]
            return "test"

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

path = "./test.db"
init_databases(path)
connection = create_connection(path);
cursor = connection.cursor();
budget = read_budget_from_file("budget.yaml")
make_categories_from_budget(cursor, budget)
connection.commit();
cursor.execute("SELECT * FROM categories")
print(cursor.fetchall())
cursor.execute("SELECT * FROM parent_categories")
print(cursor.fetchall())
connection.close()

