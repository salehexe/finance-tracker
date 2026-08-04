# ============================================ ASTRANOM v0.1 ============================================
print("\n" + "="*40 + " FINANCE TRACKER " + "="*40)
import pwinput
import json

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
incomes = []
expenses = []
total_income_categories = {"projects": 0, "retainers": 0, "consulting": 0, "maintenance": 0, "other": 0}
total_expense_categories = {"ads": 0, "salaries": 0, "freelancers": 0, "software": 0, "office": 0, "other": 0}
total_income = 0
total_expense = 0
balance = 0

def add_income():
    global incomes, total_income_categories
    print("\n" + " "*45 + " ADD INCOME ")
    while True:
        try:
         income_amount = float(input("\nIncome Amount ($): "))
         while True:
            income_category = input("Category (Projects/Retainers/Consulting/Maintenance/Other): ").lstrip().lower()
            if income_category == "projects" or income_category == "retainers" or income_category == "consulting" or income_category == "maintenance" or income_category == "other":
                print("Added")
                incomes.append({"Amount": income_amount, "Category": income_category})
                total_income_categories[income_category] += income_amount
                return
            else:
                print("Wrong format. Try again.")
        except ValueError:
            print("Something went wrong. Try again")

           
def add_expense():
    global expenses, total_expense_categories
    print("\n" + " "*45 + " ADD EXPENSE ")
    while True:
        try:
         expense_amount = float(input("\nExpense Amount ($): "))
         while True:
            expense_category = input("Category (Ads/Salaries/Office/Software/Freelancers/Other): ").lstrip().lower()
            if expense_category == "ads" or expense_category == "salaries" or expense_category == "office" or expense_category == "software" or expense_category == "freelancers" or expense_category == "other":
                print("Added")
                expenses.append({"Amount": expense_amount, "Category": expense_category})
                total_expense_categories[expense_category] += expense_amount
                return
            else:
                print("Wrong format. Try again.")
        except ValueError:
            print("Something went wrong. Try again.")

def profit():
    global balance, total_income, total_expense
    total_income = 0
    total_expense = 0
    for income in incomes:
        total_income += income["Amount"]
    for expense in expenses:
        total_expense += expense["Amount"]
    balance = total_income - total_expense
 
def show_balance():
    print("\n" + " "*45 + " BALANCE ")
    profit()
    print(f"Current Balance: ${balance}")

def show_report():
    print("\n" + " "*45 + " REPORT ")
    profit()
    print(f"Total income: ${total_income} \nTotal expense: ${total_expense} \n\nProfit: ${balance}" )
    if total_income > 0:
        print(f"Profit Margin: {balance / total_income * 100:.1f}%")
    else:
        print("Profit Margin: 0%")
    print("\nTotal Income Sources")
    for category, amount in total_income_categories.items():
        if total_income > 0:
         print(f"{category.title()} - ${amount} ({amount / total_income * 100:.1f}%)")
        else:
            print(f"{category.title()} - ${amount} (0%)")
    print("\nTotal Expense Sources")
    for category2, amount2 in total_expense_categories.items():
        if total_expense > 0:
         print(f"{category2.title()} - ${amount2} ({amount2 / total_expense * 100:.1f}%)")
        else:
            print(f"{category2.title()} - ${amount2} (0%)")
           

def save_data():
    file1 = open("incomes.json", "w")
    json.dump(incomes, file1)
    file1.close()

    file2 = open("expenses.json", "w")
    json.dump(expenses, file2)
    file2.close()

    file3 = open("income_categories.json", "w")
    json.dump(total_income_categories, file3)
    file3.close()

    file4 = open("expense_categories.json", "w")
    json.dump(total_expense_categories, file4)
    file4.close()

def load_data():
    global incomes, expenses, total_income_categories, total_expense_categories
    try:
     file1 = open("incomes.json", "r")
     incomes = json.load(file1)
     file1.close()

     file2 = open("expenses.json", "r")
     expenses = json.load(file2)
     file2.close()

     file3 = open("income_categories.json", "r")
     total_income_categories = json.load(file3)
     file3.close()

     file4 = open("expense_categories.json", "r")
     total_expense_categories = json.load(file4)
     file4.close()
    except FileNotFoundError:
        pass

load_data()
while True:
    print("\n" + "-"*45 + " MENU " + "-"*45)
    print("""1. Add Income
2. Add Expense
3. Show Balance
4. Show Report
5. Save and Exit""")
    menu = input("\nSelect (1, 2, 3, 4 or 5): ")
    if menu == "1":
        add_income()
    elif menu == "2":
        add_expense()
    elif menu == "3":
        show_balance()
    elif menu == "4":
        show_report()
    elif menu == "5":
        save_data()
        break
    else:
        print("Wrong format. Try again.")

