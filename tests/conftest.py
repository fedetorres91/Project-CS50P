import os
import pytest
from cs50 import SQL

os.environ.setdefault("MPLBACKEND", "Agg")


def _create_schema(db):
    db.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, "
        "PRIMARY KEY (id));"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS wallet ("
        "user_id INTEGER NOT NULL, balance FLOAT NOT NULL, "
        "creation_date DATETIME NOT NULL, currency TEXT, "
        "FOREIGN KEY (user_id) REFERENCES users (id));"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS transactions ("
        "id INTEGER, user_id INTEGER, tx_type TEXT NOT NULL, "
        "date DATETIME NOT NULL, amount FLOAT NOT NULL, currency TEXT, "
        "category TEXT, description TEXT, balance_after FLOAT NOT NULL, "
        "PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id));"
    )


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    db_path.touch()
    db = SQL(f"sqlite:///{db_path}")
    _create_schema(db)

    from src import database
    monkeypatch.setattr(database, "db", db)
    return db


@pytest.fixture(autouse=True)
def _matplotlib_backend(monkeypatch):
    monkeypatch.setenv("MPLBACKEND", "Agg")
