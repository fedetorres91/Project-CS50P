"""User and wallet helpers for CLI layer."""

from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db, WalletRepository
from src.models import Wallet

# DB auth helpers

def username_exists(username: str) -> bool:
    """Check if a username already exists in the database.
    
    Args:
        username (str): The username to check.
    
    Returns:
        bool: True if username exists, False otherwise.
    """
    result = db.execute("SELECT username FROM users WHERE username = ?", username)
    return len(result) > 0


def create_user(username: str, password: str) -> int:
    """Create a new user account with hashed password.
    
    Args:
        username (str): The username for the new account.
        password (str): The plaintext password (will be hashed).
    
    Returns:
        int: The user ID of the newly created user.
    """
    hashed_password = generate_password_hash(password)
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, hashed_password)
    user_row = db.execute("SELECT id FROM users WHERE username = ?", username)[0]
    return user_row["id"]


def log_in(username: str, password: str):
    """Authenticate a user by verifying username and password.
    
    Args:
        username (str): The username to authenticate.
        password (str): The plaintext password to verify.
    
    Returns:
        tuple: (user_id, username) if authentication succeeds, None if credentials invalid.
    """
    rows = db.execute("SELECT id, username, password FROM users WHERE username = ?", username)
    if not rows:
        return None
    
    # Check if provided password matches the stored hash
    if check_password_hash(rows[0]["password"], password):
        return (rows[0]["id"], rows[0]["username"])
    
    return None


# Wallet helpers

_wallet_repo = WalletRepository()

def create_wallet(user_id: int, initial_balance: float) -> Wallet:
    """Create a new wallet for a user with an initial balance.
    
    Args:
        user_id (int): The ID of the user.
        initial_balance (float): The starting balance for the wallet.
    
    Returns:
        Wallet: The newly created wallet object.
    """
    _wallet_repo.create_wallet(user_id, initial_balance)
    return _wallet_repo.load(user_id)


def load_wallet(user_id: int) -> Wallet:
    """Load a user's wallet from the database.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        Wallet: The loaded wallet object with current balance.
    """
    return _wallet_repo.load(user_id)
