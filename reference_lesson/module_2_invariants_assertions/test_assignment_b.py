"""
Assignment Part B: Tests that students' SimpleList must pass.
Students need to implement SimpleList to make these tests pass.
"""

import pytest
from assignment_b import SimpleList


class TestSimpleList:
    """Tests for SimpleList - student implementation must pass these."""
    
    def test_initialization_valid_capacity(self):
        """Test list initialization with valid capacity."""
        lst = SimpleList(3)
        assert lst.size == 0
        assert lst.is_full is False
    
    def test_initialization_invalid_capacity(self):
        """Test list initialization with invalid capacity."""
        with pytest.raises(AssertionError):
            SimpleList(0)
        
        with pytest.raises(AssertionError):
            SimpleList(-1)
    
    def test_add_success(self):
        """Test successful add operation."""
        lst = SimpleList(2)
        result = lst.add("item1")
        assert result is True
        assert lst.size == 1
    
    def test_add_when_full(self):
        """Test add when list is full."""
        lst = SimpleList(2)
        lst.add("item1")
        lst.add("item2")
        
        assert lst.is_full is True
        result = lst.add("item3")
        assert result is False
        assert lst.size == 2
    
    def test_remove_last_success(self):
        """Test successful remove_last operation."""
        lst = SimpleList(3)
        lst.add("first")
        lst.add("second")
        
        item = lst.remove_last()
        assert item == "second"
        assert lst.size == 1
    
    def test_remove_last_from_empty(self):
        """Test remove_last from empty list."""
        lst = SimpleList(2)
        item = lst.remove_last()
        assert item is None
        assert lst.size == 0
    
    def test_get_valid_index(self):
        """Test get with valid index."""
        lst = SimpleList(3)
        lst.add("zero")
        lst.add("one")
        
        item = lst.get(0)
        assert item == "zero"
        
        item = lst.get(1)
        assert item == "one"
    
    def test_get_invalid_index(self):
        """Test get with invalid index."""
        lst = SimpleList(2)
        lst.add("item")
        
        # Test negative index
        assert lst.get(-1) is None
        
        # Test index too large
        assert lst.get(5) is None