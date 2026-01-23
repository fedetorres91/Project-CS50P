import pytest
from models import Wallet, Transactions

# test wallet class

def test_correct_wallet_init():
    """Correct wallet initial balance"""
    w = Wallet(10)
    assert w.balance == 10

def test_wallet_zero_balance():
    """Test wallet with zero balance"""
    w = Wallet(0)
    assert w.balance == 0


def test_incorrect_wallet_init():
    """Incorrect wallet init balance"""
    with pytest.raises(ValueError):
        w = Wallet("1000")
    with pytest.raises(ValueError):
        w = Wallet(-35)

# income

def test_wallet_float_balance():
    """Test wallet accepts float values"""
    w = Wallet(10.5)
    w.add_income(5.25)
    assert w.balance == 15.75

def test_correct_income():
    """Income should correctly increase balance"""
    w = Wallet(0)
    w.add_income(10)
    assert w.balance == 10

def test_incorrect_income():
    """Checks incorrect income amount"""
    w = Wallet(0)
    with pytest.raises(TypeError):
        w.add_income()
    with pytest.raises(ValueError):
        w.add_income("hola")
    with pytest.raises(ValueError):
        w.add_income(True)
    with pytest.raises(ValueError):
        w.add_income(-5)

# expenses
def test_correct_expense():
    """Expense should correctly decrease balance"""
    w = Wallet(100)
    w.add_expense(10)
    assert w.balance == 90

def test_exact_expense():
    """Test expense that matches balance exactly"""
    w = Wallet(50)
    w.add_expense(50)
    assert w.balance == 0

def test_incorrect_expense():
    """Checks incorrect expense amount"""
    w = Wallet(100)
    with pytest.raises(TypeError):
        w.add_expense()
    with pytest.raises(ValueError):
        w.add_expense(500)
    with pytest.raises(ValueError):
        w.add_expense("50")
    with pytest.raises(ValueError):
        w.add_expense(-10)

# test transatcions

def test_correct_transaction():
    t1 = Transactions("income", 10)
    t2 = Transactions("expense", 20)
    assert t1.amount == 10
    assert t2.amount == 20
def test_incorrect_tx_type():
    with pytest.raises(ValueError):
        t = Transactions("gastos", 10)
def test_incorrect_amount():
    with pytest.raises(TypeError):
        t = Transactions("income")
    with pytest.raises(ValueError):
        t = Transactions("income", "ten")



