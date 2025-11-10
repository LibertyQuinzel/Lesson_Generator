"""
Starter Example: Bank Account with Design by Contract

A comprehensive demonstration of Design by Contract principles using
preconditions, postconditions, and invariants in a banking context.

LEARNING OBJECTIVES:
- Understand preconditions as caller responsibilities
- Learn postconditions as method guarantees
- Master class invariants for object consistency
- See practical contract implementation patterns

KEY CONTRACT CONCEPTS:

1. PRECONDITIONS:
   Purpose: Define what callers must guarantee before calling methods
   Responsibility: Caller must ensure these conditions are met
   Benefit: Clear API contracts and input validation

2. POSTCONDITIONS:
   Purpose: Define what methods guarantee upon successful completion
   Responsibility: Method must ensure these conditions before returning
   Benefit: Verified outputs and reliable behavior

3. CLASS INVARIANTS:
   Purpose: Properties that must always be true for object instances
   Responsibility: All methods must maintain invariants
   Benefit: Consistent object state and integrity

DESIGN BY CONTRACT PHILOSOPHY:
Contracts make the implicit explicit - they document and enforce
the responsibilities of both callers and implementers.
"""


class ContractViolationError(Exception):
    """Exception raised when a contract is violated."""
    pass


class BankAccount:
    """
    A bank account demonstrating Design by Contract principles.
    
    CLASS INVARIANTS:
    1. Balance must always be non-negative (balance >= 0)
    2. Account number must be a non-empty string
    3. Balance must be a numeric type (int or float)
    
    DESIGN PHILOSOPHY:
    Each method has explicit preconditions (what callers must guarantee)
    and postconditions (what the method guarantees). The class maintains
    invariants that must always hold true.
    """
    
    def __init__(self, account_number, initial_balance=0):
        """
        Initialize bank account with contract verification.
        
        PRECONDITIONS (Caller Responsibilities):
        - account_number must be a non-empty string
        - initial_balance must be non-negative numeric value
        
        POSTCONDITIONS (Method Guarantees):
        - Object will be created with specified account number and balance
        - All class invariants will be established and maintained
        
        Args:
            account_number (str): Unique account identifier
            initial_balance (float): Starting balance (default 0)
            
        Raises:
            ContractViolationError: If preconditions are not met
        """
        # Precondition checks - caller responsibilities
        if not isinstance(account_number, str) or not account_number:
            raise ContractViolationError("Precondition: account_number must be non-empty string")
        
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ContractViolationError("Precondition: initial_balance must be non-negative number")
        
        # Initialize object state
        self._account_number = account_number
        self._balance = float(initial_balance)
        
        # Establish class invariants
        self._check_invariants()
    
    def _check_invariants(self):
        """
        Verify that all class invariants hold true.
        
        CLASS INVARIANT VERIFICATION:
        This method encapsulates all invariant checks that must always
        be true for any valid BankAccount instance.
        
        INVARIANTS CHECKED:
        1. Balance is non-negative
        2. Account number is non-empty string  
        3. Balance is numeric type
        
        Raises:
            ContractViolationError: If any invariant is violated
        """
        if self._balance < 0:
            raise ContractViolationError("Invariant violated: balance cannot be negative")
        
        if not isinstance(self._account_number, str) or not self._account_number:
            raise ContractViolationError("Invariant violated: account_number must be non-empty string")
        
        if not isinstance(self._balance, (int, float)):
            raise ContractViolationError("Invariant violated: balance must be numeric")
    
    def deposit(self, amount):
        """
        Deposit money with full contract verification.
        
        PRECONDITIONS (Caller Responsibilities):
        - amount must be a positive number
        - amount must be of numeric type (int or float)
        
        POSTCONDITIONS (Method Guarantees):
        - balance will increase by exactly the deposit amount
        - all class invariants will be maintained
        - method will return the new balance
        
        CONTRACT PATTERN DEMONSTRATION:
        This method shows the complete contract pattern: check preconditions,
        perform operation, verify postconditions, maintain invariants.
        
        Args:
            amount (float): Amount to deposit (must be positive)
            
        Returns:
            float: New account balance after deposit
            
        Raises:
            ContractViolationError: If preconditions fail or postconditions not met
        """
        # Precondition verification
        if not isinstance(amount, (int, float)):
            raise ContractViolationError("Precondition: amount must be numeric")
        
        if amount <= 0:
            raise ContractViolationError("Precondition: amount must be positive")
        
        # Store old state for postcondition verification
        old_balance = self._balance
        
        # Perform the operation
        self._balance += amount
        
        # Postcondition verification - method guarantees
        if abs(self._balance - (old_balance + amount)) > 0.0001:
            raise ContractViolationError("Postcondition: balance not increased by deposit amount")
        
        # Verify class invariants maintained
        self._check_invariants()
        
        return self._balance
    
    def withdraw(self, amount):
        """
        Withdraw money with comprehensive contract checking.
        
        PRECONDITIONS (Caller Responsibilities):
        - amount must be positive numeric value
        - amount must not exceed current balance (sufficient funds)
        
        POSTCONDITIONS (Method Guarantees):  
        - balance will decrease by exactly the withdrawal amount
        - all class invariants will be maintained
        - method will return the new balance
        
        Args:
            amount (float): Amount to withdraw
            
        Returns:
            float: New balance after withdrawal
            
        Raises:
            ContractViolationError: If preconditions or postconditions fail
        """
        # Precondition checks
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ContractViolationError("Precondition: amount must be positive number")
        
        if amount > self._balance:
            raise ContractViolationError("Precondition: insufficient funds for withdrawal")
        
        # Store state for postcondition verification  
        old_balance = self._balance
        
        # Perform operation
        self._balance -= amount
        
        # Postcondition verification
        if abs(self._balance - (old_balance - amount)) > 0.0001:
            raise ContractViolationError("Postcondition: balance not decreased by withdrawal amount")
        
        # Invariants must still hold
        self._check_invariants()
        
        return self._balance
    
    @property
    def balance(self):
        """
        Get current balance with invariant verification.
        
        POSTCONDITION: Returned balance satisfies all invariants
        """
        self._check_invariants()
        return self._balance