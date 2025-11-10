"""
Assignment Part B: Tests that students' code must pass.
Students need to implement SimpleCalculator to make these tests pass.
"""

from assignment_b import SimpleCalculator


class TestSimpleCalculator:
    """Tests for SimpleCalculator - student implementation must pass these."""
    
    def setup_method(self):
        """Setup test fixture."""
        self.calc = SimpleCalculator()
    
    def test_divide_eafp_valid_division(self):
        """Test EAFP division with valid inputs."""
        result = self.calc.divide_eafp(10, 2)
        assert result == 5.0
    
    def test_divide_eafp_zero_division(self):
        """Test EAFP division by zero."""
        result = self.calc.divide_eafp(10, 0)
        assert result is None
    
    def test_divide_lbyl_valid_division(self):
        """Test LBYL division with valid inputs."""
        result = self.calc.divide_lbyl(15, 3)
        assert result == 5.0
    
    def test_divide_lbyl_zero_division(self):
        """Test LBYL division by zero."""
        result = self.calc.divide_lbyl(10, 0)
        assert result is None
    
    def test_get_item_eafp_valid_index(self):
        """Test EAFP list access with valid index."""
        result = self.calc.get_item_eafp([1, 2, 3], 1)
        assert result == 2
    
    def test_get_item_eafp_invalid_index(self):
        """Test EAFP list access with invalid index."""
        result = self.calc.get_item_eafp([1, 2, 3], 10)
        assert result is None
    
    def test_get_item_lbyl_valid_index(self):
        """Test LBYL list access with valid index."""
        result = self.calc.get_item_lbyl([1, 2, 3], 0)
        assert result == 1
    
    def test_get_item_lbyl_invalid_index(self):
        """Test LBYL list access with invalid index."""
        result = self.calc.get_item_lbyl([1, 2, 3], -10)
        assert result is None