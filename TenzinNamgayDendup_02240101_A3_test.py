
"""
Unit Tests for Banking Application

These tests verify correct behavior and handle edge cases for the BankAccount class.
"""

import unittest
from TenzinNamgayDendup_02240101_A3 import BankAccount, InvalidInputError, TransferError


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.acc = BankAccount("00001", "Test", "1234", 100)
        self.other = BankAccount("00002", "Other", "5678", 50)

    def test_deposit_valid(self):
        self.acc.deposit(50)
        self.assertEqual(self.acc.balance, 150)

    def test_deposit_invalid(self):
        with self.assertRaises(InvalidInputError):
            self.acc.deposit(-10)

    def test_withdraw_valid(self):
        self.acc.withdraw(50)
        self.assertEqual(self.acc.balance, 50)

    def test_withdraw_invalid(self):
        with self.assertRaises(InvalidInputError):
            self.acc.withdraw(200)

    def test_transfer_valid(self):
        self.acc.transfer(self.other, 50)
        self.assertEqual(self.acc.balance, 50)
        self.assertEqual(self.other.balance, 100)

    def test_transfer_invalid(self):
        with self.assertRaises(TransferError):
            self.acc.transfer(self.other, 200)

    def test_phone_top_up_valid(self):
        msg = self.acc.phone_top_up("1234567890", 10)
        self.assertIn("topped up", msg)
        self.assertEqual(self.acc.balance, 90)

    def test_phone_top_up_invalid_number(self):
        with self.assertRaises(InvalidInputError):
            self.acc.phone_top_up("1234", 10)

    def test_deposit_zero(self):
        with self.assertRaises(InvalidInputError):
            self.acc.deposit(0)

    def test_withdraw_zero(self):
        with self.assertRaises(InvalidInputError):
            self.acc.withdraw(0)

if __name__ == '__main__':
    unittest.main()
