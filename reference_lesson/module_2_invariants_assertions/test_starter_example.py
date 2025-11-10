"""
Tests for SimpleCounter starter example.

COMPREHENSIVE TESTING STRATEGY FOR DEFENSIVE PROGRAMMING

This test suite demonstrates how to thoroughly test defensive programming
features including assertions, invariants, and guard clauses.

TESTING DEFENSIVE PROGRAMMING CONCEPTS:

1. ASSERTION TESTING:
   - Test that assertions properly catch invalid inputs
   - Verify assertion messages are helpful for debugging
   - Use pytest.raises() to test expected assertion failures

2. INVARIANT TESTING:
   - Test that invariants are maintained across all operations
   - Verify invariants hold in both success and failure cases
   - Test boundary conditions that might violate invariants

3. GUARD CLAUSE TESTING:
   - Test both acceptance and rejection paths
   - Verify appropriate return values for invalid inputs
   - Test that invalid inputs don't change object state

TESTING PHILOSOPHY:
- Test both positive cases (should work) and negative cases (should fail safely)
- Verify that defensive mechanisms work as designed
- Ensure error messages are clear and helpful
- Test boundary conditions and edge cases

LEARNING OBJECTIVES:
- Learn to test defensive programming features systematically
- Understand how to verify assertions work correctly
- Practice testing both success and failure scenarios
- See examples of comprehensive test coverage for defensive code
"""

import pytest
from starter_example import SimpleCounter


class TestSimpleCounter:
    """
    Comprehensive test cases for SimpleCounter defensive programming features.
    
    TEST ORGANIZATION:
    Tests are organized by feature (initialization, increment, decrement, etc.)
    and include both positive (should work) and negative (should fail) cases.
    
    DEFENSIVE TESTING STRATEGY:
    Each test verifies that defensive mechanisms work correctly while
    ensuring normal functionality remains intact.
    """
    
    def test_initialization_default(self):
        """
        Test counter initialization with default value (Positive Case).
        
        TESTING CONCEPT: Default Parameter Testing
        Verifies that the constructor works correctly with default parameters
        and establishes the class invariant properly.
        
        EXPECTED BEHAVIOR:
        - Constructor should accept default start_value of 0
        - Class invariant (value >= 0) should be established
        - Object should be in valid state for further operations
        
        DEFENSIVE PROGRAMMING VERIFICATION:
        This test implicitly verifies that the constructor's assertions
        pass for valid input and that the invariant is properly established.
        """
        counter = SimpleCounter()
        assert counter.value == 0
    
    def test_initialization_custom_value(self):
        """
        Test counter initialization with custom valid value (Positive Case).
        
        TESTING CONCEPT: Parameter Validation Testing
        Verifies that constructor accepts valid non-zero starting values
        and maintains the invariant for custom initialization.
        
        EXPECTED BEHAVIOR:
        - Constructor should accept positive integer values
        - Object should initialize with the specified value
        - All defensive checks should pass silently
        """
        counter = SimpleCounter(5)
        assert counter.value == 5
    
    def test_initialization_negative_value(self):
        """
        Test that negative start value raises AssertionError (Assertion Testing).
        
        TESTING CONCEPT: Assertion Failure Testing
        This test verifies that our assertion-based defensive programming
        correctly catches invalid input and raises appropriate errors.
        
        EXPECTED BEHAVIOR:
        - Constructor should detect negative value
        - Assertion should fail with clear error message
        - Object should not be created (exception prevents it)
        
        DEFENSIVE PROGRAMMING VERIFICATION:
        This test ensures our precondition assertion works correctly
        and catches violations of our business rule (counter >= 0).
        """
        with pytest.raises(AssertionError):
            SimpleCounter(-1)
    
    def test_initialization_non_integer(self):
        """
        Test that non-integer start value raises AssertionError (Type Checking).
        
        TESTING CONCEPT: Type Validation Testing  
        Verifies that our type-checking assertions properly catch
        incorrect parameter types during object construction.
        
        EXPECTED BEHAVIOR:
        - Constructor should detect non-integer type
        - Type assertion should fail before value assertion
        - Clear error message should indicate type requirement
        
        DESIGN DECISION VERIFICATION:
        This test confirms our decision to be strict about types,
        preventing subtle bugs from type coercion or unexpected behavior.
        """
        with pytest.raises(AssertionError):
            SimpleCounter("5")
    
    def test_increment_default(self):
        """
        Test incrementing by default amount (Guard Clause Success Path).
        
        TESTING CONCEPT: Happy Path with Default Parameters
        Tests the most common usage scenario where increment() is called
        without parameters, using the default increment of 1.
        
        EXPECTED BEHAVIOR:
        - Guard clauses should all pass (valid type, non-negative)
        - Counter should increase by 1
        - Method should return True indicating success
        - Post-condition assertion should pass
        - Class invariant should be maintained
        
        DEFENSIVE PROGRAMMING VERIFICATION:  
        This test ensures that normal operations work correctly
        despite all the defensive programming checks.
        """
        counter = SimpleCounter(0)
        result = counter.increment()
        assert result is True
        assert counter.value == 1
    
    def test_increment_custom_amount(self):
        """
        Test incrementing by custom amount (Guard Clause Success Path).
        
        TESTING CONCEPT: Parameter Validation Success
        Tests that valid custom parameters pass through all guard clauses
        and produce the expected result.
        
        EXPECTED BEHAVIOR:
        - Type check guard clause should pass (int)
        - Range check guard clause should pass (>= 0)
        - Operation should complete successfully
        - Invariant should remain satisfied
        - Return value should indicate success
        
        INVARIANT TESTING:
        This test also verifies that the class invariant is maintained
        when operations modify the object state significantly.
        """
        counter = SimpleCounter(10)
        result = counter.increment(5)
        assert result is True
        assert counter.value == 15
    
    def test_increment_invalid_type(self):
        """
        Test increment with invalid type (Guard Clause Rejection).
        
        TESTING CONCEPT: Guard Clause Input Validation
        Tests that the first guard clause (type checking) correctly
        rejects invalid input types and prevents further processing.
        
        EXPECTED BEHAVIOR:
        - Type guard clause should detect string input
        - Method should return False immediately
        - Counter value should remain unchanged (no side effects)
        - No assertion errors should occur
        - Object state should be completely unaffected
        
        DEFENSIVE PROGRAMMING VERIFICATION:
        This test confirms that guard clauses prevent invalid operations
        and maintain object integrity even with bad input.
        """  
        counter = SimpleCounter(0)
        result = counter.increment("5")
        assert result is False
        assert counter.value == 0
    
    def test_decrement_valid(self):
        """
        Test valid decrement operation (Complex Guard Clause Success).
        
        TESTING CONCEPT: Multi-Level Guard Clause Testing
        Tests that all three guard clauses in decrement() pass for valid input:
        type check, range check, and invariant protection check.
        
        EXPECTED BEHAVIOR:
        - Type guard clause should pass (int)
        - Range guard clause should pass (>= 0) 
        - Invariant guard clause should pass (won't go negative)
        - Operation should complete successfully
        - Post-condition assertion should pass
        - Return value should indicate success
        
        INVARIANT PROTECTION TESTING:
        This test specifically verifies that the invariant protection
        guard clause correctly allows operations that maintain invariants.
        """
        counter = SimpleCounter(10)
        result = counter.decrement(3)
        assert result is True
        assert counter.value == 7
    
    def test_decrement_would_go_negative(self):
        """
        Test decrement that would violate class invariant (Invariant Protection).
        
        TESTING CONCEPT: Invariant Violation Prevention
        This is a critical test that verifies our invariant protection
        guard clause prevents operations that would violate class invariants.
        
        EXPECTED BEHAVIOR:
        - Type and range guard clauses should pass
        - Invariant protection guard clause should reject operation
        - Method should return False (operation denied)
        - Counter value should remain completely unchanged
        - Object should remain in valid state
        
        DEFENSIVE PROGRAMMING HIGHLIGHT:
        This test demonstrates the power of defensive programming -
        we prevent invariant violations rather than detecting them after.
        
        BUSINESS RULE TESTING:
        Confirms that our business rule (counter cannot go negative)
        is properly enforced by the defensive programming mechanisms.
        """
        counter = SimpleCounter(5)
        result = counter.decrement(10)
        assert result is False
        assert counter.value == 5
    
    def test_reset(self):
        """
        Test reset functionality with invariant verification.
        
        TESTING CONCEPT: Simple Operation Defensive Testing
        Even simple operations like reset include defensive programming.
        This test verifies that reset works correctly and maintains invariants.
        
        EXPECTED BEHAVIOR:
        - Reset should set counter to 0
        - Post-condition assertion should pass (0 >= 0)
        - Invariant should be maintained
        - Operation should complete without errors
        
        INVARIANT TESTING:
        This test verifies that reset operation establishes a valid
        state that satisfies our class invariant.
        """
        counter = SimpleCounter(100)
        counter.reset()
        assert counter.value == 0