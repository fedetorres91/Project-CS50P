from cs50 import SQL
""" CREATE DATABASE 
 SCHEMA:
 table users (id, email, first name, last name, currency)
 table wallet (user_id, balance, currency)
 table transactions(id, user_id, tx_type, date, amount, currency, category, description)"""

# open db
db = SQL("sqlite:///wallet.db")
# CREATE TABLES
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, email TEXT NOT NULL, first_name TEXT, last_name TEXT NOT NULL, currency TEXT, PRIMARY KEY (id));")
db.execute("CREATE TABLE IF NOT EXISTS wallet (user_id INTEGER NOT NULL, balance FLOAT NOT NULL, currency TEXT, FOREIGN KEY (user_id) REFERENCES users (id));")
db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER, user_id INTEGER, tx_type TEXT NOT NULL, date DATE NOT NULL, amount FLOAT NOT NULL, currency TEXT, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));")
