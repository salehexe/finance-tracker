# ============================================ ASTRANOM v0.1 ============================================
print("\n" + "="*40 + " FINANCE TRACKER " + "="*40)
import pwinput
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

try:
 account_file = open("account.txt", "r")
 content = account_file.read()
 lines = content.split("\n")
 username = lines[0]
 password = lines [1]
 account_file.close()
 # ---------- LOG IN ----------
 print("\n" + "-"*44 + " LOG IN " + "-"*44)

 max_attempts = 3
 attempts = 0

 # Login process for security
 while attempts < max_attempts:
     username_login = input("\nUsername: ")
     password_login = pwinput.pwinput(prompt="Password: ", mask="*")
    
     if username == username_login and password == password_login:
         print("Logged in successfully.")
         break # Exit the login loop
     else:
         attempts += 1
         print(f"Error: Wrong username or password, {max_attempts - attempts} attempts remaining.")

 if attempts == max_attempts:
     print("\n SYSTEM LOCKED: Maximum login attempts exceeded!")
     exit()

except FileNotFoundError:
 account_file = open("account.txt", "w")
    # ---------- CREATE ACCOUNT ----------
 print("\n" + "-"*39 + " CREATE AN ACCOUNT " + "-"*39)

  # Username validation
 while True:
     username = input("\nCreate an username: ")
     if len(username) < 5:
         print("Error: Username is too short (min 5 characters)!")
     elif len(username) > 12:
         print("Error: Username is too long (max 12 characters)!")
     else:
         print("Username set successfully.")
         break 

 # Password validation
 while True:
     password = pwinput.pwinput(prompt="\nCreate a password: ", mask="*")
     if len(password) < 7:
         print("Error: Password is too short! (min 7 characters)!")
     elif len(password) > 18:
         print("Error: Password is too long (max 18 characters)!")
     else:
         print("Password set successfully.")
         break
 account_file.write(f"{username}\n{password}") 
 account_file.close()

# ---------- FINANCE TRACKER ----------
class FinanceTracker:
   def __init__(self):
      self.incomes = []
      self.expenses = []
      self.total_income_categories = {"projects": 0, "retainers": 0, "consulting": 0, "maintenance": 0, "other": 0}
      self.total_expense_categories = {"ads": 0, "salaries": 0, "freelancers": 0, "software": 0, "office": 0, "other": 0}
      self.total_income = 0
      self.total_expense = 0
      self.balance = 0

   def add_income(self):
    print("\n" + " "*45 + " ADD INCOME ")
    while True:
        try:
         income_amount = float(input("\nIncome Amount ($): "))
         while True:
            income_category = input("Category (Projects/Retainers/Consulting/Maintenance/Other): ").strip().lower()
            if income_category == "projects" or income_category == "retainers" or income_category == "consulting" or income_category == "maintenance" or income_category == "other":
                print("Added")
                self.incomes.append({"Amount": income_amount, "Category": income_category})
                self.total_income_categories[income_category] += income_amount
                return
            else:
                print("Wrong format. Try again.")
        except ValueError:
            print("Something went wrong. Try again")

           
   def add_expense(self):
    print("\n" + " "*45 + " ADD EXPENSE ")
    while True:
        try:
         expense_amount = float(input("\nExpense Amount ($): "))
         while True:
            expense_category = input("Category (Ads/Salaries/Office/Software/Freelancers/Other): ").strip().lower()
            if expense_category == "ads" or expense_category == "salaries" or expense_category == "office" or expense_category == "software" or expense_category == "freelancers" or expense_category == "other":
                print("Added")
                self.expenses.append({"Amount": expense_amount, "Category": expense_category})
                self.total_expense_categories[expense_category] += expense_amount
                return
            else:
                print("Wrong format. Try again.")
        except ValueError:
            print("Something went wrong. Try again.")

   def profit(self):
    self.total_income = 0
    self.total_expense = 0
    for income in self.incomes:
        self.total_income += income["Amount"]
    for expense in self.expenses:
        self.total_expense += expense["Amount"]
    self.balance = self.total_income - self.total_expense
 
   def show_balance(self):
    print("\n" + " "*45 + " BALANCE ")
    self.profit()
    print(f"Current Balance: ${self.balance}")

   def show_report(self):
    print("\n" + " "*45 + " REPORT ")
    self.profit()
    print(f"Total income: ${self.total_income} \nTotal expense: ${self.total_expense} \n\nProfit: ${self.balance}" )
    if self.total_income > 0:
        print(f"Profit Margin: {self.balance / self.total_income * 100:.1f}%")
    else:
        print("Profit Margin: 0%")
    print("\nTotal Income Sources")
    for category, amount in self.total_income_categories.items():
        if self.total_income > 0:
         print(f"{category.title()} - ${amount} ({amount / self.total_income * 100:.1f}%)")
        else:
            print(f"{category.title()} - ${amount} (0%)")
    print("\nTotal Expense Sources")
    for category2, amount2 in self.total_expense_categories.items():
        if self.total_expense > 0:
         print(f"{category2.title()} - ${amount2} ({amount2 / self.total_expense * 100:.1f}%)")
        else:
            print(f"{category2.title()} - ${amount2} (0%)")

finance = FinanceTracker()

class CurrencyConverter:
    def __init__(self):
       self.base_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"

    def get_currency_rate(self, base_currency, target_currency):
        url = f"{self.base_url}/{base_currency}.json"
        response = requests.get(url)
    
        if response.status_code == 200:
         data = response.json()
         if target_currency in data[base_currency]:
          rate = data[base_currency][target_currency]
          return rate
         else:
            print("Error: 404")  
        else:
           print(f"Error: {response.status_code}")
    
    def convert(self, amount):
        print("\n" + " "*45 + " BALANCE EXCHANGE ")
        base_currency = "usd"
        target_currency = input("\nTarget Currency (EUR, TRY etc.): ").strip().lower()
        currency_rate = self.get_currency_rate(base_currency, target_currency)
           
        if currency_rate:
         exchanged_balance = amount * currency_rate
         print(f"\nYour balance in {target_currency.upper()}: {exchanged_balance:.2f}")

currency = CurrencyConverter()

class DataManager:
    def __init__(self, finance_tracker):
       self.ft = finance_tracker

    def save_data(self):
        file1 = open("incomes.json", "w")
        json.dump(self.ft.incomes, file1)
        file1.close()

        file2 = open("expenses.json", "w")
        json.dump(self.ft.expenses, file2)
        file2.close()

        file3 = open("income_categories.json", "w")
        json.dump(self.ft.total_income_categories, file3)
        file3.close()

        file4 = open("expense_categories.json", "w")
        json.dump(self.ft.total_expense_categories, file4)
        file4.close()

    def load_data(self):
        try:
         file1 = open("incomes.json", "r")
         self.ft.incomes = json.load(file1)
         file1.close()

         file2 = open("expenses.json", "r")
         self.ft.expenses = json.load(file2)
         file2.close()

         file3 = open("income_categories.json", "r")
         self.ft.total_income_categories = json.load(file3)
         file3.close()

         file4 = open("expense_categories.json", "r")
         self.ft.total_expense_categories = json.load(file4)
         file4.close()
        except FileNotFoundError:
           pass

data = DataManager(finance)

scheduler = BackgroundScheduler()
scheduler.add_job(data.save_data, 'interval', seconds = 1)
scheduler.start()

data.load_data(finance.incomes, finance.expenses, finance.total_income_categories, finance.total_expense_categories)
while True:
    print("\n" + "-"*45 + " MENU " + "-"*45)
    print("""1. Add Income
2. Add Expense
3. Show Balance
4. Show Report
5. Balance Currency Converter
6. Exit""")
    menu = input("\nSelect (1, 2, 3, 4, 5 or 6): ")
    if menu == "1":
        finance.add_income()
    elif menu == "2":
        finance.add_expense()
    elif menu == "3":
        finance.show_balance()
    elif menu == "4":
        finance.show_report()
    elif menu == "5":
        finance.show_balance()
        currency.convert(finance.balance)
    elif menu == "6":
        break
    else:
        print("Wrong format. Try again.")

