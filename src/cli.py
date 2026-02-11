"""Command line interface for wallet application."""

from src import services
from src import user_service
from src.models import CATEGORIES
from getpass import getpass


def main():
    """Main entry point for the wallet CLI application.
    
    Handles the main event loop for user authentication, wallet management,
    and transaction operations. Allows users to log in, create accounts,
    add transactions, and export transaction history.
    """
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
                           "\nSelect option: ").strip()
            if option in ("1", "2", "0"):
                break
            print("Please select a valid option.")
        if option == "1":
            result = log_in()
            if result:
                user_id, username = result
                print(f"\n✓ Welcome back {username}!\n")
                wallet = user_service.load_wallet(user_id)
                logged_in = True
            else:
                print("\n✗ Incorrect username or password.\n")
        elif option == "2":
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
        if action == 0:
            print("Program exited.")
            break
        if action == 3:
            user_id, wallet = change_user()
            continue
        make_transaction(user_id, wallet, action)


def log_in():
    """Authenticate user with username and password.
    
    Prompts user to enter credentials and validates against the database.
    
    Returns:
        tuple: (user_id, username) if authentication succeeds, None otherwise.
    """
    print("\n" + "-" * 50)
    print("LOGIN".center(50))
    print("-" * 50 + "\n")
    while True:
        username = input("Enter username: ").strip()
        if username:
            break
        print("✗ Username cannot be empty.\n")

    while True:
        password = getpass("Enter password: ")
        if password:
            break
        print("✗ Password cannot be empty.\n")
    return user_service.log_in(username, password)


def create_user():
    """Create a new user account with username and password.
    
    Prompts for username (with duplicate checking), password, and confirmation.
    Validates that passwords match before creating account.
    
    Returns:
        tuple: (user_id, username, True) where True indicates successful login.
    """
    print("\n" + "-" * 50)
    print("CREATE USER".center(50))
    print("-" * 50 + "\n")
    while True:
        username = input("Create username: ").strip()
        if not username:
            print("✗ Username cannot be empty.\n")
            continue
        if user_service.username_exists(username):
            print("✗ Username already exists.\n")
            continue
        break

    # create password
    while True:
        password = getpass("Choose a password: ")
        if password:
            break
        print("✗ Password cannot be empty.\n")

    password_confirmed = False
    while not password_confirmed:
        confirmed = getpass("Confirm password: ")
        if not confirmed:
            print("✗ Password cannot be empty.\n")
            continue
        if confirmed != password:
            print("✗ Passwords don't match. Try again.\n")
        else:
            password_confirmed = True

    user_id = user_service.create_user(username, password)
    logged_in = True
    return (user_id, username, logged_in)


def ask_amount(user_id):
    """Prompt user for initial wallet balance and create wallet.
    
    Args:
        user_id (int): The ID of the user to create a wallet for.
    """
    amount = get_amount_input("Enter initial balance:\n", allow_zero=True)
    user_service.create_wallet(user_id, amount)


def get_amount_input(prompt="Enter amount: ", allow_zero=False):
    """Get and validate numeric amount input from user.
    
    Repeatedly prompts user until a valid positive number is entered.
    
    Args:
        prompt (str): The message to display when asking for input.
        allow_zero (bool): If True, allows zero as valid input; defaults to False.
    
    Returns:
        float: A valid positive amount entered by the user.
    """
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
    """Display main menu and get user's transaction choice.
    
    Repeatedly prompts until user selects a valid option:
    1. Add income, 2. Add expense, 3. Change user, 4. Save transactions, 5. Get balance history, 6. Save transaction categories summary, 0. Exit
    
    Returns:
        int: The user's selected action (0-6).
    """
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU".center(50))
        print("=" * 50 + "\n")
        action = input("1. Add an income\n"
                       "2. Add an expense\n"
                       "3. Change user\n"
                       "4. Save transaction history\n"
                       "5. Save balance history\n"
                       "6. Save transaction categories summary\n"
                       "0. Exit\n"
                       "\nSelect option: ")
        if action in ("0", "1", "2", "3", "4", "5", "6"):
            break
        print("Please select a valid option.")
    return int(action)


def change_user():
    """Authenticate and return a new active user and wallet."""
    while True:
        result = log_in()
        if result:
            user_id, username = result
            print(f"\n✓ Welcome back {username}!\n")
            return user_id, user_service.load_wallet(user_id)
        print("\n✗ Incorrect username or password.\n")


def make_transaction(user_id, wallet, action):
    """Process a financial transaction (income or expense).
    
    Handles income/expense entry with validation, category selection,
    and updates both the wallet and database.
    
    Args:
        user_id (int): The ID of the user making the transaction.
        wallet (Wallet): The user's wallet object to update.
        action (int): Transaction type: 1 for income, 2 for expense, 4 for export.
    """
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
        
        while True:
            category_choice = input(category_menu + "Select category: ").strip()
            if not category_choice.isdigit():
                print("Please enter a number.")
                continue
            choice_num = int(category_choice)
            if 1 <= choice_num <= len(CATEGORIES) + 1:
                break
            print("Please select a valid category number.")

        # Convert number to category name (IMPORTANT!)
        if choice_num <= len(CATEGORIES):
            category = CATEGORIES[choice_num - 1]
        else:
            category = "Other"

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

    elif action == 5:
        try:
            services.save_balance_history(user_id)
            print("\n✓ Balance history graph saved.\n")
        except ValueError:
            print("\n✗ Transaction history is empty.\n")

    elif action == 6:
        try:
            services.save_transactions(user_id)
            print("\n✓ Transaction categories summary saved.\n")
        except ValueError:
            print("\n✗ Transaction history is empty.\n")
    else:
        return
