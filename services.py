"""Wallet class"""
# TODO
# wallet class
CATEGORIES = ("Food", "House", "Bills", "Shopping", "Leisure", "Travel")

# convert currencies
# to do add API to get current value
def convert_currency(amount, from_c, to_c):
    if from_c == "UYU" and to_c == "USD":
        return amount*40.0

class Wallet:
    """Wallet class with income, expenses"""
    def __init__(self, user_id, balance=0):
        self.user_id = user_id
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
    def transaction(self, type, amount, currency="USD", category =None, description =None):
        # add amount to total if income
        if type == "Income":
            if currency == "USD":
                self.balance += amount
            else:
                self.balance += convert(amount, currency, "USD")
        elif type == "Expenses":
            # update total
            self.balance -= amount

def main():
    federico = Wallet(1, 1000)
    print(federico.categories)
    federico.transaction("Income", 500)
    federico.transaction("Expenses", 100, category='Travel')
    print(f"{federico.balance} USD")

if __name__ == '__main__':
    main()
