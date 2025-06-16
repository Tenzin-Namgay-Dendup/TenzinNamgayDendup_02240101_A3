# banking_core.py
class InvalidInputError(Exception):
    pass

class TransferError(Exception):
    pass

class BankAccount:
    def __init__(self, account_number, name, password, balance=0):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidInputError("Deposit amount must be greater than zero.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            raise InvalidInputError("Invalid withdrawal amount.")
        self.balance -= amount

    def transfer(self, target_account, amount):
        if amount <= 0 or amount > self.balance:
            raise TransferError("Transfer failed due to insufficient funds or invalid amount.")
        self.withdraw(amount)
        target_account.deposit(amount)

    def phone_top_up(self, mobile_number, amount):
        if len(mobile_number) != 10 or not mobile_number.isdigit():
            raise InvalidInputError("Mobile number must be 10 digits.")
        self.withdraw(amount)
        return f"Mobile number {mobile_number} has been topped up with {amount}."
