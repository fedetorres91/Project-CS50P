"""User and wallet helpers for CLI layer."""

from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db, WalletRepository
from src.models import Wallet

# DB auth helpers

def username_exists(username: str) -> bool:
    result = db.execute("SELECT username FROM users WHERE username = ?", username)
    return len(result) > 0


def create_user(username: str, password: str) -> int:
    """Create a user with a hashed password"""
    hashed_password = generate_password_hash(password)
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, hashed_password)
    user_row = db.execute("SELECT id FROM users WHERE username = ?", username)[0]
    return user_row["id"]


def log_in(username: str, password: str):
    """Authenticate user by checking hashed password"""
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
    _wallet_repo.create_wallet(user_id, initial_balance)
    return _wallet_repo.load(user_id)


def load_wallet(user_id: int) -> Wallet:
    return _wallet_repo.load(user_id)
