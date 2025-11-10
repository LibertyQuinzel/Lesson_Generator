"""
Assignment Part A: Rectangle class to be tested by students.
Students need to write tests to achieve 100% coverage.
"""


class Rectangle:
    """
    Rectangle with Design by Contract implementation.
    Students should write comprehensive tests for this class.
    """
    
    def __init__(self, width, height):
        """
        Initialize rectangle with contract checking.
        
        Precondition: width and height must be positive numbers
        """
        assert isinstance(width, (int, float)), "Width must be numeric"
        assert isinstance(height, (int, float)), "Height must be numeric"
        assert width > 0, "Width must be positive"
        assert height > 0, "Height must be positive"
        
        self._width = width
        self._height = height
    
    def area(self):
        """
        Calculate area with postcondition verification.
        
        Postcondition: area must be positive
        """
        result = self._width * self._height
        assert result > 0, "Area must be positive"
        return result
    
    def perimeter(self):
        """Calculate perimeter with postcondition check."""
        result = 2 * (self._width + self._height)
        assert result > 0, "Perimeter must be positive"
        return result
    
    def scale(self, factor):
        """
        Scale rectangle by factor with pre/post conditions.
        
        Precondition: factor must be positive
        Postcondition: area scaled by factor squared
        """
        assert isinstance(factor, (int, float)), "Factor must be numeric"
        assert factor > 0, "Scale factor must be positive"
        
        old_area = self.area()
        self._width *= factor
        self._height *= factor
        
        # Postcondition: area scaled correctly
        new_area = self.area()
        expected_area = old_area * (factor * factor)
        assert abs(new_area - expected_area) < 0.0001, "Scaling postcondition failed"
    
    @property
    def width(self):
        """Get width with invariant check."""
        assert self._width > 0, "Width invariant violated"
        return self._width
    
    @property
    def height(self):
        """Get height with invariant check."""
        assert self._height > 0, "Height invariant violated"
        return self._height