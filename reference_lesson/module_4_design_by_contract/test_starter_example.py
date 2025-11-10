"""
Tests for BankAccount starter example.

COMPREHENSIVE CONTRACT TESTING STRATEGY

This test suite demonstrates how to test Design by Contract implementations,
including precondition violations, postcondition verification, and invariant maintenance.

TESTING CONTRACT-BASED CODE:

1. PRECONDITION TESTING:
   - Test that invalid inputs are rejected with appropriate contract violations
   - Verify that precondition checks happen before any processing
   - Test boundary conditions of preconditions

2. POSTCONDITION TESTING:
   - Verify that methods fulfill their promised guarantees
   - Test that postconditions are checked after operations
   - Ensure postconditions hold even in edge cases

3. INVARIANT TESTING:
   - Test that invariants are maintained across all operations
   - Verify invariants are checked at appropriate times
   - Test that invariant violations are detected and reported

LEARNING OBJECTIVES:
- Learn to test contract-based defensive programming
- Understand how to verify preconditions, postconditions, and invariants
- Practice testing both success and contract violation scenarios
- See examples of comprehensive contract verification testing

TESTING PHILOSOPHY:
Contract testing ensures that the defensive programming mechanisms work
correctly and that the contracts are meaningful and enforceable.
"""

import pytest
from starter_example import BankAccount, ContractViolationError


class TestBankAccount:
    """
    Comprehensive test cases for BankAccount Design by Contract implementation.
    
    TEST ORGANIZATION:
    Tests are organized by contract type (preconditions, postconditions, invariants)
    and include both successful operations and contract violation scenarios.
    
    CONTRACT TESTING STRATEGY:
    Each test verifies specific aspects of the contract system while ensuring
    that normal functionality works correctly within the contract framework.
    """
    
    def test_initialization_success(self):
        """
        Test successful account creation (Contract Establishment).
        
        TESTING CONCEPT: Contract Establishment Testing
        This test verifies that valid inputs satisfy all preconditions
        and that the object is created with proper invariants established.
        
        EXPECTED BEHAVIOR:
        - All preconditions should be satisfied
        - Object should be created successfully  
        - Class invariants should be established
        - Initial state should be correct
        
        CONTRACT VERIFICATION:
        This implicitly tests that precondition checks pass for valid input
        and that invariants are properly established during initialization.
        """
        account = BankAccount("ACC123", 100.0)
        assert account.balance == 100.0
    
    def test_initialization_precondition_empty_account_number(self):
        """
        Test precondition violation for empty account number (Precondition Testing).
        
        TESTING CONCEPT: Precondition Violation Testing
        This test verifies that precondition checks properly reject invalid
        inputs and raise appropriate contract violation errors.
        
        EXPECTED BEHAVIOR:
        - Precondition check should detect empty account number
        - ContractViolationError should be raised with descriptive message
        - Object should not be created (exception prevents completion)
        
        CONTRACT TESTING IMPORTANCE:
        This ensures that our contract system actually enforces the
        documented preconditions and catches violations early.
        """
        with pytest.raises(ContractViolationError) as exc_info:
            BankAccount("", 100.0)
        
        assert "Precondition" in str(exc_info.value)
        assert "account_number" in str(exc_info.value)
    
    def test_initialization_precondition_negative_balance(self):
        """
        Test precondition violation for negative initial balance (Precondition Testing).
        
        TESTING CONCEPT: Business Rule Precondition Testing
        Tests that business rules (no negative balances) are enforced
        as preconditions during object creation.
        
        EXPECTED BEHAVIOR:
        - Precondition should detect negative balance
        - Contract violation should be raised
        - Clear error message should indicate the violated precondition
        """
        with pytest.raises(ContractViolationError) as exc_info:
            BankAccount("ACC123", -50.0)
        
        assert "Precondition" in str(exc_info.value)
        assert "initial_balance" in str(exc_info.value)
    
    def test_deposit_success_and_postcondition(self):
        """
        Test successful deposit with postcondition verification (Postcondition Testing).
        
        TESTING CONCEPT: Postcondition Fulfillment Testing
        This test verifies that the deposit method fulfills its postcondition
        guarantee that the balance increases by exactly the deposit amount.
        
        EXPECTED BEHAVIOR:
        - Preconditions should be satisfied
        - Operation should complete successfully
        - Postcondition should be verified (balance increased correctly)
        - Invariants should be maintained
        - Correct new balance should be returned
        
        CONTRACT VERIFICATION:
        This test ensures that postconditions are actually checked and
        that the method fulfills its contractual guarantees.
        """
        account = BankAccount("ACC123", 100.0)
        new_balance = account.deposit(50.0)
        
        assert new_balance == 150.0
        assert account.balance == 150.0
    
    def test_deposit_precondition_negative_amount(self):
        """
        Test deposit precondition violation for negative amount (Precondition Testing).
        
        TESTING CONCEPT: Method Precondition Testing  
        Tests that method-level preconditions properly validate inputs
        and prevent invalid operations from proceeding.
        
        EXPECTED BEHAVIOR:
        - Precondition check should detect negative amount
        - ContractViolationError should be raised
        - Account balance should remain unchanged
        - No side effects should occur
        """
        account = BankAccount("ACC123", 100.0)
        
        with pytest.raises(ContractViolationError) as exc_info:
            account.deposit(-25.0)
        
        assert "Precondition" in str(exc_info.value)
        assert account.balance == 100.0  # Balance unchanged
    
    def test_withdraw_success_and_postcondition(self):
        """
        Test successful withdrawal with postcondition verification (Postcondition Testing).
        
        TESTING CONCEPT: Complex Postcondition Testing
        Tests that withdrawal postconditions are properly verified,
        including balance decrease and invariant maintenance.
        
        EXPECTED BEHAVIOR:
        - Preconditions should pass (positive amount, sufficient funds)
        - Balance should decrease by withdrawal amount
        - Postcondition should verify correct balance change
        - All invariants should remain satisfied
        """
        account = BankAccount("ACC123", 100.0)
        new_balance = account.withdraw(30.0)
        
        assert new_balance == 70.0
        assert account.balance == 70.0
    
    def test_withdraw_precondition_insufficient_funds(self):
        """
        Test withdrawal precondition violation for insufficient funds (Business Rule Testing).
        
        TESTING CONCEPT: Business Rule Precondition Testing
        This test verifies that business rules (sufficient funds) are
        enforced through preconditions, preventing invalid state changes.
        
        EXPECTED BEHAVIOR:
        - Precondition should detect insufficient funds
        - Contract violation should prevent withdrawal
        - Account balance should not be modified
        - Clear error message should explain the violation
        
        INVARIANT PROTECTION:
        This also tests that preconditions protect invariants by preventing
        operations that would violate the "balance >= 0" invariant.
        """
        account = BankAccount("ACC123", 50.0)
        
        with pytest.raises(ContractViolationError) as exc_info:
            account.withdraw(100.0)
        
        assert "insufficient funds" in str(exc_info.value).lower()
        assert account.balance == 50.0  # Balance unchanged
    
    def test_invariant_maintenance_across_operations(self):
        """
        Test that invariants are maintained across multiple operations (Invariant Testing).
        
        TESTING CONCEPT: Invariant Persistence Testing
        This test verifies that class invariants are maintained throughout
        the object's lifetime, across multiple method calls.
        
        EXPECTED BEHAVIOR:
        - Invariants should hold after each operation
        - Multiple operations should not corrupt object state
        - Invariant checks should catch any violations
        - Object should remain in valid state throughout
        
        COMPREHENSIVE CONTRACT TESTING:
        This test exercises the complete contract system across multiple
        operations, ensuring contracts work together correctly.
        """
        account = BankAccount("ACC123", 100.0)
        
        # Multiple operations - invariants should hold throughout
        account.deposit(50.0)  # Balance: 150.0
        account.withdraw(25.0)  # Balance: 125.0  
        account.deposit(75.0)   # Balance: 200.0
        
        # Final state should be valid and invariants maintained
        assert account.balance == 200.0