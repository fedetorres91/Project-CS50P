"""Integrates Wallet domain with persistence."""

import csv
import logging
import os
from datetime import datetime
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from src.models import Wallet, Transactions, convert_currency
from src.database import WalletRepository, TransactionRepository

# Suppress matplotlib debug messages
matplotlib.set_loglevel("warning")
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)


#TODO unit testing
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
    os.makedirs("data", exist_ok=True)
    filename = f"data/{user_id}_transactions_history.csv"
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)
    
    return filename

# get user balance history
def get_balance_history(user_id):
    """Retrieve balance history of user_id.
    
    Args:
        user_id(int): The ID of the user.
        
    Returns:
        list: List of dictionaries with ['date'] and ['balance'] info.
        
    Raises:
        ValueError: If user_id not found."""
    
    # load wallet info
    wallet = _wallet_repo.load(user_id)

    # get transaction history
    transactions = _tx_repo.get_all_transactions(user_id)

    if not transactions:
        raise ValueError(f"No transactions found for {user_id}")
    
    # Reverse to chronological order (oldest first)
    transactions = list(reversed(transactions))
    
    balance_history = []
    
    # Calculate initial balance from first (oldest) transaction
    first_tx = transactions[0]
    if first_tx['tx_type'] == 'income':
        initial_balance = first_tx['balance_after'] - first_tx['amount']
    else:
        initial_balance = first_tx['balance_after'] + first_tx['amount']
    
    # add initial balance point
    balance_history.append({'date': wallet.creation_date, 'balance': initial_balance})
    
    # add all transactions in chronological order
    for transaction in transactions:
        balance_history.append({
            'date': transaction['date'], 
            'balance': transaction['balance_after']
        })

    return balance_history


def save_balance_history(user_id):
    """Save a matplotlib graph with balance history.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        str: The filename of the saved graph.
    
    Raises:
        ValueError: If no transactions exist for the user.
    """
    balance_history = get_balance_history(user_id)
    
    # Extract dates and balances
    dates = [datetime.fromisoformat(entry['date']) for entry in balance_history]
    balances = [entry['balance'] for entry in balance_history]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, balances, marker='o', linestyle='-', linewidth=2)
    plt.xlabel('Date')
    plt.ylabel('Balance ($)')
    plt.title(f'Balance History - User {user_id}')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%Y"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.tight_layout()

    # Save the figure
    os.makedirs("data", exist_ok=True)
    filename = f"data/{user_id}_balance_history.png"
    plt.savefig(filename)
    plt.close()
    
    return filename


def save_transactions(user_id):
    """Save a matplotlib pie chart with transactions categories summary
    
    Args: user_id(int): User id
    
    Returns: filename of saved pie chart."""
    transactions_categories = _tx_repo.transaction_summary(user_id)

    if not transactions_categories:
        raise ValueError(f"No transactions found for {user_id}")

    labels = [t['category'] for t in transactions_categories]
    sizes = [t['total_amount'] for t in transactions_categories]

    if sum(sizes) <= 0:
        raise ValueError("Transaction amounts must be greater than zero")

    colors = plt.cm.Set3.colors[:len(sizes)]

    os.makedirs("data", exist_ok=True)
    filename = f"data/{user_id}_transactions_categories.png"

    def autopct(pct):
        total = sum(sizes)
        amount = pct * total / 100
        return f"{pct:.1f}%\n${amount:.2f}"

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=autopct,
        startangle=140
    )
    plt.axis("equal")

    plt.savefig(filename, bbox_inches="tight")
    plt.close()

    return filename







