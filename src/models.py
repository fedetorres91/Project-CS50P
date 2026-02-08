"""Wallet and transaction class"""

# TODO 10/1
# check correct balance and values if not raise errors

CATEGORIES = ("Food", "House", "Bills", "Shopping", "Leisure", "Travel")

# convert currencies
# TODO add API to get current value
# https://exchangeratesapi.io/

def convert_currency(amount, from_c, to_c):
    """Convert amount from one currency to another.
    
    Currently supports conversion from UYU (Uruguay Peso) to USD (US Dollar).
    
    Args:
        amount (float): The amount to convert.
        from_c (str): Source currency code (e.g., 'UYU').
        to_c (str): Target currency code (e.g., 'USD').
    
    Returns:
        float: The converted amount.
    
    Note:
        TODO: Integrate live exchange rate API for dynamic conversion rates.
    """
    if from_c == "UYU" and to_c == "USD":
        return amount*40.0

def valid_amount(amount):
    """Validate that an amount is a positive number.
    
    Args:
        amount: The value to validate.
    
    Returns:
        bool: True if amount is valid.
    
    Raises:
        ValueError: If amount is not a positive number (excludes booleans).
    """
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Amount must be a positive number.")
    return True

class Wallet:
    """Manages a user's financial balance and transactions.
    
    Tracks balance and provides methods to add income and expenses
    with automatic validation.
    """
    def __init__(self, balance=0):
        """Initialize a wallet with an optional starting balance.
        
        Args:
            balance (float): The initial balance; defaults to 0.
        
        Raises:
            ValueError: If balance is negative or not a number.
        """
        self.balance = balance

    # getter
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        """Set the wallet balance with validation.
        
        Args:
            value (float): The new balance value.
        
        Raises:
            ValueError: If value is negative or not a number.
        """
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Balance must be a non-negative number")
        self._balance = value

    def add_income(self, amount):
        """Add income to the wallet balance.
        
        Args:
            amount (float): The income amount to add.
        
        Raises:
            ValueError: If amount is not a positive number.
        """
        valid_amount(amount)
        self._balance += amount
    
    def add_expense(self, amount):
        """Deduct an expense from the wallet balance.
        
        Args:
            amount (float): The expense amount to deduct.
        
        Raises:
            ValueError: If amount is not positive or exceeds balance.
        """
        valid_amount(amount)
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount

class Transactions:
    """Represents a single financial transaction.
    
    Stores transaction details including type, amount, currency, category,
    and optional description.
    """
    def __init__(self, tx_type, amount, currency="USD", category=None, description=""):
        """Initialize a transaction record.
        
        Args:
            tx_type (str): Either 'income' or 'expense'.
            amount (float): The transaction amount (must be positive).
            currency (str): Currency code; defaults to 'USD'.
            category (str): Transaction category; optional.
            description (str): Additional transaction details; defaults to empty string.
        
        Raises:
            ValueError: If tx_type is not 'income' or 'expense', or if amount is invalid.
        """
        if tx_type not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'")
        valid_amount(amount)
        self.type = tx_type
        self.amount = amount
        self.currency = currency
        self.category = category
        self.description = description
