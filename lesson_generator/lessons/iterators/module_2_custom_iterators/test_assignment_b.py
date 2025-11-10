"""
Tests for CustomIterator implementation

This test suite verifies the iterator protocol implementation and additional iterator functionality.
"""

import pytest
from module_2_custom_iterators import Customiterator

def test_iterator_protocol():
    """Test the basic iterator protocol implementation"""
    # GIVEN
    data = [1, 2, 3]
    iterator = Customiterator(data)
    
    # WHEN/THEN
    # Verify iterator protocol methods exist
    assert hasattr(iterator, '__iter__'), "Should implement __iter__"
    assert hasattr(iterator, '__next__'), "Should implement __next__"
    
    # Verify it's actually iterable
    iter_obj = iter(iterator)
    assert iter_obj is not None
    
    # Should be able to iterate
    values = list(iterator)
    assert values == data

def test_iterator_state():
    """Test iterator state management and reset functionality"""
    # GIVEN
    iterator = Customiterator([1, 2])
    
    # WHEN/THEN
    # First iteration
    assert next(iterator) == 1
    assert iterator.has_next()
    assert next(iterator) == 2
    assert not iterator.has_next()
    
    # Should raise StopIteration at end
    with pytest.raises(StopIteration):
        next(iterator)
        
    # Reset should work
    iterator.reset()
    assert next(iterator) == 1

def test_empty_iterator():
    """Test behavior with empty data"""
    # GIVEN
    iterator = Customiterator([])
    
    # WHEN/THEN
    assert not iterator.has_next()
    with pytest.raises(StopIteration):
        next(iterator)

def test_reusability():
    """Test that iterator can be reused after completion"""
    # GIVEN
    data = [1, 2, 3]
    iterator = Customiterator(data)
    
    # WHEN/THEN
    # First complete iteration
    assert list(iterator) == data
    
    # Should be exhausted
    assert not iterator.has_next()
    
    # Reset and try again
    iterator.reset()
    assert list(iterator) == data
