"""Main program. Command line program that permits a user to create a wallet, 
make transactions, output transactions and wallet info on a csv file and some matplot graphs"""

from services import Wallet
from database import db
# TODO correct expections and raise errors

def main():
    print("\n")
    print("Welcome to wallet. A command line program for tracking income and expenses\n" \
    "Enter your last name and name. Then select option by pressing the number. \n")
    # create user
    last_name, email, amount = create_user()
    db.execute("INSERT INTO users (last_name, email) " \
    " VALUES (?, ?)", last_name, email)
    user_id = db.execute("SELECT id FROM users WHERE email = ?", email)[0]["id"]
    # create wallet
    wallet = create_wallet(user_id, last_name, amount)
    while True:
        action = ask_transaction()
        if action != 0:
            make_transaction(wallet, action)
        else:
            print("Program exited.")
            break

def create_user():
    """"creates user by  entering last name, email and initial balance"""
    # take last_name, email (required), optional first_name, currency)
    last_name, email, amount = None, None, None
    while last_name is None:
        last_name = input("Enter last name:\n")
    while email is None:
        email = input("Enter e-mail:\n")
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
    return(last_name, email, amount)

def create_wallet(user_id, last_name, amount):
    """Creates a wallet instance given an user_id and initial amount"""
    wallet = Wallet(user_id, amount)
    print(f"{last_name}'s Wallet created. Initial balance {amount}")
    return wallet

def ask_transaction():
    """Infinite loop except 0. Ask for transactions"""
    while True:
        action = input("Please enter the following option:\n"
        "1 . Adding an income.\n"
        "2 . Adding an expense.\n"
        "3 . Changing user.\n"
        "0. Exit.\n")
        if action in("0", "1", "2", "3"):
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
                    print("Please enter a positive number")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        wallet.transaction("Income", amount)
        print(f"Succesfully added {amount} to balance")
        return
    elif action == 2:
        while True:
            amount = input("Enter amount: ")
            try:
                amount = float(amount)
                if amount <= 0:
                    print("Please enter a non-negative number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        wallet.transaction("Expenses", amount)
        print(f"Succesfully added {amount} expense")
        return
    else:
        return
if __name__ == "__main__":
    main()
