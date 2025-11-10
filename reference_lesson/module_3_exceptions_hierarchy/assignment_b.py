"""
Assignment Part B: Student implementation template.
Students need to implement calculator with custom exceptions.
"""


class CalculationError(Exception):
    """
    Base exception for all calculation errors.
    Students must implement this as the root of their exception hierarchy.
    """
    # TODO: Implement base exception with error code support
    pass


class DivisionByZeroError(CalculationError):
    """Exception raised when dividing by zero."""
    # TODO: Implement specific exception for division by zero
    pass


class InvalidOperationError(CalculationError):
    """Exception raised for invalid mathematical operations."""
    # TODO: Implement specific exception for invalid operations
    pass


class SimpleCalculator:
    """
    Calculator with custom exception hierarchy.
    Students must implement methods to pass the provided tests.
    
    TODO: Implement all methods with proper exception handling
    """
    
    def divide(self, a, b):
        """
        Divide two numbers with custom exception handling.
        
        Args:
            a: numerator
            b: denominator
            
        Returns:
            float: result of division
            
        Raises:
            DivisionByZeroError: If b is zero
            InvalidOperationError: If inputs are not numbers
            
        TODO: Implement with custom exceptions
        """
        # TODO: Implement division with custom exception handling
        pass
    
    def square_root(self, x):
        """
        Calculate square root with error handling.
        
        Args:
            x: number to calculate square root of
            
        Returns:
            float: square root of x
            
        Raises:
            InvalidOperationError: If x is negative or not a number
            
        TODO: Implement with custom exceptions
        """
        # TODO: Implement square root with custom exception handling
        pass
    
    def factorial(self, n):
        """
        Calculate factorial with validation.
        
        Args:
            n: non-negative integer
            
        Returns:
            int: factorial of n
            
        Raises:
            InvalidOperationError: If n is negative or not an integer
            
        TODO: Implement with custom exceptions
        """
        # TODO: Implement factorial with custom exception handling
        pass