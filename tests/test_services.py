import src.services
import os
import csv
import pytest

def test_create_wallet(temp_db):

    # test wallet instance creation and saved on db

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 1000)
    assert wallet.balance == 1000

    rows = temp_db.execute("SELECT user_id, balance FROM wallet WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["user_id"] == user_id
    assert rows[0]["balance"] == 1000
    
def test_add_income(temp_db):

    # test income transaction and wallet update 

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 1000)
    src.services.add_income(user_id, wallet, 500)

    assert wallet.balance == 1500

    rows = temp_db.execute("SELECT user_id, balance FROM wallet WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["balance"] == 1500

    rows = temp_db.execute("SELECT user_id, tx_type, amount,  balance_after FROM transactions WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["tx_type"] == "income"
    assert rows[0]["amount"] == 500
    assert rows[0]["balance_after"] == 1500


def test_add_expense(temp_db):

    # test expense transaction and wallet update 

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 1000)
    src.services.add_expense(user_id, wallet, 500)

    assert wallet.balance == 500

    rows = temp_db.execute("SELECT user_id, balance FROM wallet WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["balance"] == 500

    rows = temp_db.execute("SELECT user_id, tx_type, amount,  balance_after FROM transactions WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["tx_type"] == "expense"
    assert rows[0]["amount"] == 500
    assert rows[0]["balance_after"] == 500


def test_export_transactions_to_csv_success(temp_db, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)

    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 0)
    src.services.add_income(user_id, wallet, 100)

    filename = src.services.export_transactions_to_csv(user_id)

    assert filename == f"data/{user_id}_transactions_history.csv"
    assert os.path.exists(filename)

    with open(filename, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["tx_type"] == "income"
    assert float(rows[0]["amount"]) == 100

def test_export_transactions_to_csv_empty_raises(temp_db):
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]
    src.services.create_wallet(user_id, 0)

    with pytest.raises(ValueError):
        src.services.export_transactions_to_csv(user_id)


def test_get_balance_history(temp_db):
    # returns list of dict with date and after_balance of transactions

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 1000)
    src.services.add_expense(user_id, wallet, 500)
    src.services.add_expense(user_id, wallet, 100)

    transactions = src.services.get_balance_history(user_id)

    assert len(transactions) == 3

    assert transactions[0]["balance"] == 1000
    assert transactions[1]["balance"] == 500
    assert transactions[2]["balance"] == 400

def test_save_balance_history_success(temp_db, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)

    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 1000)
    src.services.add_expense(user_id, wallet, 200)

    filename = src.services.save_balance_history(user_id)
    assert filename == f"data/{user_id}_balance_history.png"
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


def test_save_balance_history_empty_raises(temp_db):
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]
    src.services.create_wallet(user_id, 0)

    with pytest.raises(ValueError):
        src.services.save_balance_history(user_id)


def test_save_transactions_success(temp_db, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)

    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    wallet = src.services.create_wallet(user_id, 1000)
    src.services.add_expense(user_id, wallet, 100, category="Food", description="meal")
    src.services.add_expense(user_id, wallet, 200, category="House", description="rent")

    filename = src.services.save_transactions(user_id)
    assert filename == f"data/{user_id}_transactions_categories.png"
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0


def test_save_transactions_empty_raises(temp_db):
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]
    src.services.create_wallet(user_id, 0)

    with pytest.raises(ValueError):
        src.services.save_transactions(user_id)
