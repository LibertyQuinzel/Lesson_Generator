"""
Assignment Part B: Tests that students' Stack must pass.
Students need to implement Stack to make these tests pass.
"""

import pytest
from assignment_b import Stack, ContractViolationError


class TestStack:
    """Tests for Stack - student implementation must pass these."""
    
    def test_initialization_unlimited_capacity(self):
        """Test stack creation without capacity limit."""
        stack = Stack()
        assert stack.size() == 0
        assert stack.is_empty() is True
    
    def test_initialization_with_capacity(self):
        """Test stack creation with capacity limit."""
        stack = Stack(max_capacity=5)
        assert stack.size() == 0
        assert stack.is_empty() is True
    
    def test_initialization_precondition_invalid_capacity(self):
        """Test precondition violation for invalid capacity."""
        with pytest.raises(ContractViolationError):
            Stack(max_capacity=-1)
    
    def test_push_success_and_postcondition(self):
        """Test successful push with postcondition verification."""
        stack = Stack()
        stack.push("item1")
        
        assert stack.size() == 1
        assert stack.is_empty() is False
        assert stack.peek() == "item1"
    
    def test_push_precondition_at_capacity(self):
        """Test push precondition violation when at capacity."""
        stack = Stack(max_capacity=1)
        stack.push("item1")
        
        with pytest.raises(ContractViolationError):
            stack.push("item2")
    
    def test_pop_success_and_postcondition(self):
        """Test successful pop with postcondition verification."""
        stack = Stack()
        stack.push("item1")
        stack.push("item2")
        
        popped = stack.pop()
        assert popped == "item2"
        assert stack.size() == 1
        assert stack.peek() == "item1"
    
    def test_pop_precondition_empty_stack(self):
        """Test pop precondition violation on empty stack."""
        stack = Stack()
        
        with pytest.raises(ContractViolationError):
            stack.pop()
    
    def test_peek_success_and_postcondition(self):
        """Test successful peek with postcondition verification."""
        stack = Stack()
        stack.push("item1")
        
        peeked = stack.peek()
        assert peeked == "item1"
        assert stack.size() == 1  # Size unchanged
    
    def test_peek_precondition_empty_stack(self):
        """Test peek precondition violation on empty stack."""
        stack = Stack()
        
        with pytest.raises(ContractViolationError):
            stack.peek()
    
    def test_invariants_maintained_across_operations(self):
        """Test that invariants are maintained across multiple operations."""
        stack = Stack(max_capacity=3)
        
        # Push items
        stack.push("a")
        stack.push("b")
        stack.push("c")
        
        # Pop items
        assert stack.pop() == "c"
        assert stack.pop() == "b"
        
        # Push again
        stack.push("d")
        
        # Final state should be valid
        assert stack.size() == 2
        assert stack.peek() == "d"