
# banking_app.py

"""
Banking Application

This module provides a simple banking system with both command-line
and GUI interfaces.

Features:
- Deposit, Withdraw, Transfer funds
- Mobile phone top-up
- Custom error handling with exceptions
- GUI using Tkinter
"""

import tkinter as tk
from tkinter import messagebox

class InvalidInputError(Exception):
    """Exception raised for invalid user input."""
    pass

class TransferError(Exception):
    """Exception raised for issues during money transfers."""
    pass

class BankAccount:
    """Represents a user's bank account with basic banking functions."""

    def __init__(self, name, balance=0):
        """Initializes a new bank account."""
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        """Adds funds to the account."""
        if amount <= 0:
            raise InvalidInputError("Deposit amount must be greater than zero.")
        self.balance += amount

    def withdraw(self, amount):
        """Removes funds from the account."""
        if amount <= 0 or amount > self.balance:
            raise InvalidInputError("Invalid withdrawal amount.")
        self.balance -= amount

    def transfer(self, target_account, amount):
        """Transfers money to another account."""
        if amount <= 0 or amount > self.balance:
            raise TransferError("Transfer failed due to insufficient funds or invalid amount.")
        self.withdraw(amount)
        target_account.deposit(amount)

    def phone_top_up(self, mobile_number, amount):
        """Tops up a mobile phone balance."""
        if len(mobile_number) != 10 or not mobile_number.isdigit():
            raise InvalidInputError("Mobile number must be 10 digits.")
        self.withdraw(amount)
        return f"Mobile number {mobile_number} has been topped up with {amount}."

    def __str__(self):
        """Returns a string representation of the account."""
        return f"Account: {self.name}, Balance: {self.balance}"

def process_user_input(choice, account, accounts):
    """Handles user menu selections and executes corresponding operations."""
    try:
        if choice == '1':
            amount = float(input("Enter deposit amount: "))
            account.deposit(amount)
        elif choice == '2':
            amount = float(input("Enter withdrawal amount: "))
            account.withdraw(amount)
        elif choice == '3':
            target_name = input("Enter recipient name: ")
            amount = float(input("Enter amount to transfer: "))
            if target_name in accounts:
                account.transfer(accounts[target_name], amount)
            else:
                raise TransferError("Recipient account not found.")
        elif choice == '4':
            mobile = input("Enter 10-digit mobile number: ")
            amount = float(input("Enter top-up amount: "))
            print(account.phone_top_up(mobile, amount))
        elif choice == '5':
            print(account)
        elif choice == '6':
            print("Exiting application. Goodbye!")
            return False
        else:
            raise InvalidInputError("Invalid menu choice.")
    except (InvalidInputError, TransferError, ValueError) as e:
        print(f"Error: {e}")
    return True

def main():
    """Runs the banking application from the command line."""
    accounts = {
        'Tenzin Namgay Dendup': BankAccount('Tenzin Namgay Dendup', 1000),
        "Karma Dorji": BankAccount("Karma Dorji", 500),
    }
    current = accounts['Tenzin Namgay Dendup']
    while True:
        print("\n1. Deposit\n2. Withdraw\n3. Transfer\n4. Mobile Top-up\n5. Account Info\n6. Exit")
        choice = input("Choose an option: ")
        if not process_user_input(choice, current, accounts):
            break

class BankingGUI:
    """Graphical interface for interacting with a BankAccount."""

    def __init__(self, master, account, accounts):
        self.master = master
        self.account = account
        self.accounts = accounts

        master.title("Banking Application")
        master.geometry("350x400")

        self.label = tk.Label(master, text=f"Welcome, {self.account.name}", font=("Arial", 14))
        self.label.pack(pady=10)

        self.amount_label = tk.Label(master, text="Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack(pady=5)

        self.target_label = tk.Label(master, text="Target Account or Mobile Number:")
        self.target_label.pack()
        self.target_entry = tk.Entry(master)
        self.target_entry.pack(pady=5)

        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit, width=20)
        self.deposit_button.pack(pady=2)

        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw, width=20)
        self.withdraw_button.pack(pady=2)

        self.transfer_button = tk.Button(master, text="Transfer", command=self.transfer, width=20)
        self.transfer_button.pack(pady=2)

        self.topup_button = tk.Button(master, text="Top-Up Phone", command=self.top_up, width=20)
        self.topup_button.pack(pady=2)

        self.balance_button = tk.Button(master, text="Show Balance", command=self.show_balance, width=20)
        self.balance_button.pack(pady=2)

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.deposit(amount)
            messagebox.showinfo("Success", f"Deposited {amount} successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.withdraw(amount)
            messagebox.showinfo("Success", f"Withdrew {amount} successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transfer(self):
        try:
            amount = float(self.amount_entry.get())
            target_name = self.target_entry.get()
            if target_name == self.account.name:
                raise TransferError("Cannot transfer to the same account.")
            if target_name not in self.accounts:
                raise TransferError("Target account does not exist.")
            target = self.accounts[target_name]
            self.account.transfer(target, amount)
            messagebox.showinfo("Success", f"Transferred {amount} to {target_name}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def top_up(self):
        try:
            amount = float(self.amount_entry.get())
            mobile = self.target_entry.get()
            msg = self.account.phone_top_up(mobile, amount)
            messagebox.showinfo("Success", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_balance(self):
        messagebox.showinfo("Balance", f"{self.account.name}'s Balance: {self.account.balance}")
def select_account_gui(accounts):
    def launch_main_gui():
        selected = account_var.get()
        if selected not in accounts:
            messagebox.showerror("Error", "Please select a valid account")
            return
        selection_window.destroy()
        root = tk.Tk()
        BankingGUI(root, accounts[selected], accounts)
        root.mainloop()

    selection_window = tk.Tk()
    selection_window.title("Select Account")
    selection_window.geometry("300x200")

    tk.Label(selection_window, text="Choose your account:", font=("Arial", 12)).pack(pady=10)
    account_var = tk.StringVar(selection_window)
    account_var.set("Select")

    options = list(accounts.keys())
    dropdown = tk.OptionMenu(selection_window, account_var, *options)
    dropdown.pack(pady=10)

    tk.Button(selection_window, text="Continue", command=launch_main_gui).pack(pady=10)
    selection_window.mainloop()


if __name__ == "__main__":
    accounts = {
        "Tenzin Namgay Dendup": BankAccount("Tenzin Namgay Dendup", 1000),
        "Karma Dorji": BankAccount("Karma Dorji", 500),
    }
    select_account_gui(accounts)
