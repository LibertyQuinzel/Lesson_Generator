"""
Tests for the DictionaryHelper starter example.

COMPREHENSIVE TEST DESIGN FOR DEFENSIVE PROGRAMMING PATTERNS

This test suite demonstrates how to thoroughly test both EAFP and LBYL
implementations, ensuring they behave identically despite using different
internal approaches.

TESTING PHILOSOPHY:
- Test both happy path and edge cases
- Verify equivalent behavior between EAFP and LBYL methods  
- Use descriptive test names that explain the scenario
- Include both positive and negative test cases

KEY TESTING CONCEPTS:
1. FUNCTIONAL EQUIVALENCE: Both approaches should produce identical results
2. ERROR HANDLING: Test how each approach handles invalid inputs
3. BOUNDARY CONDITIONS: Test edge cases like empty data, None values
4. PERFORMANCE IMPLICATIONS: Understand when each approach excels

LEARNING OBJECTIVES:
- Learn to write comprehensive tests for defensive programming patterns
- Understand how to verify equivalent behavior between different implementations
- Practice testing both success and failure scenarios
- See examples of clear, descriptive test naming
"""

from starter_example import DictionaryHelper


class TestDictionaryHelper:
    """
    Comprehensive test cases for DictionaryHelper demonstrating EAFP vs LBYL.
    
    TEST ORGANIZATION:
    Tests are grouped by functionality and compare equivalent EAFP/LBYL methods.
    Each test verifies that both approaches handle the same scenario identically.
    
    FIXTURE DESIGN:
    Uses pytest's setup_method to create a fresh DictionaryHelper instance
    for each test, ensuring test isolation and preventing side effects.
    """
    
    def setup_method(self):
        """
        Set up test fixture before each test method.
        
        DESIGN PATTERN: Test Fixture Setup
        Creating a new instance for each test ensures:
        - Test isolation (no shared state between tests)
        - Consistent starting conditions
        - Prevention of test interdependencies
        
        The helper instance contains sample data: {"name": "Alice", "age": 25, "city": "Boston"}
        """
        self.helper = DictionaryHelper()
    
    def test_get_value_eafp_existing_key(self):
        """
        Test EAFP approach with existing key (Happy Path).
        
        TESTING CONCEPT: Happy Path Testing
        This test verifies the most common, successful scenario where
        the key exists in the dictionary. The EAFP approach should
        execute the try block without raising an exception.
        
        EXPECTED BEHAVIOR:
        - No exception should be raised
        - Method should return the correct value directly
        - Performance should be optimal (single dictionary access)
        """
        result = self.helper.get_value_eafp("name")
        assert result == "Alice"
    
    def test_get_value_eafp_missing_key(self):
        """
        Test EAFP approach with missing key (Exception Path).
        
        TESTING CONCEPT: Exception Path Testing  
        This test verifies error handling when the key doesn't exist.
        The EAFP approach should catch the KeyError and return None.
        
        EXPECTED BEHAVIOR:
        - KeyError should be raised internally and caught
        - Method should return None gracefully
        - No uncaught exceptions should propagate
        
        LEARNING NOTE:
        This demonstrates how EAFP handles errors through exceptions
        rather than preventing them through checks.
        """
        result = self.helper.get_value_eafp("missing")
        assert result is None
    
    def test_get_value_lbyl_existing_key(self):
        """
        Test LBYL approach with existing key (Happy Path).
        
        TESTING CONCEPT: Equivalent Behavior Verification
        This test should produce identical results to the EAFP version
        but using a different internal approach (check-then-access).
        
        EXPECTED BEHAVIOR:
        - 'in' operator check should return True
        - Dictionary access should occur after successful check
        - Same result as EAFP approach for same input
        
        COMPARISON NOTE:
        While functionally equivalent to EAFP, this approach performs
        two dictionary operations instead of one.
        """
        result = self.helper.get_value_lbyl("age")
        assert result == 25
    
    def test_get_value_lbyl_missing_key(self):
        """
        Test LBYL approach with missing key (Prevention Path).
        
        TESTING CONCEPT: Error Prevention Testing
        This test verifies that LBYL prevents errors by checking conditions
        before attempting operations, rather than handling exceptions after.
        
        EXPECTED BEHAVIOR:
        - 'in' operator check should return False
        - Dictionary access should be skipped entirely  
        - Method should return None without attempting access
        - No exceptions should be raised at any point
        
        PHILOSOPHICAL DIFFERENCE:
        Unlike EAFP which handles errors after they occur, LBYL
        prevents errors from occurring in the first place.
        """
        result = self.helper.get_value_lbyl("missing")
        assert result is None
    
    def test_convert_to_int_eafp_valid_string(self):
        """
        Test EAFP type conversion with valid numeric string.
        
        TESTING CONCEPT: Type Conversion Success Path
        Tests the most common scenario where a string contains
        a valid integer that can be converted successfully.
        
        EXPECTED BEHAVIOR:
        - int() conversion should succeed without exception
        - Method should return the converted integer value
        - No exception handling code should execute
        """
        result = self.helper.convert_to_int_eafp("123")
        assert result == 123
    
    def test_convert_to_int_eafp_invalid_string(self):
        """
        Test EAFP type conversion with invalid string.
        
        TESTING CONCEPT: Exception Handling in Type Conversion
        Tests how EAFP handles ValueError when conversion fails.
        This is a perfect example of where exceptions provide
        more information than pre-checks.
        
        EXPECTED BEHAVIOR:
        - int("abc") should raise ValueError internally
        - Exception should be caught and handled gracefully
        - Method should return safe default value (0)
        """
        result = self.helper.convert_to_int_eafp("abc")
        assert result == 0
    
    def test_convert_to_int_lbyl_integer(self):
        """
        Test LBYL type conversion with integer input.
        
        TESTING CONCEPT: Type-Based Branching
        Tests how LBYL handles the case where no conversion
        is needed because the value is already the correct type.
        
        EXPECTED BEHAVIOR:
        - isinstance(value, int) check should return True
        - Method should return value directly without conversion
        - No type conversion operations should be attempted
        
        EFFICIENCY NOTE:
        This demonstrates an advantage of LBYL - it can optimize
        for cases where operations are unnecessary.
        """
        result = self.helper.convert_to_int_lbyl(42)
        assert result == 42
    
    def test_safe_divide_eafp_valid(self):
        """
        Test EAFP division with valid operands.
        
        TESTING CONCEPT: Mathematical Operation Success Path
        Tests normal division where no errors should occur.
        This represents the "happy path" for mathematical operations.
        
        EXPECTED BEHAVIOR:
        - Division should complete successfully
        - Result should be accurate floating-point value
        - No exceptions should be raised or handled
        """
        result = self.helper.safe_divide_eafp(10, 2)
        assert result == 5.0
    
    def test_safe_divide_eafp_zero_division(self):
        """
        Test EAFP division by zero error handling.
        
        TESTING CONCEPT: Mathematical Exception Handling
        Tests how EAFP handles ZeroDivisionError, which is
        automatically raised by Python for division by zero.
        
        EXPECTED BEHAVIOR:
        - Division operation should raise ZeroDivisionError
        - Exception should be caught by except block
        - Method should return None as safe fallback value
        
        DESIGN DECISION HIGHLIGHT:
        Returns None rather than 0 or raising exception, making
        it clear that the operation failed rather than succeeded with 0.
        """
        result = self.helper.safe_divide_eafp(10, 0)
        assert result is None