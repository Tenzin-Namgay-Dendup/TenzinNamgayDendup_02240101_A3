# banking_app_gui.py
"""
Banking Application with GUI

GUI: Tkinter
Features:
- Login & Registration
- Deposit, Withdraw, Transfer, Top-up
- Account file saving
"""

import tkinter as tk
from tkinter import messagebox
import os
import random
from banking_core import BankAccount, InvalidInputError, TransferError

# --- File Handling ---
def save_account_to_file(account):
    with open("accounts.txt", "a") as f:
        f.write(f"{account.account_number},{account.name},{account.password},{account.balance}\n")

def load_accounts():
    accounts = {}
    if not os.path.exists("accounts.txt"):
        return accounts
    with open("accounts.txt", "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 4:
                acc_no, name, pwd, bal = parts
                accounts[acc_no] = BankAccount(acc_no, name, pwd, float(bal))
    return accounts

# --- Registration and Login GUI ---
class AuthGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking App Login")
        self.root.geometry("300x300")
        self.accounts = load_accounts()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Welcome to the Bank", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.frame, text="Login", command=self.login_window).pack(pady=5)
        tk.Button(self.frame, text="Register", command=self.register_window).pack(pady=5)

    def login_window(self):
        self.clear_frame()

        tk.Label(self.frame, text="Account Number:").pack()
        acc_entry = tk.Entry(self.frame)
        acc_entry.pack()

        tk.Label(self.frame, text="Password:").pack()
        pwd_entry = tk.Entry(self.frame, show="*")
        pwd_entry.pack()

        def login():
            acc = acc_entry.get()
            pwd = pwd_entry.get()
            if acc in self.accounts and self.accounts[acc].password == pwd:
                self.root.destroy()
                self.launch_main_gui(self.accounts[acc])
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        tk.Button(self.frame, text="Login", command=login).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.reset).pack()

    def register_window(self):
        self.clear_frame()

        tk.Label(self.frame, text="Full Name:").pack()
        name_entry = tk.Entry(self.frame)
        name_entry.pack()

        tk.Label(self.frame, text="Initial Deposit:").pack()
        bal_entry = tk.Entry(self.frame)
        bal_entry.pack()

        def register():
            name = name_entry.get()
            try:
                balance = float(bal_entry.get())
                if balance < 0:
                    raise InvalidInputError("Negative initial balance")
                acc_no = str(random.randint(10000, 99999))
                pwd = str(random.randint(1000, 9999))
                account = BankAccount(acc_no, name, pwd, balance)
                self.accounts[acc_no] = account
                save_account_to_file(account)
                messagebox.showinfo("Account Created", f"Account No: {acc_no}\nPassword: {pwd}")
                self.reset()
            except ValueError:
                messagebox.showerror("Error", "Enter valid numeric balance")
            except InvalidInputError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.frame, text="Register", command=register).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.reset).pack()

    def reset(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)
        self.__init__(self.root)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def launch_main_gui(self, account):
        accounts = load_accounts()
        root = tk.Tk()
        BankingGUI(root, account, accounts)
        root.mainloop()

# --- Main Banking GUI ---
class BankingGUI:
    def __init__(self, master, account, accounts):
        self.master = master
        self.account = account
        self.accounts = accounts
        master.title("Banking Application")
        master.geometry("400x450")

        tk.Label(master, text=f"Welcome, {self.account.name}", font=("Arial", 14)).pack(pady=10)

        tk.Label(master, text="Amount:").pack()
        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack(pady=5)

        tk.Label(master, text="Target Account / Mobile Number:").pack()
        self.target_entry = tk.Entry(master)
        self.target_entry.pack(pady=5)

        self.create_buttons(master)

    def create_buttons(self, master):
        tk.Button(master, text="Deposit", command=self.deposit, width=25).pack(pady=2)
        tk.Button(master, text="Withdraw", command=self.withdraw, width=25).pack(pady=2)
        tk.Button(master, text="Transfer", command=self.transfer, width=25).pack(pady=2)
        tk.Button(master, text="Top-Up Phone", command=self.top_up, width=25).pack(pady=2)
        tk.Button(master, text="Show Balance", command=self.show_balance, width=25).pack(pady=2)

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.deposit(amount)
            messagebox.showinfo("Success", f"Deposited {amount}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.withdraw(amount)
            messagebox.showinfo("Success", f"Withdrew {amount}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transfer(self):
        try:
            amount = float(self.amount_entry.get())
            target_acc = self.target_entry.get()
            if target_acc not in self.accounts:
                raise TransferError("Target account does not exist.")
            target = self.accounts[target_acc]
            self.account.transfer(target, amount)
            messagebox.showinfo("Success", f"Transferred {amount} to {target.name}")
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
        messagebox.showinfo("Balance", f"Current Balance: {self.account.balance}")

# --- Main App Launch ---
if __name__ == "__main__":
    root = tk.Tk()
    AuthGUI(root)
    root.mainloop()