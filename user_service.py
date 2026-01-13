"""User and wallet helpers for CLI layer."""

from database import db, WalletRepository
from models import Wallet

# DB auth helpers

def username_exists(username: str) -> bool:
    result = db.execute("SELECT username FROM users WHERE username = ?", username)
    return len(result) > 0


def create_user(username: str, password: str) -> int:
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, password)
    user_row = db.execute("SELECT id FROM users WHERE username = ?", username)[0]
    return user_row["id"]


def log_in(username: str, password: str):
    rows = db.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", username, password)
    if not rows:
        return None
    return (rows[0]["id"], rows[0]["username"])


# Wallet helpers

_wallet_repo = WalletRepository()

def create_wallet(user_id: int, initial_balance: float) -> Wallet:
    _wallet_repo.create_wallet(user_id, initial_balance)
    return _wallet_repo.load(user_id)


def load_wallet(user_id: int) -> Wallet:
    return _wallet_repo.load(user_id)
