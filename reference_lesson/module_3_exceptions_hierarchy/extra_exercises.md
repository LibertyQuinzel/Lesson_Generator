# Module 3 Extra Exercises: Python Exception Hierarchy and Custom Exceptions

## Quiz Questions

### 1. Multiple Choice
Which exception should most custom exceptions inherit from?
a) BaseException
b) Exception  
c) RuntimeError
d) ValueError

**Answer: b) Exception - Most custom exceptions should inherit from Exception, not BaseException**

### 2. True/False
You should always catch the most general exception (Exception) to handle all errors.

**Answer: False - Catch specific exceptions when possible, general exceptions only when necessary**

### 3. Fill in the Blanks
Complete this custom exception hierarchy:
```python
class DatabaseError(______):
    pass

class ConnectionError(______):
    pass
```

**Answer: Exception, DatabaseError**

## Practical Exercises

### Exercise 1: Exception Hierarchy Design
Design an exception hierarchy for a web API with these error types:
- Authentication errors
- Authorization errors  
- Validation errors
- Server errors

### Exercise 2: Exception Chaining
Rewrite this code to use exception chaining:
```python
try:
    data = json.loads(text)
except json.JSONDecodeError:
    raise ValueError("Invalid JSON data")
```

### Exercise 3: Error Boundaries
Implement an error boundary that catches internal exceptions and converts them to user-friendly messages.

## Cheat Sheet

### Exception Hierarchy Best Practices

**Custom Exception Structure:**
```python
class MyBaseError(Exception):
    """Base exception for my module."""
    pass

class SpecificError(MyBaseError):
    """Specific error type."""
    pass
```

**Exception with Context:**
```python
class ValidationError(Exception):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field
```

**Exception Chaining:**
```python
try:
    risky_operation()
except SomeError as e:
    raise MyError("Custom message") from e
```

### When to Create Custom Exceptions
- Domain-specific error conditions
- Need for structured error information
- Different handling for different error types
- API error responses with specific codes

### Built-in Exception Hierarchy
```
BaseException
├── SystemExit
├── KeyboardInterrupt  
└── Exception
    ├── ValueError
    ├── TypeError
    ├── RuntimeError
    └── ... (your custom exceptions here)
```