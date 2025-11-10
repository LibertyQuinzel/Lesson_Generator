"""
Starter Example: Simple Counter with Defensive Programming

A comprehensive demonstration of defensive programming techniques including
assertions, invariants, and guard clauses in a beginner-friendly context.

LEARNING OBJECTIVES:
- Understand the role of assertions in catching programming errors
- Learn to identify and maintain class invariants
- Master the use of guard clauses for input validation
- See practical examples of defensive programming patterns

KEY DEFENSIVE PROGRAMMING CONCEPTS:

1. ASSERTIONS:
   Purpose: Catch programming errors during development
   When to use: Verify assumptions and preconditions
   Important: Can be disabled in production with -O flag

2. INVARIANTS:
   Purpose: Conditions that must always be true for an object
   Types: Class invariants (properties of object state)
   Best practice: Check at strategic points in methods

3. GUARD CLAUSES:
   Purpose: Early validation and error handling
   Benefits: Reduce nesting, clarify main logic, handle edge cases first
   Pattern: Check conditions early, return/exit if invalid

DESIGN PHILOSOPHY:
This counter demonstrates how defensive programming makes code more reliable
by catching errors early and maintaining consistent object state.
"""


class SimpleCounter:
    """
    A counter demonstrating comprehensive defensive programming concepts.
    
    CLASS INVARIANT DEFINITION:
    The fundamental rule that must always hold true for any SimpleCounter instance:
    - Counter value (_count) must always be >= 0
    - This invariant is established in __init__ and maintained by all methods
    
    DEFENSIVE PROGRAMMING FEATURES:
    - Assertions for precondition checking
    - Guard clauses for input validation  
    - Invariant verification at key points
    - Clear error messages for debugging
    
    DESIGN PRINCIPLES:
    - Fail fast: Detect errors as early as possible
    - Explicit validation: Make assumptions clear through assertions
    - Consistent state: Ensure invariants are never violated
    """
    
    def __init__(self, start_value=0):
        """
        Initialize counter with starting value using defensive programming.
        
        PRECONDITION CHECKING WITH ASSERTIONS:
        Assertions verify our assumptions about the input parameters.
        They serve as executable documentation of what the method expects.
        
        WHY USE ASSERTIONS HERE:
        1. Document the expected input type and range
        2. Catch programmer errors during development
        3. Provide clear error messages for debugging
        4. Establish the class invariant from initialization
        
        ASSERTION STRATEGY:
        - Check type first (isinstance)
        - Then check value constraints (>= 0)
        - Use descriptive error messages
        
        Args:
            start_value (int): Initial counter value (must be >= 0)
            
        Raises:
            AssertionError: If start_value is not an integer or is negative
            
        Example:
            >>> counter = SimpleCounter(5)   # Valid initialization
            >>> counter = SimpleCounter(-1)  # Raises AssertionError
        """
        # Precondition assertions - verify input assumptions
        assert isinstance(start_value, int), "Start value must be an integer"
        assert start_value >= 0, "Start value must be non-negative"
        
        # Initialize with valid value
        self._count = start_value
        
        # Class invariant is now established: self._count >= 0
    
    def increment(self, amount=1):
        """
        Increase counter by amount using guard clauses for input validation.
        
        GUARD CLAUSE PATTERN DEMONSTRATION:
        This method showcases the guard clause pattern where we check
        for invalid conditions early and exit immediately if found.
        This reduces nesting and makes the main logic clearer.
        
        GUARD CLAUSE BENEFITS:
        1. Early validation - catch problems before processing
        2. Reduced nesting - avoid deeply nested if-else structures  
        3. Clear error handling - each guard handles one specific case
        4. Improved readability - main logic is not obscured by validation
        
        VALIDATION STRATEGY:
        - Type checking: Ensure amount is an integer
        - Range checking: Ensure amount is non-negative
        - Business logic: Only allow operations that maintain invariants
        
        POST-CONDITION VERIFICATION:
        After the operation, we assert that our class invariant still holds.
        This catches any logic errors that might violate our contract.
        
        Args:
            amount (int): How much to increase counter (default 1, must be >= 0)
            
        Returns:
            bool: True if operation successful, False if invalid input
            
        Example:
            >>> counter = SimpleCounter(5)
            >>> counter.increment(3)    # Returns True, counter becomes 8
            >>> counter.increment(-2)   # Returns False, counter unchanged
            >>> counter.increment("5")  # Returns False, invalid type
        """
        # Guard clause #1 - Type validation
        if not isinstance(amount, int):
            return False
        
        # Guard clause #2 - Range validation  
        if amount < 0:
            return False
        
        # Main operation - increment counter
        self._count += amount
        
        # Post-condition assertion - verify invariant maintained
        assert self._count >= 0, "Counter should never be negative"
        
        return True
    
    def decrement(self, amount=1):
        """
        Decrease counter by amount with comprehensive guard clauses.
        
        ADVANCED GUARD CLAUSE EXAMPLE:
        This method demonstrates a more complex guard clause pattern where
        we must check not only input validity but also business rules
        (maintaining the class invariant).
        
        LAYERED VALIDATION APPROACH:
        1. Input type validation (technical constraint)
        2. Input range validation (business rule)  
        3. Operation validity check (invariant protection)
        
        INVARIANT PROTECTION:
        The critical guard clause checks if the operation would violate
        our class invariant (counter >= 0) before performing it.
        This prevents the invariant from ever being broken.
        
        ERROR HANDLING PHILOSOPHY:
        Rather than raising exceptions for invalid operations,
        this method returns False, allowing the caller to handle
        the situation gracefully.
        
        Args:
            amount (int): How much to decrease counter (default 1, must be >= 0)
            
        Returns:
            bool: True if operation successful, False if invalid input or would violate invariant
            
        Example:
            >>> counter = SimpleCounter(5)
            >>> counter.decrement(2)    # Returns True, counter becomes 3
            >>> counter.decrement(10)   # Returns False, would make counter negative
            >>> counter.decrement(-1)   # Returns False, invalid amount
        """
        # Guard clause #1 - Type validation
        if not isinstance(amount, int):
            return False
        
        # Guard clause #2 - Range validation
        if amount < 0:
            return False
        
        # Guard clause #3 - Invariant protection
        # This is crucial: check if operation would violate our class invariant
        if self._count - amount < 0:
            return False
        
        # Main operation - decrement counter
        self._count -= amount
        
        # Post-condition assertion - verify invariant still holds
        # This should never fail if our guard clause logic is correct
        assert self._count >= 0, "Counter became negative!"
        
        return True
    
    def reset(self):
        """
        Reset counter to zero with invariant verification.
        
        SIMPLE OPERATION WITH DEFENSIVE CHECKS:
        Even for simple operations like reset, defensive programming
        includes verification that invariants are maintained.
        
        ASSERTION PLACEMENT STRATEGY:
        We place the assertion after the operation to verify that
        the reset operation didn't somehow violate our invariant.
        While logically this should never fail, it serves as:
        1. Documentation of our invariant
        2. Safety net against future code changes
        3. Debugging aid if something goes wrong
        
        Example:
            >>> counter = SimpleCounter(100)
            >>> counter.reset()
            >>> counter.value  # Returns 0
        """
        self._count = 0
        
        # Post-condition assertion - verify reset maintained invariant
        assert self._count >= 0, "Counter should be non-negative after reset"
    
    @property
    def value(self):
        """
        Get current counter value with invariant checking.
        
        DEFENSIVE PROPERTY ACCESS:
        Even simple getter methods can include defensive programming.
        By checking the invariant on access, we can detect if the
        object state has been corrupted by any method.
        
        INVARIANT AS DEBUGGING TOOL:
        If this assertion ever fails, it indicates that:
        1. Some method violated the invariant
        2. External code modified private attributes
        3. There's a bug in our defensive programming logic
        
        WHEN TO CHECK INVARIANTS:
        - At object creation (constructor)
        - After state-changing operations (increment/decrement)  
        - When accessing critical state (this property)
        - Before/after complex operations
        
        Returns:
            int: Current counter value (guaranteed to be >= 0)
            
        Raises:
            AssertionError: If class invariant has been violated
            
        Example:
            >>> counter = SimpleCounter(5)
            >>> counter.value  # Returns 5
        """
        # Invariant check on access - detect state corruption
        assert self._count >= 0, "Counter invariant violated"
        return self._count