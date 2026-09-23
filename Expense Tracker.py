from datetime import date
import json

class ExpenseTracker:
    def __init__(self):
        self.expenses=[]
    def save_expenses(self):
        with open("expenses.json","w") as f:
            json.dump(self.expenses,f)

    def load_expenses(self):
        try:
            with open("expenses.json","r") as f:
                self.expenses=json.load(f)
        except FileNotFoundError:
            self.expenses=[]

    def add_expenses(self, amount, category):
        transaction ={
            "amount": abs(amount), 
            "category": category.lower(), 
            "date": date.today().strftime("%d-%m-%Y") }
        self.expenses.append(transaction)

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


def main():
    tracker = ExpenseTracker()
    tracker.load_expenses()  
    while True:
        print("1.Add Expense \n2.View Expence \n3.Totals by category \n4.Exit")
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
            tracker.add_expenses(amount,category)
        elif choice==2:
            tracker.view_expenses()
        elif choice==3:
            tracker.total_by_category()
        elif choice==4:
            tracker.save_expenses()
            break
        else:
            print("Please, Enter a valid choice")

main()