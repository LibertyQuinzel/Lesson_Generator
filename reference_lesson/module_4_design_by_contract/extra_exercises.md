# Module 4 Extra Exercises: Design by Contract

## Quiz Questions

### 1. Multiple Choice
What is the primary responsibility of preconditions?
a) Method must ensure they are true before returning
b) Caller must ensure they are true before calling method
c) Class must ensure they are always true
d) They are automatically checked by Python

**Answer: b) Caller must ensure preconditions are true before calling the method**

### 2. True/False
Postconditions should be checked even when preconditions fail.

**Answer: False - If preconditions fail, postconditions are not relevant since the method shouldn't execute**

### 3. Fill in the Blanks
Complete this contract pattern:
```python
def transfer(self, amount, to_account):
    # ___________: amount > 0 and self.balance >= amount
    assert amount > 0 and self.balance >= amount
    
    old_balance = self.balance
    self.balance -= amount
    to_account.balance += amount
    
    # ___________: self.balance == old_balance - amount
    assert self.balance == old_balance - amount
```

**Answer: Precondition, Postcondition**

## Practical Exercises

### Exercise 1: Contract Design
Design contracts for a `SortedList` class with these methods:
- `add(item)` - maintains sorted order
- `remove(item)` - removes first occurrence
- `get(index)` - returns item at index

What preconditions, postconditions, and invariants would you define?

### Exercise 2: Convert to Contracts
Rewrite this function using Design by Contract:
```python
def calculate_interest(principal, rate, time):
    if principal <= 0 or rate < 0 or time < 0:
        return None
    return principal * rate * time
```

### Exercise 3: Invariant Identification
Identify class invariants for a `CircularBuffer` class that:
- Has a fixed capacity
- Overwrites oldest data when full
- Tracks current size and position

## Cheat Sheet

### Contract Types

**Preconditions (Caller's Responsibility):**
```python
def withdraw(self, amount):
    assert amount > 0, "Amount must be positive"
    assert amount <= self.balance, "Insufficient funds"
    # ... method implementation
```

**Postconditions (Method's Guarantee):**
```python
def deposit(self, amount):
    old_balance = self.balance
    self.balance += amount
    
    assert self.balance == old_balance + amount, "Balance not updated correctly"
```

**Class Invariants (Always True):**
```python
def _check_invariants(self):
    assert self.balance >= 0, "Balance cannot be negative"
    assert isinstance(self.balance, (int, float)), "Balance must be numeric"
```

### Contract Implementation Patterns

**Simple Assertion:**
```python
assert condition, "Error message"
```

**Custom Exception:**
```python
if not condition:
    raise ContractViolationError("Precondition failed: condition")
```

**Decorator Pattern:**
```python
def requires(condition):
    def decorator(func):
        def wrapper(*args, **kwargs):
            assert condition(*args, **kwargs), "Precondition failed"
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### When to Use Contracts
- Complex business logic
- Critical system components
- API boundary enforcement
- Mathematical algorithms
- Data structure implementations