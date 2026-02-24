"""Entry point and utility functions for the wallet application."""

import logging
from datetime import datetime

import matplotlib
matplotlib.set_loglevel("warning")
logging.getLogger('matplotlib').setLevel(logging.WARNING)

from src.cli import main


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a number as a currency string.

    Args:
        amount (float): The monetary amount.
        symbol (str): Currency symbol; defaults to '$'.

    Returns:
        str: Formatted string, e.g. '$1,234.56'.
    """
    return f"{symbol}{amount:,.2f}"


def validate_password(password: str, min_length: int = 8) -> bool:
    """Check that a password meets the minimum length requirement.

    Args:
        password (str): The password to validate.
        min_length (int): Minimum number of characters required; defaults to 8.

    Returns:
        bool: True if valid.

    Raises:
        ValueError: If password is not a string or is shorter than min_length.
    """
    if not isinstance(password, str) or len(password) < min_length:
        raise ValueError(f"Password must be at least {min_length} characters.")
    return True


def format_date(date_str: str) -> str:
    """Format an ISO datetime string as MM/DD/YYYY.

    Args:
        date_str (str): An ISO 8601 datetime string (e.g. '2024-01-15T10:30:00').

    Returns:
        str: Date formatted as 'MM/DD/YYYY'.
    """
    return datetime.fromisoformat(date_str).strftime("%m/%d/%Y")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram exited.")
        exit(0)
