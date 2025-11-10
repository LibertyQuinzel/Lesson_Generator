"""
Starter Example: Dictionary Helper

A comprehensive example demonstrating EAFP vs LBYL programming philosophies.
Perfect for beginners to understand both approaches with practical examples.

LEARNING OBJECTIVES:
- Understand the difference between EAFP and LBYL approaches
- Learn when to use each approach effectively
- See practical implementations of both patterns
- Understand performance and readability implications

EAFP (Easier to Ask for Forgiveness than Permission):
    Philosophy: Try the operation first, handle exceptions if they occur.
    Benefits: Generally faster when the "happy path" is common, more Pythonic
    Use when: Exceptions are rare, operations might have race conditions

LBYL (Look Before You Leap):
    Philosophy: Check conditions before performing operations.
    Benefits: Avoids exceptions entirely, can be clearer in some cases
    Use when: Checks are simple and fast, exceptions would be expensive
"""


class DictionaryHelper:
    """
    A simple class demonstrating EAFP and LBYL patterns in practical scenarios.
    
    This class provides side-by-side comparisons of both approaches for common
    operations like dictionary access, type conversion, and arithmetic operations.
    
    DESIGN PATTERN COMPARISON:
    EAFP = "Easier to Ask for Forgiveness than Permission"
        - Pythonic approach favored by the language design
        - Uses try/except blocks to handle errors
        - Generally faster when exceptions are rare
    
    LBYL = "Look Before You Leap"  
        - More traditional approach from other languages
        - Uses conditional checks before operations
        - Can be clearer when logic is complex
    
    Attributes:
        data (dict): Sample dictionary containing user profile information
                    Used to demonstrate dictionary access patterns
    """
    
    def __init__(self):
        """
        Initialize the helper with sample profile data.
        
        The sample data represents a typical user profile with mixed data types,
        perfect for demonstrating different access patterns and error scenarios.
        """
        self.data = {"name": "Alice", "age": 25, "city": "Boston"}
    
    def get_value_eafp(self, key):
        """
        Get dictionary value using EAFP (Exception-based) approach.
        
        CONCEPT EXPLANATION:
        The EAFP approach attempts the dictionary access directly within a try block.
        If the key doesn't exist, Python raises a KeyError exception, which we catch
        and handle gracefully by returning None.
        
        ADVANTAGES:
        - More Pythonic and idiomatic Python code
        - Faster when the key usually exists (common case)
        - Atomic operation - no race conditions possible
        - Handles the "happy path" efficiently
        
        PERFORMANCE NOTE:
        Exception handling has overhead, but Python's exception system is optimized.
        When exceptions are rare (< 10% of cases), this approach is typically faster.
        
        Args:
            key (str): The dictionary key to look up
            
        Returns:
            Any: Value associated with key, or None if key doesn't exist
            
        Example:
            >>> helper = DictionaryHelper()
            >>> helper.get_value_eafp("name")  # Returns "Alice"
            >>> helper.get_value_eafp("missing")  # Returns None
        """
        try:
            return self.data[key]
        except KeyError:
            return None
    
    def get_value_lbyl(self, key):
        """
        Get dictionary value using LBYL (Check-first) approach.
        
        CONCEPT EXPLANATION:
        The LBYL approach first checks if the key exists using the 'in' operator,
        then accesses the value only if the check passes. This avoids exceptions
        entirely by validating conditions before attempting operations.
        
        ADVANTAGES:
        - No exceptions raised, which some consider "cleaner"
        - More explicit about what conditions are being checked
        - Familiar pattern from other programming languages
        - Predictable execution path
        
        DISADVANTAGES:
        - Two dictionary operations instead of one (check + access)
        - Potential race condition in multithreaded code
        - Less idiomatic in Python
        
        PERFORMANCE NOTE:
        When keys frequently don't exist, this can be faster than EAFP
        because it avoids exception overhead.
        
        Args:
            key (str): The dictionary key to look up
            
        Returns:
            Any: Value associated with key, or None if key doesn't exist
            
        Example:
            >>> helper = DictionaryHelper()
            >>> helper.get_value_lbyl("age")  # Returns 25
            >>> helper.get_value_lbyl("missing")  # Returns None
        """
        if key in self.data:
            return self.data[key]
        else:
            return None
    
    def convert_to_int_eafp(self, value):
        """
        Convert value to integer using EAFP approach.
        
        CONCEPT EXPLANATION:
        This method demonstrates EAFP for type conversion operations.
        We attempt the int() conversion directly and catch multiple exception
        types that could occur during conversion.
        
        EXCEPTION HANDLING STRATEGY:
        - ValueError: Raised when string cannot be converted (e.g., "abc")
        - TypeError: Raised when value type cannot be converted (e.g., list)
        
        REAL-WORLD APPLICATION:
        This pattern is common when processing user input, file data, or
        API responses where data types are uncertain.
        
        DESIGN DECISION:
        Returns 0 as a safe default value rather than None, making it
        suitable for mathematical operations without additional checks.
        
        Args:
            value: Value to convert to integer (any type)
            
        Returns:
            int: Converted integer value, or 0 if conversion fails
            
        Example:
            >>> helper = DictionaryHelper()
            >>> helper.convert_to_int_eafp("123")  # Returns 123
            >>> helper.convert_to_int_eafp("abc")  # Returns 0
            >>> helper.convert_to_int_eafp([1,2,3])  # Returns 0
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    
    def convert_to_int_lbyl(self, value):
        """
        Convert value to integer using LBYL approach.
        
        CONCEPT EXPLANATION:
        This method demonstrates LBYL for type conversion by checking
        the value's type and format before attempting conversion.
        Each condition is verified before proceeding to the next step.
        
        VALIDATION STRATEGY:
        1. Check if already an integer - return directly
        2. Check if string AND contains only digits - safe to convert
        3. All other cases - return default value
        
        LIMITATIONS OF THIS APPROACH:
        - Only handles positive integers (isdigit() doesn't handle "-123")
        - More verbose than EAFP version
        - Doesn't handle edge cases like whitespace or float strings
        
        TRADE-OFFS:
        + Explicit about what cases are handled
        + No exceptions raised
        - More code to handle all edge cases properly
        - Less flexible than exception-based approach
        
        Args:
            value: Value to convert to integer (any type)
            
        Returns:
            int: Converted integer value, or 0 if conversion not possible
            
        Example:
            >>> helper = DictionaryHelper()
            >>> helper.convert_to_int_lbyl(42)     # Returns 42
            >>> helper.convert_to_int_lbyl("123")  # Returns 123
            >>> helper.convert_to_int_lbyl("-123") # Returns 0 (limitation!)
        """
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return 0
    
    def safe_divide_eafp(self, a, b):
        """
        Divide two numbers using EAFP approach.
        
        CONCEPT EXPLANATION:
        Mathematical operations are perfect examples for EAFP because
        the operation itself will raise specific exceptions for error cases.
        Division by zero is a well-defined error condition in Python.
        
        EXCEPTION HANDLING:
        ZeroDivisionError is raised automatically by Python when dividing by zero.
        We catch this specific exception rather than checking beforehand.
        
        ADVANTAGES:
        - Single operation attempt
        - Handles the error exactly where it occurs
        - Natural Python behavior
        
        Args:
            a (number): Numerator
            b (number): Denominator
            
        Returns:
            float: Result of division, or None if division by zero
            
        Example:
            >>> helper = DictionaryHelper()
            >>> helper.safe_divide_eafp(10, 2)  # Returns 5.0
            >>> helper.safe_divide_eafp(10, 0)  # Returns None
        """
        try:
            return a / b
        except ZeroDivisionError:
            return None
    
    def safe_divide_lbyl(self, a, b):
        """
        Divide two numbers using LBYL approach.
        
        CONCEPT EXPLANATION:
        This version checks the denominator before attempting division.
        The condition b != 0 prevents the ZeroDivisionError from occurring.
        
        LOGICAL FLOW:
        1. Check if denominator is non-zero
        2. If safe, perform division
        3. Otherwise, return error value
        
        COMPARISON WITH EAFP:
        - More explicit about the condition being checked
        - Avoids exception overhead
        - Traditional approach familiar from other languages
        
        PERFORMANCE CONSIDERATION:
        For simple numeric checks like this, the performance difference
        between EAFP and LBYL is negligible in Python.
        
        Args:
            a (number): Numerator  
            b (number): Denominator
            
        Returns:
            float: Result of division, or None if denominator is zero
            
        Example:
            >>> helper = DictionaryHelper()
            >>> helper.safe_divide_lbyl(15, 3)  # Returns 5.0
            >>> helper.safe_divide_lbyl(15, 0)  # Returns None
        """
        if b != 0:
            return a / b
        return None