# Wallet — Personal Finance Tracker

A command-line application for tracking income, expenses, and balance history. Supports multiple users, secure authentication, and data export to CSV and charts.

## Features

- Multi-user accounts with hashed password authentication
- Add income and categorized expense transactions
- Export full transaction history to CSV
- Generate a balance history line chart (PNG)
- Generate an expense category breakdown pie chart (PNG)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python project.py
   ```

## Usage

On startup, log in to an existing account or create a new one (password must be at least 8 characters). Once logged in, the main menu offers:

| Option | Action | Output |
|--------|--------|--------|
| 1 | Add income | Updates balance |
| 2 | Add expense (with category + description) | Updates balance |
| 3 | Switch user | Changes active session |
| 4 | Export transaction history | `data/<user_id>_transactions_history.csv` |
| 5 | Save balance history chart | `data/<user_id>_balance_history.png` |
| 6 | Save expense category chart | `data/<user_id>_transactions_categories.png` |
| 0 | Exit | |

All generated files are saved to the `data/` folder.

## Project Structure

```
project.py              # Entry point + utility functions (format_currency, validate_password, format_date)
test_project.py         # Tests for project.py utility functions
src/
  models.py             # Wallet and Transaction domain classes, convert_currency
  database.py           # SQLite repositories (WalletRepository, TransactionRepository)
  services.py           # Business logic: transactions, CSV export, chart generation
  user_service.py       # Authentication helpers (create_user, log_in, load_wallet)
  cli.py                # Interactive command-line interface
tests/
  conftest.py           # Shared pytest fixtures (in-memory test DB)
  test_models.py        # Unit tests for Wallet, Transaction, convert_currency
  test_database.py      # Unit tests for WalletRepository and TransactionRepository
  test_services.py      # Integration tests for service functions
  test_user_service.py  # Unit tests for auth and wallet helpers
  test_cli.py           # Unit tests for CLI input/output functions
data/                   # Generated output files (created at runtime)
```

## Design Decisions

- **Layered architecture**: `cli` → `services` → `database` → `models`. Each layer is independently testable and has a single responsibility.
- **Transaction as a value object**: The `Transaction` class validates type and amount before any DB or wallet operation, acting as the first line of defense.
- **Password hashing**: Uses `werkzeug.security` (PBKDF2-HMAC), the same library used by Flask.
- **Parameterized queries**: All DB access goes through `cs50.SQL`, which prevents SQL injection.
- **Absolute DB path**: The SQLite file is resolved relative to `database.py` so the program works correctly regardless of the working directory it is launched from.
- **Headless charts**: Matplotlib saves charts as PNG files rather than displaying them interactively, so the program works in environments without a display.
