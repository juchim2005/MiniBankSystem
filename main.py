import pandas as pd
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt
import json
from user import User
from transactions import Transactions

def createuser():
    login = input("Enter login: ")
    password = input("Enter password: ")
    new_user = User(login, password)
    return new_user

def login(users):
    login = input("Enter login: ")
    password = input("Enter password: ")
    for user in users:
        if login == user.login and password == user.password:
            return user
    return

def add(user):
    filename = Transactions.initialize_csv(user)
    date = get_date("Enter the date of the transaction (dd-mm-yyy):", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    if category == "Expense" and user.balance - amount <0:
        print("Not enough money")
    else:
        Transactions.add_entry(filename,date, amount, category, description)
        if category == "Expense":
            user.balance -= amount
        else:
            user.balance += amount
    

def plot_transactions(df):
    df.set_index('date', inplace=True)

    income_df = (df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0))
    expense_df = (df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0))

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expenses')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    user = None
    filename = "users.json"
    users = []
    def initialize_json():
            with open(filename, "r", encoding="utf-8") as file:
                user_list = json.load(file)
            
            users = [User.from_dict(d) for d in user_list]
            return users
            

    users = initialize_json()

    def idkhowtonameit(user, users):
        while user == None:
        
            start = input("Do you want to Sign up(S)? or Log in(L)?: ")
            if start == "S":
                temp = True 
                user = createuser()
                for u in users:
                    if user.login == u.login:
                        print("User already exists")
                        temp = False
                        user = None
                        break
                if temp == True:
                    users.append(user)
                    with open(filename, "w", encoding="utf-8") as file:
                        json.dump([u.to_dict() for u in users], file, indent=4, ensure_ascii=False)
            elif start == "L":
                try:
                    user = login(users)
                    if user == None:
                        raise ValueError("User not found")
                except ValueError as e:
                    print(e)
            else:
                print("Wrong symbol")
        return user, users
    
    user, users = idkhowtonameit(user, users)

    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Log out")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add(user)
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyy): ")
            df = Transactions.get_transactions(user, start_date, end_date)
            if input("Do you want to see a plot (Y/N)?: ").upper() == "Y":
                print("test")
                plot_transactions(df)
        elif choice == "3":
            user = None
            user, users = idkhowtonameit(user, users)
        elif choice =="4":
            with open(filename, "w", encoding="utf-8") as file:
                json.dump([u.to_dict() for u in users], file, indent=4, ensure_ascii=False)
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()