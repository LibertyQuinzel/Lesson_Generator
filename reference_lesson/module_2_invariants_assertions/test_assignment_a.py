"""
Assignment Part A: Test template for students.
Students need to complete these tests for 100% coverage.
"""

import pytest
from assignment_a import BankAccount


class TestBankAccount:
    """Test template - students should complete these tests."""
    
    def test_valid_initialization_default(self):
        """Test creating account with default balance."""
        # TODO: Test BankAccount() has balance 0
        pass
    
    def test_valid_initialization_custom(self):
        """Test creating account with custom balance."""
        # TODO: Test BankAccount(100) has balance 100
        pass
    
    def test_invalid_negative_balance(self):
        """Test initialization with negative balance."""
        # TODO: Test BankAccount(-50) should raise AssertionError
        pass
    
    def test_invalid_balance_type(self):
        """Test initialization with invalid balance type."""
        # TODO: Test BankAccount("100") should raise AssertionError
        pass
    
    def test_deposit_valid_amount(self):
        """Test depositing valid amount."""
        # TODO: Test deposit(50) returns True and increases balance
        pass
    
    def test_deposit_zero_amount(self):
        """Test depositing zero amount."""
        # TODO: Test deposit(0) returns False
        pass
    
    def test_deposit_negative_amount(self):
        """Test depositing negative amount."""
        # TODO: Test deposit(-25) returns False
        pass
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing valid amount."""
        # TODO: Test withdraw from account with sufficient funds
        pass
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than balance."""
        # TODO: Test withdraw amount > balance returns False
        pass
    
    def test_withdraw_invalid_type(self):
        """Test withdrawing invalid type."""
        # TODO: Test withdraw("50") returns False
        pass
    
    # TODO: Add more tests to achieve 100% coverage
    # Consider edge cases like:
    # - Float amounts
    # - Very large amounts
    # - Exact balance withdrawal