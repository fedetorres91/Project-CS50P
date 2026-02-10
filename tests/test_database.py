from src.database import WalletRepository, TransactionRepository
from src.models import Wallet


# wallet repo
def test_create_wallet(temp_db):
    # correctly creates wallet table

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    repo = WalletRepository()
    repo.create_wallet(user_id, 1000)

    rows = temp_db.execute("SELECT user_id, balance FROM wallet WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["user_id"] == user_id
    assert rows[0]["balance"] == 1000

def test_load(temp_db):
    # correctly creates wallet object with balance and creation_date from database

        # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    repo = WalletRepository()
    repo.create_wallet(user_id, 1000)

    wallet = repo.load(user_id)
    assert wallet.balance == 1000
    assert wallet.creation_date is not None

def test_save(temp_db):
    # correclty updates wallet table

     # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    repo = WalletRepository()
    repo.create_wallet(user_id, 1000)

    # update wallet instance balance
    wallet = Wallet(2000)
    repo.save(user_id, wallet)
    rows = temp_db.execute("SELECT user_id, balance FROM wallet WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["user_id"] == user_id
    assert rows[0]["balance"] == 2000

# transaction repo

def test_save_income(temp_db):
    # tests save_income

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    w_repo = WalletRepository()
    w_repo.create_wallet(user_id, 1000)

    # transaction repo
    t_repo = TransactionRepository()
    t_repo.save_income(user_id, 500, 1500)

    rows = temp_db.execute("SELECT user_id, tx_type, amount,  balance_after FROM transactions WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["user_id"] == user_id
    assert rows[0]["tx_type"] == "income"
    assert rows[0]["amount"] == 500
    assert rows[0]["balance_after"] == 1500

def test_save_expense(temp_db):
    # tests save_expense

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    w_repo = WalletRepository()
    w_repo.create_wallet(user_id, 1000)

    # transaction repo
    t_repo = TransactionRepository()
    t_repo.save_expense(user_id, 500, 'Food', 'meal', 500)

    rows = temp_db.execute("SELECT user_id, tx_type, amount, category, description, balance_after FROM transactions WHERE user_id = ?", user_id)
    assert len(rows) == 1
    assert rows[0]["user_id"] == user_id
    assert rows[0]["tx_type"] == "expense"
    assert rows[0]["amount"] == 500
    assert rows[0]["category"] == "Food"
    assert rows[0]["description"] == "meal"
    assert rows[0]["balance_after"] == 500

def test_all_transactions(temp_db):

    # retrieves list of transaction of user

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    w_repo = WalletRepository()
    w_repo.create_wallet(user_id, 1000)

    # transaction repo
    t_repo = TransactionRepository()
    t_repo.save_expense(user_id, 500, 'Food', 'meal', 500)

    transactions = t_repo.get_all_transactions(user_id)

    assert len(transactions) == 1
    assert transactions[0]["user_id"] == user_id
    assert transactions[0]["tx_type"] == "expense"
    assert transactions[0]["amount"] == 500
    assert transactions[0]["category"] == "Food"
    assert transactions[0]["description"] == "meal"
    assert transactions[0]["balance_after"] == 500

def test_transaction_summary(temp_db):

    # first need to create user
    temp_db.execute("INSERT INTO users (username, password) VALUES (?, ?)", "alice", "hash")
    user_id = temp_db.execute("SELECT id FROM users WHERE username = ?", "alice")[0]["id"]

    w_repo = WalletRepository()
    w_repo.create_wallet(user_id, 5000)

    # transaction repo
    t_repo = TransactionRepository()
    t_repo.save_expense(user_id, 500, 'Food', 'meal', 4500)
    t_repo.save_expense(user_id, 100, 'Food', 'meal', 4400)
    t_repo.save_expense(user_id, 1000, 'House', 'rent', 3400)
    t_repo.save_expense(user_id, 400, 'House', 'tv', 3000)

    transactions = t_repo.transaction_summary(user_id)

    assert len(transactions) == 2
    # create dict with key category and value amount
    totals = {row["category"]: row["total_amount"] for row in transactions}

    assert totals["Food"] == 600
    assert totals["House"] == 1400
    












