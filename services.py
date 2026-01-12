"""Wallet class"""

import datetime
from database import db

# TODO 10/1
# check correct balance and values if not raise errors

CATEGORIES = ("Food", "House", "Bills", "Shopping", "Leisure", "Travel")

# convert currencies
# TODO add API to get current value
# https://exchangeratesapi.io/

def convert_currency(amount, from_c, to_c):
    if from_c == "UYU" and to_c == "USD":
        return amount*40.0

class Wallet:
    """Wallet class with income, expenses and stores on a database"""
    def __init__(self, user_id, balance=0):
        self.user_id = user_id
        self._balance = balance
        # create wallet for user
        db.execute(
        "INSERT INTO wallet (user_id, balance)"
        " VALUES (?, ?)", self.user_id, self._balance)
        # create category of expenses
        self.categories = CATEGORIES

    # getter
    @property
    def balance(self):
        return self._balance

    # setter
    # check if value is valid else raise error
    @balance.setter
    def balance(self, value):
        if not value:
            raise ValueError("please put value")
        self._balance = value
    # add transaction
    def transaction(self, tx_type, amount, currency="USD", category =None, description =None):
        # add transaction to db
        db.execute(
        "INSERT INTO transactions (user_id, tx_type, date, amount, currency, category, description)" \
        " VALUES (?, ?, ?, ?, ?, ?, ?)", 
        self.user_id,
        tx_type,
        datetime.date.today().isoformat(),
        amount, 
        currency,
        category, 
        description)
        # add amount to total if income
        if tx_type == "Income":
            if currency == "USD":
                self.balance += amount
            else:
                self.balance += convert_currency(amount, currency, "USD")
        elif tx_type == "Expenses":
            self.balance -= amount
        # update wallet
        db.execute("UPDATE wallet SET balance = ?" \
        " WHERE user_id = ?",
        self.balance,
        self.user_id)

def main():
    federico = Wallet(1, 1000)
    print(federico.categories)
    federico.transaction("Income", 500)
    federico.transaction("Expenses", 100, category='Travel')
    print(f"{federico.balance} USD")

if __name__ == '__main__':
    main()
