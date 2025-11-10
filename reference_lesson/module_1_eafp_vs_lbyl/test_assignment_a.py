"""
Assignment Part A: Test template for students.
Students need to complete these tests to achieve 100% coverage.
"""

from assignment_a import NumberProcessor


class TestNumberProcessor:
    """Test template - students should complete these tests."""
    
    def setup_method(self):
        """Setup test fixture."""
        self.processor = NumberProcessor()
    
    def test_parse_number_eafp_valid_string(self):
        """Test EAFP with valid number string."""
        # TODO: Write test for "123"
        pass
    
    def test_parse_number_eafp_invalid_string(self):
        """Test EAFP with invalid string."""
        # TODO: Write test for "abc"
        pass
    
    def test_parse_number_lbyl_integer(self):
        """Test LBYL with integer input."""
        # TODO: Write test for integer 42
        pass
    
    def test_parse_number_lbyl_invalid_type(self):
        """Test LBYL with invalid type."""
        # TODO: Write test for list input [1, 2, 3]
        pass
    
    def test_get_first_eafp_valid_list(self):
        """Test EAFP with valid list."""
        # TODO: Write test for ["a", "b", "c"]
        pass
    
    def test_get_first_eafp_empty_list(self):
        """Test EAFP with empty list."""
        # TODO: Write test for []
        pass
    
    def test_get_first_lbyl_valid_list(self):
        """Test LBYL with valid list."""
        # TODO: Write test for [1, 2, 3]
        pass
    
    def test_get_first_lbyl_none_input(self):
        """Test LBYL with None input."""
        # TODO: Write test for None
        pass