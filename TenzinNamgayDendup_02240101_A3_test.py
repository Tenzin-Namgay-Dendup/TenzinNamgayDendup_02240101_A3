
"""
Unit Tests for Banking Application

These tests verify correct behavior and handle edge cases for the BankAccount class.
"""

import unittest
from TenzinNamgayDendup_02240101_A3 import BankAccount, InvalidInputError, TransferError

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Creates sample accounts for testing."""
        self.acc = BankAccount("Test", 100)
        self.other = BankAccount("Other", 50)

    def test_deposit_valid(self):
        """Test depositing a positive amount."""
        self.acc.deposit(50)
        self.assertEqual(self.acc.balance, 150)

    def test_deposit_invalid(self):
        """Test depositing a negative amount."""
        with self.assertRaises(InvalidInputError):
            self.acc.deposit(-10)

    def test_withdraw_valid(self):
        """Test a successful withdrawal."""
        self.acc.withdraw(50)
        self.assertEqual(self.acc.balance, 50)

    def test_withdraw_invalid(self):
        """Test withdrawing more than available balance."""
        with self.assertRaises(InvalidInputError):
            self.acc.withdraw(200)

    def test_transfer_valid(self):
        """Test a valid fund transfer between accounts."""
        self.acc.transfer(self.other, 50)
        self.assertEqual(self.acc.balance, 50)
        self.assertEqual(self.other.balance, 100)

    def test_transfer_invalid(self):
        """Test an invalid transfer due to insufficient funds."""
        with self.assertRaises(TransferError):
            self.acc.transfer(self.other, 200)

    def test_phone_top_up_valid(self):
        """Test a valid mobile phone top-up."""
        msg = self.acc.phone_top_up("1234567890", 10)
        self.assertIn("topped up", msg)
        self.assertEqual(self.acc.balance, 90)

    def test_phone_top_up_invalid_number(self):
        """Test top-up with an invalid mobile number."""
        with self.assertRaises(InvalidInputError):
            self.acc.phone_top_up("1234", 10)

    def test_deposit_zero(self):
        """Test depositing zero amount."""
        with self.assertRaises(InvalidInputError):
            self.acc.deposit(0)

    def test_withdraw_zero(self):
        """Test withdrawing zero amount."""
        with self.assertRaises(InvalidInputError):
            self.acc.withdraw(0)

if __name__ == '__main__':
    unittest.main()
