"""
Assignment Part B: Student implementation template.
Students need to implement Stack with Design by Contract.
"""


class ContractViolationError(Exception):
    """Exception raised when a contract is violated."""
    pass


class Stack:
    """
    Stack with comprehensive Design by Contract implementation.
    Students must implement with proper pre/post conditions and invariants.
    
    Class Invariants:
    - Stack size should always be >= 0
    - Stack size should not exceed max_capacity (if set)
    - Top element should be accessible when stack is not empty
    
    TODO: Implement all methods with proper contracts
    """
    
    def __init__(self, max_capacity=None):
        """
        Initialize stack with optional capacity limit.
        
        Precondition: max_capacity must be positive if provided
        Postcondition: Empty stack created with proper invariants
        
        TODO: Implement with contract checking
        """
        # TODO: Implement initialization with contracts
        pass
    
    def push(self, item):
        """
        Push item onto stack.
        
        Precondition: Stack must not be at capacity
        Postcondition: Stack size increases by 1, item becomes new top
        
        TODO: Implement with pre/post conditions
        """
        # TODO: Implement push with contracts
        pass
    
    def pop(self):
        """
        Pop and return top item from stack.
        
        Precondition: Stack must not be empty
        Postcondition: Stack size decreases by 1, returns correct item
        
        TODO: Implement with pre/post conditions
        """
        # TODO: Implement pop with contracts
        pass
    
    def peek(self):
        """
        Return top item without removing it.
        
        Precondition: Stack must not be empty
        Postcondition: Stack size unchanged, returns top item
        
        TODO: Implement with contracts
        """
        # TODO: Implement peek with contracts
        pass
    
    def size(self):
        """
        Get current stack size.
        
        Postcondition: Returns non-negative integer
        
        TODO: Implement with postcondition
        """
        # TODO: Implement size with contracts
        pass
    
    def is_empty(self):
        """
        Check if stack is empty.
        
        Postcondition: Returns True iff size is 0
        
        TODO: Implement with postcondition
        """
        # TODO: Implement is_empty with contracts
        pass