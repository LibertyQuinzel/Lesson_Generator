# Module 1 Extra Exercises: EAFP vs LBYL

## Quiz Questions

### 1. Multiple Choice
Which approach is generally preferred in Python?
a) LBYL - because it's safer
b) EAFP - because it follows Python philosophy  
c) Both are equally good
d) Neither, avoid error handling

**Answer: b) EAFP follows Python's philosophy of "it's easier to ask forgiveness than permission"**

### 2. True/False
EAFP is always faster than LBYL in Python.

**Answer: False - EAFP is faster when exceptions are rare, but LBYL can be faster when exceptions are common**

### 3. Fill in the Blanks
Complete this EAFP pattern:
```python
___:
    result = risky_operation()
______ SpecificException:
    result = default_value
```

**Answer: try, except**

## Practical Exercises

### Exercise 1: Dictionary Access
Write both EAFP and LBYL versions for safely getting a nested dictionary value:
```python
data = {"user": {"profile": {"name": "Alice"}}}
# Get data["user"]["profile"]["name"] safely
```

### Exercise 2: File Operations  
When would you choose EAFP vs LBYL for file operations? Give examples.

### Exercise 3: Performance Analysis
Explain why EAFP might be slower when exceptions are frequent.

## Cheat Sheet

### EAFP Pattern
```python
try:
    # Attempt operation
    result = operation()
except SomeException:
    # Handle failure
    result = fallback()
```

### LBYL Pattern
```python
if precondition_check():
    result = operation()
else:
    result = fallback()
```

### When to Use Each
- **EAFP**: File I/O, dict access, attribute access, race conditions
- **LBYL**: Simple validation, expensive exceptions, multiple checks