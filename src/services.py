"""Integrates Wallet domain with persistence."""

from src.models import Wallet, Transactions, convert_currency
from src.database import WalletRepository, TransactionRepository
import csv

_wallet_repo = WalletRepository()
_tx_repo = TransactionRepository()


def create_wallet(user_id, amount):
    """Create and save on database a wallet for the user."""
    wallet = Wallet(amount)
    _wallet_repo.create_wallet(user_id, amount)
    return wallet


def add_income(user_id, wallet, amount, currency="USD"):
    """Add income to wallet and save on database transaction and balance."""
    if currency == "USD":
        wallet.add_income(amount)
    else:
        wallet.add_income(convert_currency(amount, currency, "USD"))

    balance_after = wallet.balance
    _tx_repo.save_income(user_id, amount, balance_after)
    _wallet_repo.save(user_id, wallet)


def add_expense(user_id, wallet, amount, currency="USD", category=None, description=None):
    """Add expense to wallet and save on database transaction and balance."""
    if currency == "USD":
        wallet.add_expense(amount)
    else:
        wallet.add_expense(convert_currency(amount, currency, "USD"))

    balance_after = wallet.balance
    _tx_repo.save_expense(user_id, amount, category, description, balance_after)
    _wallet_repo.save(user_id, wallet)


def export_transactions_to_csv(user_id):
    """Export user's transaction history to csv."""
    transactions = _tx_repo.get_all_transactions(user_id)

    if not transactions:
        raise ValueError(f"No transactions found for {user_id}")
    
    # create and save csv file to data folder
    filename = f"data/{user_id}_transactions_history.csv"
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)
    
    return filename




