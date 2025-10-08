import sqlite3, json
from datetime import datetime
import os

FILE = "s.txt"
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        try:
            users = json.load(f)
            if isinstance(users, dict):
                users = [users]
        except json.JSONDecodeError:
            users = []
else:
    users = []

login = False
k = input("New user (y/n): ").strip().lower()

if k == "n":
    x = input("Enter your username: ")
    y = input("Enter password: ")

    found = False
    for user in users:
        if user["username"] == x and user["password"] == y:
            print("✅ Login success")
            login = True
            found = True
            balance = user.get("balance", 0) 
            break
    if not found:
        print("❌ Wrong password or username not found")

else:
    x = input("Enter your username: ")
    y = input("Create a password: ")

    users.append({"username": x, "password": y, "balance": 0})

    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)

    print("✅ Account created successfully")
    balance = 0
    login = True

if login:
    conn = sqlite3.connect(f"{x}.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS money(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reason TEXT,
        amount REAL,
        date TEXT
    )
    """)

    monthly_expense_limit = 5

    def save_balance():
        for user in users:
            if user["username"] == x:
                user["balance"] = balance
                break
        with open(FILE, "w") as f:
            json.dump(users, f, indent=4)

    def show_balance():
        print(f"💰 Current Balance: {balance}")

    def show_transactions():
        cursor.execute("SELECT * FROM money")
        rows = cursor.fetchall()
        if not rows:
            print("No transactions yet.")
        for row in rows:
            print(row)

    def add_expense():
        global balance, monthly_expense_limit
        amount = int(input("How much did you spend? "))
        kind = input("Is it a stationary expense? (y/n): ")

        if kind.lower() == "y":
            reason = "Stationary"
            print("✅ No worries, stationary expense logged.")
        else:
            reason = "Other/Waste"
            monthly_expense_limit -= 1
            print("⚠️ Careful! Non-essential expense logged.")

        balance -= amount
        save_balance()  
        cursor.execute("INSERT INTO money(reason, amount, date) VALUES (?, ?, ?)",
                    (reason, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

    def add():
        global balance
        x = int(input("How much money want to add: "))
        balance += x
        save_balance()  

    def report():
        cursor.execute("SELECT * from money")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "reason": row[1],
                "amount": row[2],
                "date": row[3]
            })
        print(json.dumps(data, indent=4))
        conn.close()

    def menu():
        while True:
            print("\n------- Daily Expense Tracker -------")
            print("1. Show Balance")
            print("2. Show Transactions")
            print("3. Add Expense")
            print("4. Want a report?" )
            print("5. Add Money")
            print("6. Exit")

            choice = input("Choose an option: ")
            if choice == "1":
                show_balance()
            elif choice == "2":
                show_transactions()
            elif choice == "3":
                add_expense()
            elif choice == "4":
                report()
            elif choice == "5":
                add()
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice. Try again.")

    menu()
    conn.close()
