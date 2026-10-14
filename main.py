"""A personal expense tracker for recording and managing expenses."""

from datetime import date
import json


def show_menu():
    """Display the main menu options."""
    print("=============================")
    print("  PERSONAL EXPENSE TRACKER   ")
    print("=============================")
    print("1. Add expense")
    print("2. View expenses")
    print('3. View spending by category')
    print("4. View budget")
    print("5. View today's expenses")
    print("6. Change budget")
    print("7. Exit")
    print("8. View expenses by category")
    print("9. Delete an expense")
    print("10. Edit an expense")


def add_expense(expenses):
    """Add a new expense to the expense list."""
    print("\nAdding a new expense...")

    while True:
        expense_name = input("What did you spend money on? ")
        if expense_name.strip() == "":
            print("Expense name cannot be empty.")
            continue
        expense_category = input("What category is it? ")
        if expense_category.strip() == "":
            print("Category cannot be empty.")
            continue
        try:
            expense_amount = float(input("How much did you spend? "))
            if expense_amount <= 0:
                print("Expense amount must be greater than 0.")
                continue
            if expense_amount > 1000000:
                print("Expense amount too large.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue
        expense_date = date.today().strftime("%m/%d/%y")

        expenses.append({"name": expense_name, "category": expense_category,
                        "amount": expense_amount, "date": expense_date})
        save_expenses(expenses)
        print("\nExpense reorded!")
        print(f"your expense amount is {expense_amount: .2f}")

        another = input("\nWould you like to add another expense? (yes/no): ")
        if another.lower() != "yes":
            break


def get_budget():
    """Ask the user for a valid spending budget."""
    while True:
        try:
            budget = float(input("What is your budget? "))
            if budget < 0:
                print('Bugdet cannot be negative.')
                continue
            return budget
        except ValueError:
            print("Please enter a valid number.")


def calculate_total(expenses):
    """Calculate the total amount spent."""
    total = 0
    for expense in expenses:
        total = total + expense['amount']
    return total


def show_expenses(expenses):
    """Display all recorded expenses."""
    print("\nYour expenses:")

    for expense in expenses:
        print(
            f"-{expense['name']} | {expense['category']} |"
            f"{expense['amount']:.2f} | {expense['date']}")


def delete_expense(expenses):
    """Delete a selected expense."""
    if not expenses:
        print("No expense to delete.")
        return
    show_expenses(expenses)
    choice = input("Enter the number of the expense you want to delete: ")
    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a valid number")
        return
    if choice < 1 or choice > len(expenses):
        print("Invalid expense number.")
        return
    deleted_expense = expenses.pop(choice - 1)
    save_expenses(expenses)
    print(f"Deleted: {deleted_expense['name']}")


def edit_expense(expenses):
    """Edit the name, category, or amount of an expense."""
    if not expenses:
        print("No expense to edit.")
        return
    show_expenses(expenses)
    choice = input("Enter the number of the expense you want to edit: ")
    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a valid number")
        return
    if choice < 1 or choice > len(expenses):
        print("Invalid expense number.")
        return

    expense = expenses[choice - 1]
    print("What would you like to edit?")
    print("1. Expense name")
    print("2. Category")
    print("3. Amount")

    edit_choice = input("Enter your choice (1-3): ")
    if edit_choice not in ['1', '2', '3']:
        print("Invalid choice.")
        return

    if edit_choice == "1":
        new_name = input("Enter the new expense name: ")
        if not new_name.strip():
            print("Expense name cannot be empty.")
            return
        expense['name'] = new_name

    elif edit_choice == "2":
        new_category = input("Enter the new category: ")
        if not new_category.strp():
            print("Category cannot be empty.")
            return
        expense["category"] = new_category
    elif edit_choice == "3":
        try:
            new_amount = float(input("Enter new amount."))
        except ValueError:
            print("Please enter a valid amount.")
            return
        if new_amount <= 0 or new_amount > 1000000:
            print("Amount must be greater than 0 and no more than 1,000,000.")
            return
        expense["amount"] = new_amount
    save_expenses(expenses)
    print("Expense updated successfully! ")


def show_category_summary(expenses):
    """Summarize spending by category."""
    category_totals = {}

    for expense in expenses:
        category = expense['category']
        amount = expense['amount']

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    if not category_totals:
        print("\nNo expense recorded yet.")
        return
    print("\nSpending by category:")
    total = calculate_total(expenses)
    print(f"\nTotal spending: {total:.2f}")
    for category, amount in category_totals.items():
        percentage = (amount / total) * 100
        print(f"- {category}: {amount:.2f} ({percentage:.1f}%)")
    print(
        f"\nYour highest spending category is: {max(category_totals, key=category_totals.get)}")


def show_today_expenses(expenses):
    """Display expenses recorded today."""
    today = date.today().strftime("%m/%d/%y")
    print("\nToday's expense:")

    found = False
    today_total = 0

    for expense in expenses:
        if expense["date"] == today:
            print(
                f"- {expense['name']} | {expense['category']} | {expense['amount']:.2f}")
            today_total += expense['amount']
            found = True

    if not found:
        print("No expenses recorded today.")
    print(f"Total spent today: {today_total:.2f}")


def show_expenses_by_category(expenses):
    """Display expenses belonging to a selected category."""
    category = input("Enter a category: ").strip()

    found = False
    category_total = 0

    print(f"\nExpenses in {category}:")

    for expense in expenses:
        if expense['category'].lower() == category.lower():
            print(
                f"- {expense["name"]} | {expense['category']} |"
                f"{expense['amount']:.2f} | {expense['date']}")
            category_total += expense['amount']
            found = True

    if not found:
        print("No expenses found in that category.")
    if found:
        print(f"Total spent in {category}: {category_total:.2f}")


def save_expenses(expenses):
    """Save expenses to a JSON file."""
    with open("expenses.json", 'w', encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)
    print("Expense saved successfully!")


def load_expenses():
    """Load expenses from JSON file."""
    try:
        with open("expenses.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print('Warning: Your expenses file contains invalid data.')
        raise


name = input("Enter your name: ")
expenses = load_expenses()

print(f"\nWelcome, {name}! ")
print("Let's start tracking your expenses.")

budget = get_budget()

while True:
    show_menu()

    choice = input("Choose an option: ")
    if choice == "1":
        add_expense(expenses)
    elif choice == "2":
        show_expenses(expenses)
    elif choice == "3":
        show_category_summary(expenses)
    elif choice == "4":
        total = calculate_total(expenses)
        remaining_budget = budget-total
        print(f"\nYour budget: {budget:.2f}")
        print(f"Total spent: {total:.2f}")
        print(f"Remaining budget: {remaining_budget:.2f}")
        if remaining_budget < 0:
            print("⚠️ You have exceeded your budget!")
        elif remaining_budget <= budget * 0.2:
            print("Warning⚠️: You are close to your budget limit.")
        else:
            print("You are within your budget.")
    elif choice == "5":
        show_today_expenses(expenses)

    elif choice == "6":
        budget = get_budget()
        print(f"Budget updated to {budget:.2f}")
    elif choice == "7":
        print('Thank you for using the Expense Tracker. Goodbye!')

    elif choice == "8":
        show_expenses_by_category(expenses)
        break
    elif choice == "9":
        delete_expense(expenses)
    elif choice == '10':
        edit_expense(expenses)
    else:
        print('\n❌ Invalid choice. Please choose 1-8.')
print(f"You selected option {choice}.")
