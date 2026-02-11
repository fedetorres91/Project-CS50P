import pytest
from werkzeug.security import check_password_hash

import src.user_service as user_service
from src.models import Wallet


@pytest.fixture
def user_service_db(temp_db, monkeypatch):
    monkeypatch.setattr(user_service, "db", temp_db)
    return temp_db


def test_username_exists(user_service_db):
    assert user_service.username_exists("alice") is False
    assert user_service.username_exists("   ") is False

    user_service_db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        "alice",
        "hashed",
    )

    assert user_service.username_exists("alice") is True


def test_create_user_creates_hashed_password_and_returns_id(user_service_db):
    user_id = user_service.create_user("alice", "secret")

    row = user_service_db.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        "alice",
    )[0]

    assert user_id == row["id"]
    assert row["username"] == "alice"
    assert row["password"] != "secret"
    assert check_password_hash(row["password"], "secret")


def test_create_user_validates_empty_values(user_service_db):
    with pytest.raises(ValueError):
        user_service.create_user("", "secret")
    with pytest.raises(ValueError):
        user_service.create_user("alice", "")


def test_log_in_success(user_service_db):
    user_id = user_service.create_user("alice", "secret")

    result = user_service.log_in("alice", "secret")

    assert result == (user_id, "alice")


def test_log_in_invalid_credentials(user_service_db):
    user_service.create_user("alice", "secret")

    assert user_service.log_in("alice", "wrong") is None
    assert user_service.log_in("missing", "secret") is None
    assert user_service.log_in(" ", "secret") is None
    assert user_service.log_in("alice", "") is None


def test_log_in_strips_username(user_service_db):
    user_id = user_service.create_user("alice", "secret")

    result = user_service.log_in("  alice  ", "secret")

    assert result == (user_id, "alice")


def test_create_wallet_persists_and_returns_wallet(user_service_db):
    user_id = user_service.create_user("alice", "secret")

    wallet = user_service.create_wallet(user_id, 250.0)

    assert isinstance(wallet, Wallet)
    assert wallet.balance == 250.0

    row = user_service_db.execute(
        "SELECT balance FROM wallet WHERE user_id = ?",
        user_id,
    )[0]
    assert row["balance"] == 250.0


def test_load_wallet_returns_existing_wallet(user_service_db):
    user_id = user_service.create_user("alice", "secret")
    user_service.create_wallet(user_id, 75.5)

    wallet = user_service.load_wallet(user_id)

    assert isinstance(wallet, Wallet)
    assert wallet.balance == 75.5
