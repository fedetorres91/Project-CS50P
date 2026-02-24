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
    user_id = user_service.create_user("alice", "secret12")

    row = user_service_db.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        "alice",
    )[0]

    assert user_id == row["id"]
    assert row["username"] == "alice"
    assert row["password"] != "secret12"
    assert check_password_hash(row["password"], "secret12")


def test_create_user_validates_empty_values(user_service_db):
    with pytest.raises(ValueError):
        user_service.create_user("", "secret12")
    with pytest.raises(ValueError):
        user_service.create_user("alice", "")


def test_log_in_success(user_service_db):
    user_id = user_service.create_user("alice", "secret12")

    result = user_service.log_in("alice", "secret12")

    assert result == (user_id, "alice")


def test_log_in_invalid_credentials(user_service_db):
    user_service.create_user("alice", "secret12")

    assert user_service.log_in("alice", "wrongpass") is None
    assert user_service.log_in("missing", "secret12") is None
    assert user_service.log_in(" ", "secret12") is None
    assert user_service.log_in("alice", "") is None


def test_log_in_strips_username(user_service_db):
    user_id = user_service.create_user("alice", "secret12")

    result = user_service.log_in("  alice  ", "secret12")

    assert result == (user_id, "alice")


def test_create_user_rejects_short_password(user_service_db):
    with pytest.raises(ValueError, match="8 characters"):
        user_service.create_user("alice", "short")


def test_load_wallet_returns_existing_wallet(user_service_db):
    from datetime import datetime
    user_id = user_service.create_user("alice", "secret12")
    user_service_db.execute(
        "INSERT INTO wallet (user_id, balance, creation_date, currency) VALUES (?, ?, ?, ?)",
        user_id, 75.5, datetime.now().isoformat(), "USD",
    )

    wallet = user_service.load_wallet(user_id)

    assert isinstance(wallet, Wallet)
    assert wallet.balance == 75.5
