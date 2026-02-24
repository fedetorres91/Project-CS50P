import os
import pytest
from cs50 import SQL
from src.database import init_db


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    db_path.touch()
    db = SQL(f"sqlite:///{db_path}")
    init_db(db)

    from src import database
    monkeypatch.setattr(database, "db", db)
    return db


@pytest.fixture(autouse=True)
def _matplotlib_backend(monkeypatch):
    monkeypatch.setenv("MPLBACKEND", "Agg")
