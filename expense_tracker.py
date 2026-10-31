from datetime import date
from datetime import datetime                         
from pathlib import Path
import json
import math
import shutil

FILE_PATH=Path(__file__).parent / "expenses.json"

class ExpenseTracker:
    def __init__(self):
        self.expenses=[]
    def save_expenses(self):
        with FILE_PATH.open("w") as f:
            json.dump(self.expenses,f,indent=4)
            print("expense successfully saved")

    
    def load_expenses(self):
        print("File path:", FILE_PATH.resolve())
        print("File exists:", FILE_PATH.exists())
        try:
            if FILE_PATH.exists():
                with FILE_PATH.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                if not isinstance(data, list):
                    raise ValueError("Invalid expense data format")

                self.expenses = data
            else:
                self.expenses = []

        except json.JSONDecodeError:
            backup_path = FILE_PATH.with_suffix(".json.bak")
            shutil.copy2(FILE_PATH,backup_path)
            print(f"Corrupted file backed up to {backup_path}")
            self.expenses = []

        except UnicodeDecodeError as e:
            backup_path = FILE_PATH.with_suffix(".json.bak")
            shutil.copy2(FILE_PATH,backup_path)
            print(f"Unreadable file backed up to {backup_path}")
            self.expenses = []

        except ValueError as e:
            backup_path = FILE_PATH.with_suffix(".json.bak")
            print(f"Could not load expenses: {e}")
            shutil.copy2(FILE_PATH,backup_path)
            self.expenses = []


    def add_expenses(self, amount, category):
            if not math.isfinite(amount) or amount<=0:
                print("Invalid amount")
                return
            if not category.strip():
                print("Category cannot be empty.")
                return
            transaction ={
                "amount": amount, 
                "category": category.strip().lower(), 
                "date": date.today().strftime("%d-%m-%Y") }
            self.expenses.append(transaction)
            self.save_expenses()

    def view_expenses(self):
        if not self.expenses:   
            print("No current expense(s)")
        else:
            for expense in self.expenses:
                print(f'Amount: ₹{expense["amount"]}, Category: {expense["category"]}, Date: {expense["date"]}')

    def total_by_category(self):
        total={}
        if not self.expenses:
            print("No current expense(s)")
        else:
            for expense in self.expenses:
                    total[expense["category"]]=(total.get(expense["category"],0))+ ((expense["amount"]))
            for category, amount in total.items():
                    print(f'Amount: ₹{amount}, category: {category}')

    def delete_expense(self):
        if not self.expenses:
            print("No Expenses Found!")
            return

        for i, expense in enumerate(self.expenses, start=1):
            print(f"{i}. {expense['category']} - "f"₹{expense['amount']} - {expense['date']}")

        try:
            delete_e = int(input("Enter expense number to delete: "))

            if 1 <= delete_e <= len(self.expenses):
                self.expenses.pop(delete_e - 1)
                self.save_expenses()
                print("Expense deleted successfully!")
            else:
                print("Invalid expense number!")

        except ValueError:
            print("Please enter a valid integer.")
    
    def monthly_summary(self):
        monthly_sum={}
        for expense in self.expenses:
            date_obj=datetime.strptime(expense["date"],"%d-%m-%Y")
            month_year=(date_obj.year,date_obj.month)
            monthly_sum[month_year] = monthly_sum.get(month_year, 0) + expense["amount"]
        return monthly_sum

    def print_monthly_summary(self):
        result = self.monthly_summary()

        if not result:
            print("No expenses found!")
            return

        for year, month in sorted(result):
            amount = result[(year, month)]
            print(f"{month:02d}-{year}: ₹{amount:.2f}")


def main():
    tracker = ExpenseTracker()
    tracker.load_expenses() 
    print("Expense Tracker Started.") 
    while True:
        print("1.Add Expense \n2.View Expense \n3.Totals by category \n4.Delete Expense \n5.Monthly Summary \n6.Exit")
        try:
            choice=int(input("Enter your choice: "))
        except ValueError:
            print("Please, Enter a valid number")
            continue
        if choice==1:
            category=input("Enter the category: ")
            try:
                amount=float(input("Enter the amount: "))
            except ValueError:
                print("Please, Enter a valid amount")
                continue
            if amount<=0:
                print("Valid amount required!")
                continue
            tracker.add_expenses(amount,category)
        elif choice==2:
            tracker.view_expenses()
        elif choice==3:
            tracker.total_by_category()
        elif choice==4:
            tracker.delete_expense()
        elif choice==5:
            tracker.print_monthly_summary()
        elif choice==6:
            break
        else:
            print("Please, Enter a valid choice")
if __name__=="__main__":
    main()