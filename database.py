from datetime import date
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

# repositories/wallet_repository.py

from models import Wallet
from database import db

class WalletRepository:
    """class Walletrepository, updates wallet table on database """

    def create_wallet(self, user_id: int, initial_balance: float):
        """creates a wallet on database"""
        db.execute(
            "INSERT INTO wallet (user_id, balance) VALUES (?, ?)",
            user_id, initial_balance
        )
        
    def load(self, user_id: int) -> Wallet:
        """retreives balance from a user_id"""
        row = db.execute(
            "SELECT balance FROM wallet WHERE user_id = ?", user_id
        )[0]
        return Wallet(balance=row["balance"])

    def save(self, user_id: int, wallet: Wallet):
        """updates wallet table on db"""
        db.execute(
            "UPDATE wallet SET balance = ? WHERE user_id = ?",
            wallet.balance, user_id
        )

class TransactionRepository:
    def save_income(self, user_id, amount):
        db.execute(
            "INSERT INTO transactions (user_id, tx_type, amount, date) VALUES (?, ?, ?, ?)",
            user_id, "income", amount, date.today().isoformat()
        )

    def save_expense(self, user_id, amount, category, description):
        db.execute(
            "INSERT INTO transactions (user_id, tx_type, amount, category, description, date) VALUES (?, ?, ?, ?, ?, ?)",
            user_id, "expense", amount, category, description, date.today().isoformat()
        )
