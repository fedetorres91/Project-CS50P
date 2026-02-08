"""Integrates Wallet domain with persistence."""

from src.models import Wallet, Transactions, convert_currency
from src.database import WalletRepository, TransactionRepository
import csv

_wallet_repo = WalletRepository()
_tx_repo = TransactionRepository()


def create_wallet(user_id, amount):
    """Create and persist a new wallet for a user.
    
    Args:
        user_id (int): The ID of the user.
        amount (float): The initial wallet balance.
    
    Returns:
        Wallet: The newly created wallet object.
    """
    wallet = Wallet(amount)
    _wallet_repo.create_wallet(user_id, amount)
    return wallet


def add_income(user_id, wallet, amount, currency="USD"):
    """Record income transaction and update wallet balance in database.
    
    Args:
        user_id (int): The ID of the user.
        wallet (Wallet): The user's wallet object.
        amount (float): The income amount.
        currency (str): Currency code; defaults to 'USD'.
    
    Raises:
        ValueError: If amount is invalid.
    """
    if currency == "USD":
        wallet.add_income(amount)
    else:
        wallet.add_income(convert_currency(amount, currency, "USD"))

    balance_after = wallet.balance
    _tx_repo.save_income(user_id, amount, balance_after)
    _wallet_repo.save(user_id, wallet)


def add_expense(user_id, wallet, amount, currency="USD", category=None, description=None):
    """Record expense transaction and update wallet balance in database.
    
    Args:
        user_id (int): The ID of the user.
        wallet (Wallet): The user's wallet object.
        amount (float): The expense amount.
        currency (str): Currency code; defaults to 'USD'.
        category (str): Transaction category; optional.
        description (str): Additional expense details; optional.
    
    Raises:
        ValueError: If amount is invalid or exceeds balance.
    """
    if currency == "USD":
        wallet.add_expense(amount)
    else:
        wallet.add_expense(convert_currency(amount, currency, "USD"))

    balance_after = wallet.balance
    _tx_repo.save_expense(user_id, amount, category, description, balance_after)
    _wallet_repo.save(user_id, wallet)


def export_transactions_to_csv(user_id):
    """Export user's complete transaction history to a CSV file.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        str: The filename of the exported CSV file.
    
    Raises:
        ValueError: If no transactions exist for the user.
    """
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




