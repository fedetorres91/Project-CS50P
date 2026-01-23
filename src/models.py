"""Wallet and transaction class"""

# TODO 10/1
# check correct balance and values if not raise errors

CATEGORIES = ("Food", "House", "Bills", "Shopping", "Leisure", "Travel")

# convert currencies
# TODO add API to get current value
# https://exchangeratesapi.io/

def convert_currency(amount, from_c, to_c):
    if from_c == "UYU" and to_c == "USD":
        return amount*40.0

# check amount valid positive number
def valid_amount(amount):
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Amount must be a positive number.")
    return True

class Wallet:
    """Wallet class - manages balance only"""
    def __init__(self, balance=0):
        self.balance = balance

    # getter
    @property
    def balance(self):
        return self._balance

    # setter
    # check if value is valid else raise error
    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Balance must be a non-negative number")
        self._balance = value

    def add_income(self, amount):
        """Add income to balance"""
        # check correct amount
        valid_amount(amount)
        self._balance += amount
    
    def add_expense(self, amount):
        """Add income to balance"""
        valid_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount

class Transactions:
    """Represents a single transaction"""
    def __init__(self, tx_type, amount, currency="USD", category=None, description=""):
        if tx_type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")
        valid_amount(amount)
        self.type = tx_type
        self.amount = amount
        self.currency = currency
        self.category = category
        self.description = description
