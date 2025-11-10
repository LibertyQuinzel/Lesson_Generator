"""
Assignment Part B: Student implementation template.
Students need to implement SimpleList class to pass provided tests.
"""


class SimpleList:
    """
    A simple list with maximum capacity showing defensive programming.
    Students must implement this class with proper invariants and assertions.
    
    Class Invariant: List size should never exceed max_capacity
    """
    
    def __init__(self, max_capacity):
        """
        Initialize list with maximum capacity.
        
        Args:
            max_capacity: Maximum number of items list can hold
            
        TODO: 
        - Add assertion to check max_capacity is valid
        - Initialize internal storage
        """
        # TODO: Implement initialization with assertions
        pass
    
    def add(self, item):
        """
        Add item to list using guard clauses.
        
        Returns:
            bool: True if successful, False if list is full
            
        TODO:
        - Use guard clause to check if list is full
        - Add item to list
        - Check invariants
        """
        # TODO: Implement with guard clauses
        pass
    
    def remove_last(self):
        """
        Remove and return last item from list.
        
        Returns:
            Any: Last item if list not empty, None otherwise
            
        TODO:
        - Use guard clause to check if list is empty
        - Remove last item
        """
        # TODO: Implement with guard clauses
        pass
    
    def get(self, index):
        """
        Get item at index using guard clauses.
        
        Returns:
            Any: Item at index, or None if invalid index
            
        TODO:
        - Use guard clauses to check valid index
        - Return item at index
        """
        # TODO: Implement with guard clauses
        pass
    
    @property
    def size(self):
        """Get current list size."""
        # TODO: Return current size
        pass
    
    @property
    def is_full(self):
        """Check if list is at capacity."""
        # TODO: Return True if at max capacity
        pass