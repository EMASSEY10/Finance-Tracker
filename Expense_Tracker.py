import csv
import datetime
import calendar
import os

class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __str__(self):
        return f"{self.name} ({self.category}): ${self.amount:.2f}"

def save_user_expense(expense, expense_file_path):
    """Saves an expense to a CSV file."""
    try:
        # Check if the file exists; if not, create it and add headers
        file_exists = os.path.exists(expense_file_path)
        with open(expense_file_path, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:  # Write header only if the file doesn't exist
                writer.writerow(["name", "category", "amount"])  # Add headers to CSV if file is empty
            writer.writerow([expense.name, expense.category, expense.amount])  # Write expense data
    except OSError as e:
        print(f"Error saving expense: {e}")

def track_category_budget(expenses):
    """Track spending per category."""
    # Define fixed category budgets
    category_budgets = {
        "Food": 300,
        "Gas": 100,
        "Rent": 1000,
        "Coffee": 50,
        "Subscription": 75,
        "Loan": 200,
        "Utilities": 150,
        "Misc": 100
    }

    expenses_by_category = {category: 0 for category in category_budgets}
    for expense in expenses:
        if expense.category in expenses_by_category:
            expenses_by_category[expense.category] += expense.amount
        else:
            print(f"Warning: Category '{expense.category}' not found in predefined categories.")

    print("\nCategory Spending vs Budget:")
    for category, budget in category_budgets.items():
        spent = expenses_by_category.get(category, 0)  # Safely handle missing categories
        remaining = budget - spent
        print(f"{category}: Budget = ${budget:.2f}, Spent = ${spent:.2f}, Remaining = ${remaining:.2f}")

def summarize_expense(expense_file_path, overall_budget):
    """Summarizes and displays expenses from the CSV file."""
    expenses = []
    try:
        with open(expense_file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                if len(row) == 3:
                    expense = Expense(row[0], row[1], float(row[2]))
                    expenses.append(expense)
                else:
                    print(f"Skipping invalid row: {row}")
    except IOError as e:
        print(f"Error reading the file: {e}")
        return

    # Calculating total spent
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = overall_budget - total_spent

    print("\nExpenses Summary:")
    print(f"Total spent: ${total_spent:.2f}")
    print(f"Remaining budget: ${remaining_budget:.2f}")

    # Track category budgets
    track_category_budget(expenses)

    # Calculate remaining days in the month
    now = datetime.date.today()
    _, last_day = calendar.monthrange(now.year, now.month)
    remaining_days = last_day - now.day

    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
    print(f"Daily budget: ${daily_budget:.2f}")
    print(f"Remaining days in the month: {remaining_days}")

def get_user_expense():
    """Gets expense details from the user."""
    expense_name = input("Enter expense name: ")

    # Validating expense amount
    while True:
        try:
            expense_amount = float(input("Enter expense amount: $"))
            if expense_amount <= 0:
                print("Amount should be greater than zero. Try again.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    # Validating category selection
    expense_categories = [
        "Food", 
        "Gas", 
        "Rent", 
        "Coffee",
        "Subscription", 
        "Loan", 
        "Utilities",
        "Misc"
    ]

    while True:
        print("\nSelect expense category:")
        for i, category_name in enumerate(expense_categories, start=1):
            print(f" {i}. {category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        try:
            selected_index = int(input(f"Enter category number {value_range}: "))
            if 1 <= selected_index <= len(expense_categories):
                selected_category = expense_categories[selected_index - 1]
                return Expense(name=expense_name, category=selected_category, amount=expense_amount)
            else:
                print(f"Invalid category number {value_range}. Try again.")
        except ValueError:
            print(f"Invalid input. Please enter a valid number between 1 and {len(expense_categories)}.")

def display_menu():
    """Displays the main menu of the app."""
    print("\nSelect an option:")
    print("1. Add an expense")
    print("2. View summary")
    print("3. Exit")
    return input("Enter your choice: ")  

def main():
    """Entry point of the program."""
    print("Welcome to the Finance Tracker")

    # Get the user-defined overall budget and convert to float
    while True:
        try:
            budget = float(input("Enter your monthly budget: $"))
            if budget >= 0:
                break
            else:
                print("Budget should be a non-negative number. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    expense_file_path = "expenses.csv"

    while True:
        choice = display_menu()
        if choice == "1":
            expense = get_user_expense()
            if expense:
                save_user_expense(expense, expense_file_path)
            print(f"\nExpense '{expense.name}' saved successfully!")
        elif choice == "2":
            summarize_expense(expense_file_path, budget)
        elif choice == "3":
            print("\nExiting the app. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")
            
if __name__ == "__main__":
    main()
