# Module 3: Python Exception Hierarchy and Custom Exceptions - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Python's built-in exception hierarchy and how to leverage it
- When and how to create custom exceptions effectively
- How to design exception hierarchies for your applications
- Best practices for exception handling and error boundaries
- How to structure exception handling in larger applications

---

## 📚 Step 1: Understanding the Concepts

### Python Exception Hierarchy

Understanding Python's exception hierarchy is crucial for effective error handling:

```
BaseException
├── SystemExit
├── KeyboardInterrupt  
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    ├── LookupError
    │   ├── IndexError
    │   ├── KeyError
    │   └── ValueError
    ├── OSError (IOError)
    │   ├── FileNotFoundError
    │   └── PermissionError
    ├── RuntimeError
    ├── TypeError
    ├── ValueError
    └── ... (many others)
```

### Key Exception Categories

**1. System Exceptions** (inherit from BaseException):
- `SystemExit`: Raised by sys.exit()
- `KeyboardInterrupt`: Ctrl+C interruption
- `GeneratorExit`: Generator cleanup
- **Generally should NOT be caught by application code**

**2. Application Exceptions** (inherit from Exception):
- All exceptions your application should handle
- **Base class for custom exceptions**
- Safe to catch with `except Exception:`

### Specific vs General Exception Handling

```python
# ❌ Too general - catches everything including system exceptions
try:
    risky_operation()
except BaseException:
    handle_error()

# ❌ Still too general - catches all application exceptions
try:
    risky_operation() 
except Exception:
    handle_error()

# ✅ Better - catch specific exceptions
try:
    risky_operation()
except (ValueError, TypeError) as e:
    handle_specific_error(e)
except FileNotFoundError as e:
    handle_file_error(e)
```

### When to Create Custom Exceptions

**Create custom exceptions when**:
- You need **domain-specific error information**
- You want **different handling** for different error types
- You need to **add context** or **error codes**
- You want to **group related errors** under a common base

**Don't create custom exceptions when**:
- Built-in exceptions already express the error appropriately
- You're just renaming existing exceptions without adding value
- The error is truly generic (ValueError, TypeError are often sufficient)

### Designing Custom Exception Hierarchies

**1. Single Custom Exception**:
```python
class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    def __init__(self, message, config_key=None):
        super().__init__(message)
        self.config_key = config_key
```

**2. Exception Hierarchy**:
```python
class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class ConnectionError(DatabaseError):
    """Database connection failed."""
    pass

class QueryError(DatabaseError):
    """Database query failed."""
    def __init__(self, message, query=None):
        super().__init__(message)
        self.query = query

class TransactionError(DatabaseError):
    """Database transaction failed."""
    pass
```

**3. Exception with Error Codes**:
```python
class APIError(Exception):
    """API operation failed."""
    def __init__(self, message, error_code=None, status_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code
        
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {super().__str__()}"
        return super().__str__()
```

### Exception Handling Best Practices

**1. Catch Specific Exceptions**:
```python
def process_user_data(data):
    try:
        user_id = int(data['user_id'])
        return lookup_user(user_id)
    except KeyError:
        raise ValueError("Missing required field: user_id")
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("user_id must be a valid integer")
        raise  # Re-raise if it's a different ValueError
    except UserNotFoundError:
        return None  # This is expected, return sentinel value
```

**2. Exception Chaining**:
```python
def load_config(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigurationError(f"Config file not found: {filename}") from e
    except json.JSONDecodeError as e:
        raise ConfigurationError(f"Invalid JSON in config: {filename}") from e
```

**3. Error Boundaries**:
```python
class UserService:
    def get_user_profile(self, user_id):
        """Error boundary: converts internal errors to domain errors."""
        try:
            # Internal operations that might raise various exceptions
            user_data = self._fetch_user_data(user_id)
            profile = self._build_profile(user_data)
            return profile
        except DatabaseError as e:
            # Convert internal database errors to domain errors
            raise UserServiceError(f"Failed to retrieve user {user_id}") from e
        except ValidationError as e:
            # Convert validation errors to domain errors
            raise UserServiceError(f"Invalid user data for {user_id}") from e
```

### Real-World Example: File Processing System

```python
# Exception hierarchy for file processing
class FileProcessingError(Exception):
    """Base exception for file processing operations."""
    pass

class FileAccessError(FileProcessingError):
    """File cannot be accessed."""
    pass

class FileFormatError(FileProcessingError):
    """File format is invalid or unsupported."""
    def __init__(self, message, expected_format=None, actual_format=None):
        super().__init__(message)
        self.expected_format = expected_format
        self.actual_format = actual_format

class FileValidationError(FileProcessingError):
    """File content validation failed."""
    def __init__(self, message, line_number=None):
        super().__init__(message)
        self.line_number = line_number

# Usage with error boundaries
class DocumentProcessor:
    def process_document(self, filepath):
        """Process document with proper error boundaries."""
        try:
            # File access operations
            content = self._read_file(filepath)
            
            # Format validation
            parsed_data = self._parse_content(content)
            
            # Content validation  
            validated_data = self._validate_data(parsed_data)
            
            return self._transform_data(validated_data)
            
        except OSError as e:
            # Convert OS errors to domain errors
            if e.errno == errno.ENOENT:
                raise FileAccessError(f"File not found: {filepath}") from e
            elif e.errno == errno.EACCES:
                raise FileAccessError(f"Permission denied: {filepath}") from e
            else:
                raise FileAccessError(f"Cannot access file: {filepath}") from e
                
        except json.JSONDecodeError as e:
            raise FileFormatError(
                f"Invalid JSON format in {filepath}",
                expected_format="JSON",
                actual_format="invalid JSON"
            ) from e
```

### Exception Handling Patterns

**1. EAFP with Custom Exceptions**:
```python
def get_user_preference(user_id, preference_key):
    try:
        user = User.objects.get(id=user_id)
        return user.preferences[preference_key]
    except User.DoesNotExist:
        raise UserNotFoundError(f"User {user_id} not found")
    except KeyError:
        raise PreferenceNotFoundError(
            f"Preference '{preference_key}' not found for user {user_id}"
        )
```

**2. Exception Translation**:
```python
def save_user_data(user_data):
    """Translate low-level exceptions to domain exceptions."""
    try:
        validated_data = validate_user_data(user_data)
        return database.save(validated_data)
    except ValidationError as e:
        # Translate validation error to domain error
        raise InvalidUserDataError(str(e)) from e
    except DatabaseConnectionError as e:
        # Translate infrastructure error to service error
        raise UserServiceUnavailableError("Cannot save user data") from e
```

---

## 🛠️ Step 2: Hands-On Practice

### 📝 **ACTION ITEM**: Study the Starter Example

**File to review**: `starter_example.py`

This file contains a `UserManager` class that demonstrates:
- Custom exception hierarchy for user management
- Proper exception inheritance and initialization
- Error boundaries and exception translation
- Context-aware error messages with additional data

**What to do**:
1. Open `starter_example.py` and examine the exception hierarchy
2. Notice how different exceptions inherit from a common base
3. Observe how exceptions carry additional context (user_id, validation rules)
4. Study the error boundary pattern in the service methods

### 🧪 **ACTION ITEM**: Run the Tests

**File to run**: `test_starter_example.py`

```bash
# Navigate to module 3 directory
cd module_3_exceptions_hierarchy

# Run the tests to see exception handling in action
python -m pytest test_starter_example.py -v

# Run specific test categories
python -m pytest test_starter_example.py::TestUserManager::test_exception_hierarchy -v
```

**What to observe**:
- How custom exceptions provide more specific error information
- How exception inheritance allows catching groups of related errors
- How exception chaining preserves the original error context
- How error boundaries convert low-level errors to domain-specific ones

---

## 📋 Step 3: Complete the Assignments

### Assignment A: Write Tests (Exception Testing Mastery)

**Objective**: Master testing exception hierarchies and inheritance relationships

**Files involved**:
- Read the requirements in the assignment details below
- Implement your tests in `test_assignment_a.py`

**Assignment A Details**:

You are given a `FileProcessor` class with custom exceptions:

```python
class ProcessingError(Exception):
    """Base exception for file processing operations."""
    pass

class FileNotFoundError(ProcessingError):
    """Exception raised when file doesn't exist."""
    pass

class InvalidFormatError(ProcessingError):
    """Exception raised when file format is invalid."""
    pass

class FileProcessor:
    def process_file(self, filename):
        if not filename:
            raise ProcessingError("Filename cannot be empty")
        
        if not filename.endswith('.txt'):
            raise InvalidFormatError(f"Invalid format: {filename}")
        
        return f"Processed {filename}"
    
    def read_file(self, filename):
        if filename == "missing.txt":
            raise FileNotFoundError(f"File not found: {filename}")
        return f"Content of {filename}"
```

**Your task**: Write comprehensive tests in `test_assignment_a.py` covering:

**Exception Testing Scenarios**:
- **Specific Exception Types**: Test that correct exception types are raised
- **Exception Messages**: Verify error messages contain relevant information
- **Exception Inheritance**: Test that custom exceptions inherit properly
- **Exception Context**: Verify exceptions carry appropriate context
- **Exception Hierarchy**: Test catching exceptions at different levels

**Test Categories to Include**:
1. **Success Cases**: Valid operations that don't raise exceptions
2. **Specific Exceptions**: Each custom exception type individually
3. **Inheritance Testing**: Catching base class catches derived exceptions
4. **Message Testing**: Exception messages contain expected content
5. **Edge Cases**: Empty strings, None values, boundary conditions

### Assignment B: Implement Code (Custom Exception Design)

**Objective**: Design and implement a complete custom exception hierarchy

**Files involved**:
- Implement your code in `assignment_b.py`
- Tests are provided in `test_assignment_b.py`

**Assignment B Details**:

Implement a `SimpleCalculator` class with a comprehensive custom exception hierarchy:

**Required Exception Hierarchy**:
```python
class CalculatorError(Exception):
    """Base exception for calculator operations."""

class InvalidOperationError(CalculatorError):
    """Raised when operation is not supported."""

class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""

class InvalidInputError(CalculatorError):
    """Raised when input values are invalid."""
```

**Required Methods**:
1. `add(self, a, b)` - Addition with input validation
2. `subtract(self, a, b)` - Subtraction with input validation
3. `multiply(self, a, b)` - Multiplication with input validation
4. `divide(self, a, b)` - Division with zero checking
5. `calculate(self, expression)` - Parse and evaluate expressions

**Exception Handling Requirements**:
- **Input Validation**: Raise `InvalidInputError` for non-numeric inputs
- **Division by Zero**: Raise `DivisionByZeroError` with context
- **Invalid Operations**: Raise `InvalidOperationError` for unsupported operations
- **Error Context**: Include relevant information in exception messages
- **Exception Chaining**: Use `from` clause where appropriate

**Additional Requirements**:
- Add error codes to exceptions for programmatic handling
- Include the invalid input/operation in error messages
- Support both integer and float operations
- Provide clear, user-friendly error messages

**Run the tests**:
```bash
python -m pytest test_assignment_b.py -v
```

**Implementation Tips**:
- Start with the exception hierarchy before implementing methods
- Add `__init__` methods to exceptions for additional context
- Use `isinstance()` for input type checking
- Test each exception type thoroughly
- Consider edge cases like infinity and NaN values


## Evaluation Criteria

- Proper custom exception hierarchy design
- Clear exception messages and error codes
- Correct inheritance relationships
- Test coverage (Part A)
- All tests passing (Part B)


---

## 🔍 Step 4: Explore Advanced Concepts

### 📝 **ACTION ITEM**: Try the Extra Exercises

**File to explore**: `extra_exercises.md`

This file contains advanced exception handling challenges:

**Basic Level**:
- Bank account with transaction exceptions
- File manager with IO exception hierarchy
- Web API client with HTTP exception mapping

**Intermediate Level**:
- Multi-level exception translation
- Exception aggregation for batch operations
- Context managers with custom exceptions

**Advanced Level**:
- Distributed system error boundaries
- Exception recovery strategies
- Performance considerations in exception design

**Recommended Approach**:
1. Complete both assignments before starting extra exercises
2. Focus on understanding exception hierarchy design principles
3. Practice exception chaining and context preservation
4. Explore real-world exception handling patterns

---

## ✅ Step 5: Self-Assessment

### Check Your Understanding

After completing this module, you should be able to:

**Exception Hierarchy Knowledge**:
- [ ] Explain Python's built-in exception hierarchy
- [ ] Choose appropriate base classes for custom exceptions
- [ ] Design exception hierarchies for domain-specific needs

**Custom Exception Design**:
- [ ] Create meaningful custom exceptions with proper inheritance
- [ ] Add context and error codes to exceptions appropriately
- [ ] Design exception hierarchies that support different handling strategies

**Exception Handling Patterns**:
- [ ] Implement error boundaries that translate exceptions
- [ ] Use exception chaining to preserve error context
- [ ] Handle exceptions at appropriate levels of abstraction

### Quick Self-Test

Design exception hierarchies for these scenarios:

1. **E-commerce System**: Order processing, payment, inventory exceptions
2. **Data Pipeline**: Extraction, transformation, loading exceptions
3. **Authentication System**: Login, authorization, session exceptions

### Common Pitfalls to Avoid

1. **Over-engineering**: Don't create exceptions for every possible error
2. **Poor inheritance**: Ensure exceptions inherit from appropriate base classes
3. **Generic exceptions**: Provide specific, actionable error information
4. **Missing context**: Include relevant data in exception objects
5. **Catching too broadly**: Catch specific exceptions, not `Exception`

---

## 🔗 Building on Previous Modules

**Module 1 Connection (EAFP/LBYL)**:
- EAFP patterns work best with well-designed exception hierarchies
- Custom exceptions make EAFP code more readable and maintainable
- Exception hierarchies enable granular error handling in EAFP style

**Module 2 Connection (Assertions/Guards)**:
- Guard clauses often raise custom exceptions for invalid inputs
- Assertions complement exceptions for different types of error checking
- Custom exceptions provide better error messages than generic ones

---

## 📖 Additional Resources

### Python Documentation
- [Python Documentation - Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- [Python Documentation - Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Python Documentation - Traceback Module](https://docs.python.org/3/library/traceback.html)
- [Python Documentation - sys.exc_info()](https://docs.python.org/3/library/sys.html#sys.exc_info)

### Python Enhancement Proposals (PEPs)
- [PEP 3134 - Exception Chaining and Embedded Tracebacks](https://peps.python.org/pep-3134/)
- [PEP 3151 - Reworking the OS and IO Exception Hierarchy](https://peps.python.org/pep-3151/)
- [PEP 409 - Suppressing Exception Context](https://peps.python.org/pep-0409/)
- [PEP 415 - Implement context suppression with exception attributes](https://peps.python.org/pep-0415/)

### Books and Advanced Reading
- [Effective Python by Brett Slatkin - Item 14: Prefer exceptions to returning None](https://effectivepython.com/)
- [Effective Python by Brett Slatkin - Item 15: Know how closures interact with variable scope](https://effectivepython.com/)
- [Python Tricks by Dan Bader - Exception Handling](https://realpython.com/python-tricks/)
- [Fluent Python by Luciano Ramalho - Chapter 14: Iterables, Iterators, and Generators](https://www.oreilly.com/library/view/fluent-python/9781491946237/)

### Exception Handling Patterns
- [Real Python - Python Exceptions Handling](https://realpython.com/python-exceptions/)
- [Real Python - Working with Python Exceptions](https://realpython.com/python-exceptions/)
- [Martin Fowler - Exception Patterns](https://martinfowler.com/articles/replaceThrowWithNotification.html)

### Error Handling Best Practices
- [Google Python Style Guide - Exceptions](https://google.github.io/styleguide/pyguide.html#24-exceptions)
- [Python Exception Handling Best Practices](https://realpython.com/the-most-diabolical-python-antipattern/)
- [Stack Overflow - Python Exception Handling Best Practices](https://stackoverflow.com/questions/16138232/what-is-the-proper-way-to-handle-exceptions-in-python)

### Testing Exception Handling
- [pytest Documentation - Testing Exceptions](https://docs.pytest.org/en/stable/how-to-use-exceptions.html)
- [unittest Documentation - Testing Exceptions](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises)
- [Testing Exception Handling in Python](https://realpython.com/python-testing/#testing-exceptional-cases)

### Logging and Debugging
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Real Python - Logging in Python](https://realpython.com/python-logging/)
- [Python Debugging with Pdb](https://realpython.com/python-debugging-pdb/)

---

## 🎯 Success Criteria

You've successfully completed Module 3 when you can:

1. **Run all tests successfully**:
   ```bash
   python -m pytest test_starter_example.py test_assignment_a.py test_assignment_b.py -v
   ```

2. **Demonstrate exception hierarchy understanding**:
   ```python
   # You can catch derived exceptions with base class
   try:
       processor.process_file("invalid.pdf")
   except ProcessingError as e:  # Catches InvalidFormatError too
       print(f"Processing failed: {e}")
   ```

3. **Design effective custom exceptions**: Create exceptions that add value beyond built-ins

4. **Implement proper error boundaries**: Translate low-level errors to domain-specific ones

---

## 🚀 Next Steps

Ready for **Module 4: Design by Contract (Pre-/Post-conditions)**?

You'll build on exception handling to learn:
- How to formalize method contracts with preconditions and postconditions
- When to use contracts versus defensive programming
- How to implement contract checking in Python
- Design patterns for robust, contract-based APIs

The exception handling skills you've learned will be essential for implementing contract violations and creating self-documenting, reliable interfaces.