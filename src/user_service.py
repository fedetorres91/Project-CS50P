"""User and wallet helpers for CLI layer."""

from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db, WalletRepository
from src.models import Wallet

MIN_PASSWORD_LENGTH = 8

# DB auth helpers

def _normalized_username(username: str) -> str:
    """Normalize username input for DB operations."""
    return username.strip() if isinstance(username, str) else ""


def username_exists(username: str) -> bool:
    """Check if a username already exists in the database.
    
    Args:
        username (str): The username to check.
    
    Returns:
        bool: True if username exists, False otherwise.
    """
    username = _normalized_username(username)
    if not username:
        return False
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
    username = _normalized_username(username)
    if not username:
        raise ValueError("Username cannot be empty.")
    if not isinstance(password, str) or not password:
        raise ValueError("Password cannot be empty.")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")

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
    username = _normalized_username(username)
    if not username or not isinstance(password, str) or not password:
        return None

    rows = db.execute("SELECT id, username, password FROM users WHERE username = ?", username)
    if not rows:
        return None
    
    # Check if provided password matches the stored hash
    if check_password_hash(rows[0]["password"], password):
        return (rows[0]["id"], rows[0]["username"])
    
    return None


# Wallet helpers

_wallet_repo = WalletRepository()


def load_wallet(user_id: int) -> Wallet:
    """Load a user's wallet from the database.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        Wallet: The loaded wallet object with current balance.
    """
    return _wallet_repo.load(user_id)
