"""Command line interface for wallet application."""

import services
import user_service
from models import CATEGORIES


def main():
    print("\n")
    print("Welcome to wallet. A command line interface program for tracking your expenses.\n"
          "Press CTRL+D/CTRL+C to exit. \n")
    logged_in = False
    wallet = None
    user_id = None

    while not logged_in:
        while True:
            option = input("1. Log in.\n"
                           "2. Create user.\n"
                           "0. Exit program.\n")
            if option in ("1", "2", "0"):
                break
        if int(option) == 1:
            result = log_in()
            if result:
                user_id, username = result
                print(f"Logged in. Welcome back {username}.")
                wallet = user_service.load_wallet(user_id)
                logged_in = True
            else:
                print("Incorrect username or password.\n")
        elif int(option) == 2:
            user_id, username, logged_in = create_user()
            print(f"User created successfully. Welcome {username}.\n")
            ask_amount(user_id)
            wallet = user_service.load_wallet(user_id)
        else:
            print("Program exited.")
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
    username, password = None, None
    while username is None:
        username = input("Enter username:\n")
    while password is None:
        password = input("Enter password:\n")
    return user_service.log_in(username, password)


def create_user():
    """Create user by entering username and password. Returns (user_id, username, True)."""
    print("Please create a user.")
    username, password = None, None

    while username is None:
        username = input("Create username:\n")
        if user_service.username_exists(username):
            print(f"Incorrect username. {username} already exists.")
            username = None

    # create password
    while password is None:
        password = input("Choose a password:\n")
    password_confirmed = False
    while not password_confirmed:
        password_confirmed = input("Confirm password:\n") == password

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
        action = input("Main Menu:\n"
                       "1. Add an income.\n"
                       "2. Add an expense.\n"
                       "3. Change user.\n"
                       "4. Save transaction history.\n"
                       "0. Exit.\n"
                       "Select option: ")
        if action in ("0", "1", "2", "3", "4"):
            break
    return int(action)


def make_transaction(user_id, wallet, action):
    """Make income or expense transaction."""
    if action == 1:
        amount = get_amount_input()
        services.add_income(user_id, wallet, amount)
        print(f"Successfully added {amount} to balance")
        return
    elif action == 2:
        amount = get_amount_input()
        
        # Build category menu from CATEGORIES constant
        category_menu = "Choose appropriate category of expense:\n"
        for i, cat in enumerate(CATEGORIES, 1):
            category_menu += f"{i}. {cat}.\n"
        category_menu += f"{len(CATEGORIES) + 1}. Other.\n"
        
        category = input(category_menu)
        description = input("Add description. Otherwise press enter: ")
        
        services.add_expense(user_id, wallet, amount, category=category, description=description)
        print(f"Successfully added {amount} expense")
        return
    # TODO save_transaction_history
    else:
        return


# TODO
# def save_transaction_history
# function that saves a csv file with transaction history of the user.
