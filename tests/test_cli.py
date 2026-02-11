import src.cli as cli


class DummyWallet:
    def __init__(self, balance):
        self.balance = balance


def test_get_amount_input_retries_until_valid(monkeypatch):
    entries = iter(["abc", "-1", "0", "2.5"])
    monkeypatch.setattr("builtins.input", lambda _="": next(entries))

    amount = cli.get_amount_input()

    assert amount == 2.5


def test_get_amount_input_allow_zero(monkeypatch):
    entries = iter(["0"])
    monkeypatch.setattr("builtins.input", lambda _="": next(entries))

    amount = cli.get_amount_input(allow_zero=True)

    assert amount == 0.0


def test_ask_transaction_reprompts_until_valid(monkeypatch):
    entries = iter(["x", "9", "2"])
    monkeypatch.setattr("builtins.input", lambda _="": next(entries))

    action = cli.ask_transaction()

    assert action == 2


def test_log_in_uses_user_service(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _="": "alice")
    monkeypatch.setattr(cli, "getpass", lambda _="": "secret")
    monkeypatch.setattr(cli.user_service, "log_in", lambda u, p: (12, u) if p == "secret" else None)

    result = cli.log_in()

    assert result == (12, "alice")


def test_create_user_retries_duplicate_and_password_confirmation(monkeypatch):
    usernames = iter(["alice", "bob"])
    passwords = iter(["secret", "wrong", "secret"])

    monkeypatch.setattr("builtins.input", lambda _="": next(usernames))
    monkeypatch.setattr(cli, "getpass", lambda _="": next(passwords))

    calls = {"username_exists": 0, "create_user": []}

    def fake_username_exists(username):
        calls["username_exists"] += 1
        return username == "alice"

    def fake_create_user(username, password):
        calls["create_user"].append((username, password))
        return 7

    monkeypatch.setattr(cli.user_service, "username_exists", fake_username_exists)
    monkeypatch.setattr(cli.user_service, "create_user", fake_create_user)

    result = cli.create_user()

    assert result == (7, "bob", True)
    assert calls["username_exists"] == 2
    assert calls["create_user"] == [("bob", "secret")]


def test_create_user_retries_on_empty_username_and_password(monkeypatch):
    usernames = iter(["   ", "bob"])
    passwords = iter(["", "secret", "", "secret"])

    monkeypatch.setattr("builtins.input", lambda _="": next(usernames))
    monkeypatch.setattr(cli, "getpass", lambda _="": next(passwords))
    monkeypatch.setattr(cli.user_service, "username_exists", lambda _u: False)
    monkeypatch.setattr(cli.user_service, "create_user", lambda _u, _p: 11)

    result = cli.create_user()

    assert result == (11, "bob", True)


def test_ask_amount_creates_wallet(monkeypatch):
    monkeypatch.setattr(cli, "get_amount_input", lambda *_, **__: 100.0)

    captured = {}

    def fake_create_wallet(user_id, amount):
        captured["args"] = (user_id, amount)

    monkeypatch.setattr(cli.user_service, "create_wallet", fake_create_wallet)

    cli.ask_amount(3)

    assert captured["args"] == (3, 100.0)


def test_make_transaction_income_calls_service(monkeypatch):
    monkeypatch.setattr(cli, "get_amount_input", lambda *_, **__: 50.0)

    captured = {}

    def fake_add_income(user_id, wallet, amount):
        captured["args"] = (user_id, wallet, amount)

    monkeypatch.setattr(cli.services, "add_income", fake_add_income)
    wallet = DummyWallet(balance=10)

    cli.make_transaction(4, wallet, 1)

    assert captured["args"] == (4, wallet, 50.0)


def test_make_transaction_expense_insufficient_balance(monkeypatch):
    monkeypatch.setattr(cli, "get_amount_input", lambda *_, **__: 200.0)

    called = {"expense": False}

    def fake_add_expense(*_args, **_kwargs):
        called["expense"] = True

    monkeypatch.setattr(cli.services, "add_expense", fake_add_expense)
    wallet = DummyWallet(balance=100.0)

    cli.make_transaction(4, wallet, 2)

    assert called["expense"] is False


def test_make_transaction_expense_with_other_category(monkeypatch):
    monkeypatch.setattr(cli, "get_amount_input", lambda *_, **__: 25.0)
    entries = iter([str(len(cli.CATEGORIES) + 1), "coffee"])
    monkeypatch.setattr("builtins.input", lambda _="": next(entries))

    captured = {}

    def fake_add_expense(user_id, wallet, amount, category, description):
        captured["args"] = (user_id, wallet, amount, category, description)

    monkeypatch.setattr(cli.services, "add_expense", fake_add_expense)
    wallet = DummyWallet(balance=100.0)

    cli.make_transaction(5, wallet, 2)

    assert captured["args"] == (5, wallet, 25.0, "Other", "coffee")


def test_make_transaction_export_handles_empty_history(monkeypatch):
    monkeypatch.setattr(
        cli.services,
        "export_transactions_to_csv",
        lambda _user_id: (_ for _ in ()).throw(ValueError()),
    )

    # Should not raise
    cli.make_transaction(9, DummyWallet(balance=0), 4)


def test_change_user_retries_until_success(monkeypatch):
    calls = iter([None, (8, "alice")])
    monkeypatch.setattr(cli, "log_in", lambda: next(calls))
    monkeypatch.setattr(cli.user_service, "load_wallet", lambda _uid: DummyWallet(balance=77))

    user_id, wallet = cli.change_user()

    assert user_id == 8
    assert wallet.balance == 77


def test_make_transaction_save_balance_history_success(monkeypatch):
    called = {"ok": False}
    monkeypatch.setattr(
        cli.services,
        "save_balance_history",
        lambda _user_id: called.__setitem__("ok", True),
    )

    cli.make_transaction(10, DummyWallet(balance=0), 5)

    assert called["ok"] is True


def test_make_transaction_save_balance_history_empty(monkeypatch):
    monkeypatch.setattr(
        cli.services,
        "save_balance_history",
        lambda _user_id: (_ for _ in ()).throw(ValueError()),
    )

    # Should not raise
    cli.make_transaction(10, DummyWallet(balance=0), 5)


def test_make_transaction_save_transactions_success(monkeypatch):
    called = {"ok": False}
    monkeypatch.setattr(
        cli.services,
        "save_transactions",
        lambda _user_id: called.__setitem__("ok", True),
    )

    cli.make_transaction(10, DummyWallet(balance=0), 6)

    assert called["ok"] is True


def test_make_transaction_save_transactions_empty(monkeypatch):
    monkeypatch.setattr(
        cli.services,
        "save_transactions",
        lambda _user_id: (_ for _ in ()).throw(ValueError()),
    )

    # Should not raise
    cli.make_transaction(10, DummyWallet(balance=0), 6)
