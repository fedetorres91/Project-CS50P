"""Main program. Command line program that permits a user to create a wallet, 
make transactions, output transactions and wallet info on a csv file and some basic matplot graphs"""

from services import Wallet
from database import db
# TODO correct expcetions and raise errors
# TODO 12/1 make unit tests, create user/password
# TODO 13/1 output csv file

def main():
    print("\n")
    print("Welcome to wallet. A command line program for tracking your expenses.\n" \
    "Press CTRL+D/CTRL+C to exit. \n")
    # TODO
    # log in, create user
    logged_in = False
    wallet = None

    while not logged_in:
        while True:
            option = input("1. Log in.\n" \
            "2. Create user.\n"
            "0. Exit program.\n")
            if option in ("1", "2", "0"):
                break
        # log in
        if int(option) == 1:
            user_id = log_in()
            if user_id:
                print("Logged in. Welcome back.")
                wallet = create_wallet(user_id, db.execute("SELECT balance FROM wallet WHERE user_id = ?", user_id)[0]["balance"])
                logged_in = True
            else:
                print("Incorrect username or password.\n")
        # create user
        elif int(option) == 2:
            # create a user, store on database, inital amount and log in
            username, password, amount, wallet, logged_in = create_user()
    # ask for transaction.
    while True:
        action = ask_transaction()
        if action != 0:
            make_transaction(wallet, action)
        else:
            print("Program exited.")
            break
def log_in():
    """ask for username and password, returns user_id if correct user and password on db
    else returns none"""
    username, password = None, None
    while username is None:
        username = input("Enter username:\n")
    while password is None:
        password = input("Enter password:\n")
    try:
        user_id = db.execute("SELECT id FROM users WHERE username = ? AND password = ?", username, password)[0]["id"]
        return user_id
    except IndexError:
        pass
    return None
    
def create_user():
    """"creates user by  entering username, password and initial balance, creates wallt. 
    create a username and stores password, creates a new wallet"""
    print("Please create a user.")
    # take last_name, email (required), optional first_name, currency)
    username, password, amount = None, None, None
    while username is None:
        username = input("Create username:\n")
        if username is not None:
            valid_username = True
            # check username does not exist on db
            try:
                check_username = db.execute("SELECT username FROM users WHERE username = ?", username)[0]["username"]
                if check_username is not None:
                    valid_username = False
                    print(f"Incorrect username. {username} already exists.")
            except IndexError:
                pass
        if not valid_username:
            username = None
    # create password
    while password is None:
        password = input("Choose a password:\n")
    password_confirmed = False
    while not password_confirmed:
        password_confirmed = input("Confirm password:\n") == password
    print(f"User created succesfully. Welcome {username}.\n")
    while True:
        amount = input("Enter initial balance:\n")
        try:
            amount = float(amount)
            if amount < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    db.execute("INSERT INTO users (username, password) " \
    " VALUES (?, ?)", username, password)
    user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
    # create wallet
    wallet = create_wallet(user_id, amount)
    logged_in=True
    return(username, password, amount, wallet, logged_in)

def create_wallet(user_id, amount):
    """Creates a wallet instance given an user_id and initial amount"""
    wallet = Wallet(user_id, amount)
    print(f"Wallet created. Initial balance {amount}")
    return wallet

def ask_transaction():
    """Infinite loop except 0. Ask for transactions"""
    while True:
        action = input("Main Menu:\n"
        "1. Add an income.\n"
        "2. Add an expense.\n"
        "3. Change user.\n"
        "4. Save transaction history.\n"
        "0. Exit.\n"
        "Select option: ")
        if action in("0", "1", "2", "3", "4"):
            break
    return int(action)

def make_transaction(wallet, action):
    """Makes the transaction"""
    if action == 1:
        while True:
            amount = input("Enter amount: ")
            try:
                amount = float(amount)
                if amount <= 0:
                    print("Please enter a positive number. ")
                    continue
                break
            except ValueError:
                print("Please enter a valid number. ")
        wallet.transaction("Income", amount)
        print(f"Succesfully added {amount} to balance")
        return
    elif action == 2:
        while True:
            amount = input("Enter amount: ")
            try:
                amount = float(amount)
                if amount <= 0:
                    print("Please enter a non-negative number. ")
                    continue
                break
            except ValueError:
                print("Please enter a valid number. ")
        catergory = input("Choose appropiate category of expense.\n" \
        "1. Food.\n." \
        "2. House. \n" \
        "3. Bills. \n" \
        "4. Shopping. \n" \
        "6. Leisure. \n" \
        "7. Travel. \n" \
        "8. Other. \n")
        description = input("Add description. Otherwise press enter.")
        wallet.transaction("Expenses", amount, category, description)
        print(f"Succesfully added {amount} expense")
        return
    # TODO save_transaction_history 
    else:
        return
# TODO
# def_save_transaction_history
# function that saves a csv file with transaction history of the user.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram exited.")
        exit(0)
