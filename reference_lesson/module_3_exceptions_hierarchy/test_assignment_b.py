"""
Assignment Part B: Tests that students' SimpleCalculator must pass.
Students need to implement SimpleCalculator to make these tests pass.
"""

import pytest
from assignment_b import SimpleCalculator, CalculationError, DivisionByZeroError, InvalidOperationError


class TestSimpleCalculator:
    """Tests for SimpleCalculator - student implementation must pass these."""
    
    def setup_method(self):
        """Setup test fixture."""
        self.calc = SimpleCalculator()
    
    def test_divide_success(self):
        """Test successful division."""
        result = self.calc.divide(10, 2)
        assert result == 5.0
    
    def test_divide_by_zero(self):
        """Test division by zero raises DivisionByZeroError."""
        with pytest.raises(DivisionByZeroError):
            self.calc.divide(10, 0)
    
    def test_divide_invalid_types(self):
        """Test division with invalid types raises InvalidOperationError."""
        with pytest.raises(InvalidOperationError):
            self.calc.divide("10", 2)
    
    def test_square_root_success(self):
        """Test successful square root calculation."""
        result = self.calc.square_root(16)
        assert result == 4.0
    
    def test_square_root_negative(self):
        """Test square root of negative number raises InvalidOperationError."""
        with pytest.raises(InvalidOperationError):
            self.calc.square_root(-4)
    
    def test_factorial_success(self):
        """Test successful factorial calculation."""
        result = self.calc.factorial(5)
        assert result == 120
    
    def test_factorial_negative(self):
        """Test factorial of negative number raises InvalidOperationError."""
        with pytest.raises(InvalidOperationError):
            self.calc.factorial(-1)
    
    def test_exception_hierarchy(self):
        """Test that specific exceptions inherit from CalculationError."""
        # Test DivisionByZeroError inheritance
        with pytest.raises(CalculationError):
            self.calc.divide(5, 0)
        
        # Test InvalidOperationError inheritance
        with pytest.raises(CalculationError):
            self.calc.square_root(-1)