import os
from datetime import datetime
from cs50 import SQL
from src.models import Wallet

""" CREATE DATABASE 
 SCHEMA:
 table users (id, username,  password)
 table wallet (user_id, balance, creation_date, currency)
 table transactions(id, user_id, tx_type, date, amount, currency, category, description, balance_after)"""

# TODO unit testing


# Create empty database file if it doesn't exist
if not os.path.exists("wallet.db"):
    open("wallet.db", "a").close()

db = SQL("sqlite:///wallet.db")

# open db
db = SQL("sqlite:///wallet.db")
# CREATE TABLES
# users
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, PRIMARY KEY (id));")
# wallet
db.execute("CREATE TABLE IF NOT EXISTS wallet (user_id INTEGER NOT NULL, balance FLOAT NOT NULL, creation_date DATETIME NOT NULL, currency TEXT, FOREIGN KEY (user_id) REFERENCES users (id));")

# transactions
db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER, user_id INTEGER, tx_type TEXT NOT NULL, date DATETIME NOT NULL, amount FLOAT NOT NULL, currency TEXT, category TEXT, description TEXT, balance_after FLOAT NOT NULL, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));")

# repositories/wallet_repository.py

class WalletRepository:
    """Manages wallet data persistence in the database.
    
    Handles creation, loading, and updating of wallet records.
    """

    def create_wallet(self, user_id: int, initial_balance: float):
        """Create a new wallet record in the database.
        
        Args:
            user_id (int): The ID of the user.
            initial_balance (float): The starting balance for the wallet.
            
        """
        db.execute(
            "INSERT INTO wallet (user_id, balance, creation_date) VALUES (?, ?, ?)",
            user_id, initial_balance, datetime.now().isoformat()
        )
        
    def load(self, user_id: int) -> Wallet:
        """Load a wallet from the database.
        
        Args:
            user_id (int): The ID of the user.
        
        Returns:
            Wallet: A wallet object with the user's current balance and creation date
        """
        row = db.execute(
            "SELECT balance, creation_date FROM wallet WHERE user_id = ?", user_id
        )[0]
        return Wallet(balance=row["balance"], creation_date=row["creation_date"])

    def save(self, user_id: int, wallet: Wallet):
        """Update wallet balance in the database.
        
        Args:
            user_id (int): The ID of the user.
            wallet (Wallet): The wallet object with updated balance.
        """
        db.execute(
            "UPDATE wallet SET balance = ? WHERE user_id = ?",
            wallet.balance, user_id
        )

class TransactionRepository:
    """Manages transaction data persistence in the database.
    
    Handles creation and retrieval of transaction records.
    """
    
    def save_income(self, user_id, amount, balance_after):
        """Record an income transaction.
        
        Args:
            user_id (int): The ID of the user.
            amount (float): The income amount.
            balance_after (float): The wallet balance after the transaction.
        """
        db.execute(
            "INSERT INTO transactions (user_id, tx_type, amount, date, balance_after) VALUES (?, ?, ?, ?, ?)",
            user_id, "income", amount, datetime.now().isoformat(), balance_after
        )

    def save_expense(self, user_id, amount, category, description, balance_after):
        """Record an expense transaction.
        
        Args:
            user_id (int): The ID of the user.
            amount (float): The expense amount.
            category (str): The expense category.
            description (str): Additional expense details.
            balance_after (float): The wallet balance after the transaction.
        """
        db.execute(
            "INSERT INTO transactions (user_id, tx_type, amount, category, description, date, balance_after) VALUES (?, ?, ?, ?, ?, ?, ?)",
            user_id, "expense", amount, category, description, datetime.now().isoformat(), balance_after
        )

    def get_all_transactions(self, user_id):
        """Retrieve all transactions for a user, ordered by date.
        
        Args:
            user_id (int): The ID of the user.
        
        Returns:
            list: A list of transaction records (dicts), or empty list if no transactions exist.
        """

        rows = db.execute(
            "SELECT users.id,  "
            "transactions.user_id, "
            "transactions.tx_type, "
            "transactions.amount, "
            "transactions.category, "
            "transactions.description, "
            "transactions.date, "
            "transactions.balance_after "
            "FROM users "
            "JOIN transactions ON users.id = transactions.user_id "
            "WHERE users.id = ? "
            " ORDER BY transactions.date DESC",
            user_id
        )
        return rows if rows else []
    
    def transaction_summary(self, user_id):
        """Returns amount of transaction per category.
        
        Args: user_id (int): The ID of the user.
        
        Returns: List of categoriese, amount. If there is none returns empty list.
            """
        transactions_categories = db.execute(
            "SELECT category, SUM(amount) AS total_amount" 
            " FROM transactions WHERE user_id = ? AND tx_type = ?" 
            " GROUP BY category", 
            user_id, "expense"
        )

        return transactions_categories
        
        
        
        