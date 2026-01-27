"""Command line interface for wallet application."""

from src import services
from src import user_service
from src.models import CATEGORIES
from getpass import getpass


def main():
    print("\n" + "="*50)
    print("💰 Welcome to Wallet 💰".center(50))
    print("="*50)
    print("\nA CLI program for tracking your expenses.")
    print("Press CTRL+D/CTRL+C to exit.\n")
    logged_in = False
    wallet = None
    user_id = None

    while not logged_in:
        while True:
            print("-" * 50)
            option = input("1. Log in\n"
                           "2. Create user\n"
                           "0. Exit program\n"
                           "\nSelect option: ")
            if option in ("1", "2", "0"):
                break
        if int(option) == 1:
            result = log_in()
            if result:
                user_id, username = result
                print(f"\n✓ Welcome back {username}!\n")
                wallet = user_service.load_wallet(user_id)
                logged_in = True
            else:
                print("\n✗ Incorrect username or password.\n")
        elif int(option) == 2:
            user_id, username, logged_in = create_user()
            print(f"\n✓ User created successfully. Welcome {username}!\n")
            ask_amount(user_id)
            wallet = user_service.load_wallet(user_id)
        else:
            print("\n👋 Program exited.\n")
            return

    # ask for transaction.
    while True:
        action = ask_transaction()
        if action != 0:
            make_transaction(user_id, wallet, action)
        else:
            print("Program exited.")
            break


def log_in():
    """Ask for username and password, returns (user_id, username) if correct, else None."""
    print("\n" + "-" * 50)
    print("LOGIN".center(50))
    print("-" * 50 + "\n")
    username, password = None, None
    while username is None:
        username = input("Enter username: ")
    while password is None:
        password = getpass("Enter password: ")
    return user_service.log_in(username, password)


def create_user():
    """Create user by entering username and password. Returns (user_id, username, True)."""
    print("\n" + "-" * 50)
    print("CREATE USER".center(50))
    print("-" * 50 + "\n")
    username, password = None, None

    while username is None:
        username = input("Create username: ")
        if user_service.username_exists(username):
            print(f"✗ Username already exists.\n")
            username = None

    # create password
    while password is None:
        password = getpass("Choose a password: ")
    password_confirmed = False
    while not password_confirmed:
        confirmed = getpass("Confirm password: ")
        if confirmed != password:
            print("✗ Passwords don't match. Try again.\n")
        else:
            password_confirmed = True

    user_id = user_service.create_user(username, password)
    logged_in = True
    return (user_id, username, logged_in)


def ask_amount(user_id):
    """Ask for initial balance and create wallet."""
    amount = get_amount_input("Enter initial balance:\n", allow_zero=True)
    user_service.create_wallet(user_id, amount)


def get_amount_input(prompt="Enter amount: ", allow_zero=False):
    """Get and validate amount input from user."""
    while True:
        amount = input(prompt)
        try:
            amount = float(amount)
            if amount < 0 or (not allow_zero and amount <= 0):
                print("Please enter a positive number.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")


def ask_transaction():
    """Infinite loop except 0. Ask for transactions."""
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU".center(50))
        print("=" * 50 + "\n")
        action = input("1. Add an income\n"
                       "2. Add an expense\n"
                       "3. Change user\n"
                       "4. Save transaction history\n"
                       "0. Exit\n"
                       "\nSelect option: ")
        if action in ("0", "1", "2", "3", "4"):
            break
    return int(action)


def make_transaction(user_id, wallet, action):
    """Make income or expense transaction."""
    if action == 1:
        amount = get_amount_input("\nEnter income amount: ")
        try:
            services.add_income(user_id, wallet, amount)
            print(f"\n✓ Successfully added ${amount:.2f} to balance\n")
        except ValueError as e:
            print(f"\n✗ Error: {e}\n")
        return

    elif action == 2:
        amount = get_amount_input("\nEnter expense amount: ")
        
        # Validate balance before asking for category/description
        if amount > wallet.balance:
            print(f"\n✗ Insufficient balance! Current balance: ${wallet.balance:.2f}\n")
            return
        
        # Build category menu from CATEGORIES constant
        print("\nChoose category:")
        category_menu = ""
        for i, cat in enumerate(CATEGORIES, 1):
            category_menu += f"{i}. {cat}\n"
        category_menu += f"{len(CATEGORIES) + 1}. Other\n"
        
        category = input(category_menu + "Select category: ")
        description = input("Add description (or press enter to skip): ")
        
        try: 
            services.add_expense(user_id, wallet, amount, category=category, description=description)
            print(f"\n✓ Successfully added ${amount:.2f} expense\n")
        except ValueError as e:
            print(f"\n✗ Error: {e}\n")
        return
    
    elif action == 4:
        try:
            services.export_transactions_to_csv(user_id)
            print("\n✓ Transaction history saved.\n")
        except ValueError:
            print("\n✗ Transaction history is empty.\n")

    else:
        return


# TODO
# print matplot lib of transaction category and balance history