from cs50 import SQL
""" CREATE DATABASE 
 SCHEMA:
 table users (id, username,  password)
 table wallet (user_id, balance, currency)
 table transactions(id, user_id, tx_type, date, amount, currency, category, description)"""

# open db
db = SQL("sqlite:///wallet.db")
# CREATE TABLES
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, PRIMARY KEY (id));")
db.execute("CREATE TABLE IF NOT EXISTS wallet (user_id INTEGER NOT NULL, balance FLOAT NOT NULL, currency TEXT, FOREIGN KEY (user_id) REFERENCES users (id));")
db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER, user_id INTEGER, tx_type TEXT NOT NULL, date DATE NOT NULL, amount FLOAT NOT NULL, currency TEXT, category TEXT, description TEXT, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));")
