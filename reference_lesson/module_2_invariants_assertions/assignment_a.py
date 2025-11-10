"""
Assignment Part A: Simple BankAccount class to be tested by students.
Students need to write tests to achieve 100% coverage.
"""


class BankAccount:
    """
    A simple bank account with defensive programming.
    Students should write comprehensive tests for this class.
    
    Class Invariant: Balance should never be negative
    """
    
    def __init__(self, initial_balance=0):
        """
        Initialize bank account.
        
        Args:
            initial_balance: Starting balance (must be >= 0)
        """
        assert isinstance(initial_balance, (int, float)), "Balance must be a number"
        assert initial_balance >= 0, "Initial balance cannot be negative"
        
        self._balance = initial_balance
    
    def deposit(self, amount):
        """
        Deposit money using guard clauses.
        
        Returns:
            bool: True if successful, False if invalid amount
        """
        # Guard clauses
        if not isinstance(amount, (int, float)):
            return False
        
        if amount <= 0:
            return False
        
        # Main operation
        self._balance += amount
        
        # Post-condition check
        assert self._balance >= 0, "Balance should never be negative"
        
        return True
    
    def withdraw(self, amount):
        """
        Withdraw money with guard clauses.
        
        Returns:
            bool: True if successful, False if invalid or insufficient funds
        """
        # Guard clauses
        if not isinstance(amount, (int, float)):
            return False
        
        if amount <= 0:
            return False
        
        if amount > self._balance:
            return False
        
        # Main operation
        self._balance -= amount
        
        # Invariant check
        assert self._balance >= 0, "Balance became negative!"
        
        return True
    
    @property
    def balance(self):
        """Get current balance."""
        # Check invariant
        assert self._balance >= 0, "Balance invariant violated"
        return self._balance