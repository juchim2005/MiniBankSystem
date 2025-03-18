import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
class Transactions:

    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    def __init__(self, user):
        self.user = user
        self.CSV_FILE = self.initialize_csv(user)

    @classmethod
    def initialize_csv(cls, user):
        filename = f"{user.login}_transactions.csv"
        try:
            pd.read_csv(filename)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(filename, index=False)
        return filename
        

    @classmethod
    def add_entry(cls,filename, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry addes successfully")


    @classmethod
    def get_transactions(cls, user,  start_date, end_date):
        df = pd.read_csv(f"{user.login}_transactions.csv")
        df["date"] = pd.to_datetime(df["date"], format=Transactions.FORMAT)
        start_date = datetime.strptime(start_date, Transactions.FORMAT)
        end_date = datetime.strptime(end_date, Transactions.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found")
        else:
            print(
                f"Transactions from {start_date.strftime(Transactions.FORMAT)} to {end_date.strftime(Transactions.FORMAT)}"
                )
            print(
                filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(Transactions.FORMAT)})
                )
            
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Toral Income: {total_income:.2f}zł")
            print(f"Toral Expense: {total_expense:.2f}zł")
            print(f"Net savings: {(total_income-total_expense):.2f}zł")
        return filtered_df