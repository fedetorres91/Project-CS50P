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
    def __init__(self, user_id, total=0):
        self.user_id = user_id
        self._total = total;
        # create category of expenses
        self.categories = CATEGORIES

    # getter
    @property
    def total(self):
        return self._total

    # setter
    # check if value is valid else raise error
    @total.setter
    def total(self, value):
        if not value:
            raise ValueError("please put value")
        self._total = value
    # add income
    def add_income(self, amount, currency="USD"):
        # add amount to total
        if currency == "USD":
            self.total += amount
        else:
            self.total += convert(amount, currency, "USD")

    def make_expense(self, amount, currency='USD', category=None, description=None):
        # update total
        self.total -= amount

def main():
    federico = Wallet(1, 1000)
    print(federico.categories)
    federico.add_income(500)
    federico.make_expense(100, category='Travel')
    print(f"{federico.total} USD")

if __name__ == '__main__':
    main()
