"""
Assignment Part A: Test template for students.
Students need to complete these tests to achieve 100% coverage.
"""

import pytest
from assignment_a import Rectangle


class TestRectangle:
    """Test template - students should complete these tests."""
    
    def test_initialization_success(self):
        """Test successful rectangle creation."""
        # TODO: Test Rectangle(5, 3) creates successfully
        pass
    
    def test_initialization_precondition_negative_width(self):
        """Test precondition violation for negative width."""
        # TODO: Test Rectangle(-5, 3) raises AssertionError
        pass
    
    def test_initialization_precondition_zero_height(self):
        """Test precondition violation for zero height."""  
        # TODO: Test Rectangle(5, 0) raises AssertionError
        pass
    
    def test_initialization_precondition_non_numeric(self):
        """Test precondition violation for non-numeric input."""
        # TODO: Test Rectangle("5", 3) raises AssertionError
        pass
    
    def test_area_calculation_and_postcondition(self):
        """Test area calculation with postcondition verification."""
        # TODO: Test area calculation for Rectangle(4, 6) 
        pass
    
    def test_perimeter_calculation_and_postcondition(self):
        """Test perimeter calculation with postcondition."""
        # TODO: Test perimeter calculation for Rectangle(3, 4)
        pass
    
    def test_scale_success_with_postcondition(self):
        """Test successful scaling with postcondition verification."""
        # TODO: Test scale(2.0) and verify area scaling
        pass
    
    def test_scale_precondition_negative_factor(self):
        """Test scale precondition violation for negative factor."""
        # TODO: Test scale(-1) raises AssertionError
        pass
    
    def test_scale_precondition_zero_factor(self):
        """Test scale precondition violation for zero factor."""
        # TODO: Test scale(0) raises AssertionError
        pass
    
    def test_width_property_with_invariant(self):
        """Test width property access with invariant check."""
        # TODO: Test width property returns correct value
        pass
    
    def test_height_property_with_invariant(self):
        """Test height property access with invariant check."""
        # TODO: Test height property returns correct value
        pass
    
    # TODO: Add more tests to achieve 100% coverage
    # Consider edge cases like very small positive numbers, large numbers