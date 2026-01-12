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
    def __init__(self, balance=0):
        self._balance = balance
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
    def add_income(self, amount):
    # TODO

    def add_expense(self, amount):
    # TODO
    

if __name__ == '__main__':
    main()
