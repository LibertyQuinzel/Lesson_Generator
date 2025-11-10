# Module 2 Extra Exercises: Invariants, Assertions, and Guard Clauses

## Quiz Questions

### 1. Multiple Choice
When should you use assertions in Python?
a) For user input validation
b) For catching programmer errors during development
c) For handling network errors
d) For production error handling

**Answer: b) Assertions are for catching programmer errors during development**

### 2. True/False
Assertions are always executed in Python programs.

**Answer: False - Assertions can be disabled with `python -O` optimization flag**

### 3. Fill in the Blanks
Complete this guard clause pattern:
```python
def process_data(data):
    __ not data:
        ______ None
    
    # Main processing logic here
    return process(data)
```

**Answer: if, return**

## Practical Exercises

### Exercise 1: Bank Account Invariants
Design a `BankAccount` class with these invariants:
- Balance is never negative for regular accounts
- All transactions must have positive amounts
- Account number is immutable after creation

### Exercise 2: Guard Clause Refactoring
Refactor this nested code using guard clauses:
```python
def validate_user(user):
    if user:
        if user.get('email'):
            if '@' in user['email']:
                if user.get('age'):
                    if user['age'] >= 18:
                        return True
    return False
```

### Exercise 3: Loop Invariants
Write a binary search function with clear loop invariants.

## Cheat Sheet

### Assertion Pattern
```python
assert condition, "Clear error message"
# Use for: debugging, preconditions, postconditions, invariants
```

### Guard Clause Pattern  
```python
def function(param):
    # Handle edge cases first
    if not param:
        return default_value
    
    if invalid_condition:
        return error_value
    
    # Main logic - "happy path"
    return main_processing(param)
```

### Class Invariant Pattern
```python
class MyClass:
    def _check_invariants(self):
        assert self.state_is_valid(), "Invariant violated"
    
    def public_method(self):
        self._check_invariants()  # Before
        # ... do work ...
        self._check_invariants()  # After
```

### When to Use Each
- **Assertions**: Debug-time checks, invariants, preconditions  
- **Guard Clauses**: Early returns, reducing nesting, error handling
- **Invariants**: Class state validation, loop conditions