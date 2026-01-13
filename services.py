"""Integrates Wallet domain with persistence."""

from models import Wallet, Transactions, convert_currency
from database import WalletRepository, TransactionRepository

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

    _tx_repo.save_income(user_id, amount)
    _wallet_repo.save(user_id, wallet)


def add_expense(user_id, wallet, amount, currency="USD", category=None, description=None):
    """Add expense to wallet and save on database transaction and balance."""
    if currency == "USD":
        wallet.add_expense(amount)
    else:
        wallet.add_expense(convert_currency(amount, currency, "USD"))

    _tx_repo.save_expense(user_id, amount, category, description)
    _wallet_repo.save(user_id, wallet)



