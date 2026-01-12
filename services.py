"""Integrates class wallet with db"""

from models import Wallet
from database import WalletRepository

def create_wallet(user_id, amount):
    """creates """
    # create wallet instance
    wallet = Wallet(user_id, amount)
    # save to database
    wallet_repo = WalletRepository.create(user_id, amount)
    return wallet

def add_income(user_id, wallet, amount, currency="USD", category =None, description =None):):
    """adds income to instance and updates db"""
    wallet = wallet
    # updates instance
    if currency == "USD":
        wallet.balance += amount
    else:
        wallet.balance += convert_currency(amount, currency, "USD")
    
    # insert transaction and update balance on db
    wallet = wallet_repo.load(user_id)
    wallet.add_income(amount)
    tx_repo.save_income(user_id, amount)
    wallet_repo.save(user_id, wallet)



