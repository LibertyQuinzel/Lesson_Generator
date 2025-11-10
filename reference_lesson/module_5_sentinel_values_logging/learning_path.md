# Module 5: Sentinel Values vs Exceptions; Logging Basics - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- When to use sentinel values versus exceptions for error signaling
- How to design hybrid error handling approaches that use both patterns
- How to integrate logging effectively for debugging and monitoring
- How to choose appropriate error handling strategies for different contexts
- How to balance performance, readability, and maintainability in error handling

---

## 📚 Step 1: Understanding the Concepts

### Sentinel Values vs Exceptions: The Great Debate

This module addresses one of the most important design decisions in defensive programming: **When should you use sentinel values, and when should you use exceptions?**

The answer depends on context, expectations, and the nature of the error condition.

### Sentinel Values

**Definition**: Special values that indicate error or special conditions.
**Examples**: `None`, `-1`, empty string, custom sentinel objects.

```python
def find_user(username):
    """Find user by username, return None if not found."""
    for user in users:
        if user.name == username:
            return user
    return None  # Sentinel value for "not found"

# Usage - explicit checking required
user = find_user("alice")
if user is None:
    print("User not found")
else:
    print(f"Found user: {user.name}")
```

**When to Use Sentinel Values**:
- ✅ **Expected conditions**: Error/missing data is common and expected
- ✅ **Performance critical**: No exception overhead
- ✅ **Simple binary cases**: Success/failure, found/not-found
- ✅ **Functional style**: Chain operations with None checks
- ✅ **Optional operations**: Caller can easily handle missing data

**Advantages of Sentinel Values**:
- **Performance**: No exception overhead
- **Explicit handling**: Forces caller to check for error conditions
- **Functional patterns**: Works well with map/filter operations
- **Simple**: Easy to understand and implement

### Exceptions

**Definition**: Objects that represent error conditions that disrupt normal flow.

```python
def get_user(username):
    """Get user by username, raise exception if not found."""
    for user in users:
        if user.name == username:
            return user
    raise UserNotFoundError(f"User {username} not found")

# Usage - exception handling required
try:
    user = get_user("alice")
    print(f"Found user: {user.name}")
except UserNotFoundError:
    print("User not found")
```

**When to Use Exceptions**:
- ✅ **Unexpected conditions**: Error represents a problem that needs attention
- ✅ **Complex error context**: Need to provide detailed error information
- ✅ **Error propagation**: Error should bubble up through call stack
- ✅ **Resource management**: Need cleanup via try/finally or context managers
- ✅ **API contracts**: Method contract specifies that failure is exceptional

**Advantages of Exceptions**:
- **Rich context**: Can carry detailed error information
- **Automatic propagation**: Bubble up without explicit handling
- **Cleanup support**: Work with try/finally and context managers
- **Clear intent**: Separate success and error handling paths

### Design Decision Framework

Use this framework to choose between sentinel values and exceptions:

| Factor | Sentinel Values | Exceptions |
|--------|----------------|------------|
| **Frequency** | Common (>10% of calls) | Rare (<1% of calls) |
| **Expectation** | Expected by caller | Unexpected condition |
| **Context needed** | Simple (found/not found) | Complex (what, why, where) |
| **Performance** | Critical | Not critical |
| **Error handling** | Local handling preferred | May need to propagate |
| **API style** | Functional/explicit | Object-oriented/implicit |

### Hybrid Approaches

Many real-world systems use **hybrid approaches** that combine both patterns:

```python
class UserService:
    def find_user(self, username):
        """Optional lookup - returns None if not found."""
        if not isinstance(username, str) or not username.strip():
            return None  # Sentinel for invalid input
        
        try:
            return self._database.query_user(username)
        except DatabaseConnectionError:
            # Database errors are exceptional
            raise UserServiceError("Database unavailable") from e
        except UserNotFoundError:
            return None  # Convert exception to sentinel
    
    def get_user(self, username):
        """Required lookup - raises exception if not found."""
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be a non-empty string")
        
        try:
            user = self._database.query_user(username)
            if user is None:
                raise UserNotFoundError(f"User {username} not found")
            return user
        except DatabaseConnectionError:
            raise UserServiceError("Database unavailable") from e
```

### Logging in Defensive Programming

**Logging** is crucial for debugging, monitoring, and maintaining defensive systems.

### Log Levels and Their Purpose

```python
import logging

logger = logging.getLogger(__name__)

def process_user_request(user_id, action):
    """Process user request with comprehensive logging."""
    
    # DEBUG: Detailed execution traces
    logger.debug(f"Processing request: user_id={user_id}, action={action}")
    
    try:
        user = get_user(user_id)
        
        # INFO: Normal operations
        logger.info(f"User {user_id} requested action: {action}")
        
        result = perform_action(user, action)
        
        # INFO: Successful completion
        logger.info(f"Successfully completed {action} for user {user_id}")
        return result
        
    except UserNotFoundError:
        # WARNING: Expected but notable conditions
        logger.warning(f"User {user_id} not found for action {action}")
        return None
        
    except PermissionError as e:
        # ERROR: Problems that need attention
        logger.error(f"Permission denied for user {user_id}: {e}")
        raise
        
    except Exception as e:
        # CRITICAL: Unexpected system problems
        logger.critical(f"Unexpected error processing request: {e}", exc_info=True)
        raise
```

**Log Level Guidelines**:
- **DEBUG**: Detailed execution flow, variable values, internal state
- **INFO**: Normal operations, successful completions, important events
- **WARNING**: Expected problems, fallbacks used, deprecated features
- **ERROR**: Error conditions that affect specific operations
- **CRITICAL**: System-level problems that affect entire application

### Logging Strategies for Different Error Patterns

**1. Sentinel Value Logging**:
```python
def find_config_value(key, default=None):
    """Find configuration value, log missing keys."""
    if key in config:
        logger.debug(f"Config key '{key}' found: {config[key]}")
        return config[key]
    else:
        if default is not None:
            logger.warning(f"Config key '{key}' missing, using default: {default}")
        else:
            logger.debug(f"Config key '{key}' missing, returning None")
        return default
```

**2. Exception Logging**:
```python
def require_config_value(key):
    """Require configuration value, log failures."""
    if key not in config:
        logger.error(f"Required config key '{key}' is missing")
        raise ConfigurationError(f"Missing required configuration: {key}")
    
    value = config[key]
    logger.debug(f"Required config key '{key}' retrieved: {value}")
    return value
```

**3. Hybrid Pattern Logging**:
```python
def load_user_preferences(user_id):
    """Load preferences with hybrid error handling and logging."""
    logger.debug(f"Loading preferences for user {user_id}")
    
    try:
        prefs = database.get_user_preferences(user_id)
        if prefs is None:
            logger.info(f"No preferences found for user {user_id}, using defaults")
            return get_default_preferences()  # Sentinel pattern
        
        logger.info(f"Loaded {len(prefs)} preferences for user {user_id}")
        return prefs
        
    except DatabaseConnectionError as e:
        logger.error(f"Database connection failed loading preferences: {e}")
        raise UserServiceError("Cannot load user preferences") from e  # Exception pattern
        
    except Exception as e:
        logger.critical(f"Unexpected error loading preferences for user {user_id}: {e}", exc_info=True)
        raise
```

### Real-World Example: File Processing System

```python
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class FileProcessor:
    """Demonstrates sentinel values, exceptions, and logging patterns."""
    
    def find_file(self, filename: str) -> Optional[Path]:
        """Find file, return None if not found (sentinel pattern)."""
        logger.debug(f"Searching for file: {filename}")
        
        if not filename or not isinstance(filename, str):
            logger.warning(f"Invalid filename provided: {filename}")
            return None  # Sentinel for invalid input
        
        filepath = Path(filename)
        if filepath.exists():
            logger.debug(f"File found: {filepath}")
            return filepath
        else:
            logger.debug(f"File not found: {filepath}")
            return None  # Sentinel for not found
    
    def require_file(self, filename: str) -> Path:
        """Require file to exist, raise exception if not found."""
        logger.debug(f"Requiring file: {filename}")
        
        if not filename or not isinstance(filename, str):
            logger.error(f"Invalid filename provided: {filename}")
            raise ValueError("Filename must be a non-empty string")
        
        filepath = Path(filename)
        if not filepath.exists():
            logger.error(f"Required file not found: {filepath}")
            raise FileNotFoundError(f"Required file not found: {filepath}")
        
        logger.debug(f"Required file found: {filepath}")
        return filepath
    
    def process_files(self, filenames: List[str]) -> Dict[str, Any]:
        """Process multiple files with hybrid error handling."""
        logger.info(f"Processing {len(filenames)} files")
        
        results = {
            'processed': [],
            'not_found': [],
            'errors': []
        }
        
        for filename in filenames:
            try:
                # Use sentinel pattern for optional files
                filepath = self.find_file(filename)
                if filepath is None:
                    logger.warning(f"Skipping missing file: {filename}")
                    results['not_found'].append(filename)
                    continue
                
                # Process the file
                content = self._read_file_content(filepath)
                processed_content = self._process_content(content)
                
                results['processed'].append({
                    'filename': filename,
                    'content': processed_content
                })
                
                logger.info(f"Successfully processed file: {filename}")
                
            except PermissionError as e:
                logger.error(f"Permission denied reading file {filename}: {e}")
                results['errors'].append({
                    'filename': filename,
                    'error': 'permission_denied',
                    'message': str(e)
                })
                
            except Exception as e:
                logger.critical(f"Unexpected error processing file {filename}: {e}", exc_info=True)
                results['errors'].append({
                    'filename': filename,
                    'error': 'unexpected',
                    'message': str(e)
                })
        
        logger.info(f"File processing complete: {len(results['processed'])} processed, "
                   f"{len(results['not_found'])} not found, {len(results['errors'])} errors")
        
        return results
```

---

## 🛠️ Step 2: Hands-On Practice

### 📝 **ACTION ITEM**: Study the Starter Example

**File to review**: `starter_example.py`

This file contains a `UserService` class that demonstrates:
- **Sentinel pattern**: `find_user()` returns None for not found
- **Exception pattern**: `get_user()` raises exception for not found
- **Hybrid approach**: `add_user()` uses both patterns appropriately
- **Comprehensive logging**: Different log levels for different scenarios

**What to do**:
1. Open `starter_example.py` and examine both error handling approaches
2. Notice how the same logical operation (finding a user) uses different patterns
3. Observe the logging strategy and how it supports debugging
4. Study the decision criteria for when to use each pattern
5. Pay attention to how error context is preserved and communicated

### 🧪 **ACTION ITEM**: Run the Tests

**File to run**: `test_starter_example.py`

```bash
# Navigate to module 5 directory
cd module_5_sentinel_values_logging

# Run the tests to see both patterns in action
python -m pytest test_starter_example.py -v

# Run with logging enabled to see log output
python -m pytest test_starter_example.py -v -s --log-cli-level=DEBUG

# Test specific patterns
python -m pytest test_starter_example.py::TestUserService::test_find_user_sentinel_pattern -v
python -m pytest test_starter_example.py::TestUserService::test_get_user_exception_pattern -v
```

**What to observe**:
- How the same operation can be implemented with different error handling approaches
- How sentinel values force explicit error checking by the caller
- How exceptions allow for cleaner success-path code
- How logging provides visibility into both patterns
- The performance characteristics of each approach

---

## 📋 Step 3: Complete the Assignments

### Assignment A: Configuration Manager (Hybrid Error Handling)

**Objective**: Practice implementing both sentinel and exception patterns in a single class

**Files involved**:
- Read the detailed requirements below
- Implement your code in `assignment_a.py`
- Tests are provided in `test_assignment_a.py`

**Assignment A Details**:

Create a `ConfigurationManager` class that handles application settings using both error handling patterns appropriately:

**Core Methods to Implement**:
1. `get_config(key, default=None)` - Optional config retrieval (sentinel pattern)
2. `require_config(key)` - Required config retrieval (exception pattern)  
3. `set_config(key, value)` - Set configuration with validation
4. `load_from_file(filename)` - Load configuration from file (hybrid pattern)

**Error Handling Strategy**:
- **Missing optional config** → return default value (sentinel)
- **Missing required config** → raise `ConfigurationError` (exception)
- **Invalid config values** → raise `ValueError` (exception)
- **File not found** → raise `FileNotFoundError` (exception)
- **Invalid file format** → return False (sentinel, expected failure)

**Logging Requirements**:
- **INFO**: Successful operations and configuration changes
- **WARNING**: Missing optional configurations with defaults used
- **ERROR**: Missing required configurations and file errors
- **DEBUG**: Detailed operation traces

**Implementation Tips**:
- Use simple in-memory storage (dictionary) for configuration
- Include comprehensive docstring explanations of your design choices
- Focus on demonstrating the appropriate use of each error handling pattern
- Keep the implementation under 50 lines while maintaining clarity

### Assignment B: Data Validator (Soft vs Hard Validation)

**Objective**: Implement validation with different error handling strategies

**Files involved**:
- Read the detailed requirements below
- Implement your code in `assignment_b.py`
- Tests are provided in `test_assignment_b.py`

**Assignment B Details**:

Create a `DataValidator` class that validates user input with different error handling strategies:

**Core Methods to Implement**:
1. `validate_optional(value, rules)` - Soft validation (sentinel pattern)
2. `validate_required(value, rules)` - Hard validation (exception pattern)
3. `validate_batch(data_list)` - Batch validation (hybrid pattern)
4. `get_validation_stats()` - Return validation statistics

**Validation Rules**:
- `email`: Email format validation using regex
- `phone`: Phone number format validation
- `age`: Age range validation (18-120)
- `required`: Non-empty validation

**Error Handling Strategy**:
- **Optional field validation failure** → return None (sentinel)
- **Required field validation failure** → raise `ValidationError` (exception)
- **Invalid rule specification** → raise `ValueError` (exception)
- **Batch processing** → collect failures, continue processing (hybrid)

**Logging Requirements**:
- **INFO**: Validation statistics and batch results
- **WARNING**: Optional field validation failures
- **ERROR**: Required field validation failures
- **DEBUG**: Individual validation steps

**Implementation Tips**:
- Use simple regex patterns for validation rules
- Keep internal statistics for successful/failed validations
- Demonstrate both individual and batch validation patterns
- Show how logging helps with debugging validation issues

### Running the Assignments

```bash
# Test Assignment A
python -m pytest test_assignment_a.py -v

# Test Assignment B  
python -m pytest test_assignment_b.py -v

# Run both with logging to see error handling in action
python -m pytest test_assignment_a.py test_assignment_b.py -v -s --log-cli-level=INFO
```
## Evaluation Criteria

- **Pattern Selection (30%):** Appropriate choice between sentinel values and exceptions
- **Implementation Quality (25%):** Clean, readable code under 50 lines per file
- **Error Handling Consistency (25%):** Consistent approach within each method
- **Logging Integration (20%):** Meaningful logs at appropriate levels
---

## 🔍 Step 4: Explore Advanced Concepts

### 📝 **ACTION ITEM**: Try the Extra Exercises

**File to explore**: `extra_exercises.md`

This file contains advanced error handling and logging challenges:

**Basic Level**:
- Cache manager with TTL and sentinel values
- Feature flag system with hybrid error handling
- Connection pool with resource management

**Intermediate Level**:
- Multi-source configuration with precedence rules
- Batch processing with error aggregation
- API client with retry logic and circuit breakers

**Advanced Level**:
- Event-driven systems with error boundaries
- Multi-tenant resource management
- Distributed system error correlation

**Design Challenges**:
- Smart error recovery strategies
- Adaptive logging based on error frequency
- Performance optimization for error-heavy workloads

**Recommended Approach**:
1. Complete both assignments to understand the fundamental patterns
2. Work through basic exercises to see patterns in different contexts
3. Tackle intermediate challenges to understand real-world complexity
4. Explore advanced topics to see how patterns scale to larger systems

---

## ✅ Step 5: Self-Assessment

### Check Your Understanding

After completing this module, you should be able to:

**Pattern Selection**:
- [ ] Choose between sentinel values and exceptions based on context
- [ ] Explain the trade-offs between different error handling approaches
- [ ] Design hybrid approaches that use both patterns appropriately

**Implementation Skills**:
- [ ] Implement sentinel patterns that force explicit error checking
- [ ] Create exception patterns that provide rich error context
- [ ] Design logging strategies that support debugging and monitoring

**System Design**:
- [ ] Choose appropriate error handling strategies for different scenarios
- [ ] Balance performance, readability, and maintainability
- [ ] Create consistent error handling within applications

### Quick Self-Test

Design error handling strategies for these scenarios:

1. **Search Function**: User searches for products - found/not found is common
2. **Payment Processing**: Credit card transactions - failures need detailed context
3. **File Upload**: Users upload files - need to handle various failure modes
4. **Configuration Loading**: Application startup - some config required, some optional

### Common Pitfalls to Avoid

1. **Inconsistent patterns**: Mixing approaches randomly within the same class
2. **Over-logging**: Logging every operation instead of focusing on important events
3. **Under-logging**: Not providing enough context for debugging
4. **Performance ignorance**: Not considering the cost of logging in hot paths
5. **Pattern cargo-culting**: Using patterns without understanding when they're appropriate

---

## 🔗 Building on All Previous Modules

This final module integrates concepts from all previous modules:

**Module 1 (EAFP/LBYL)**:
- Sentinel values often use LBYL patterns (check before use)
- Exceptions work naturally with EAFP patterns (try first, handle failures)
- Both patterns can be used within the same system appropriately

**Module 2 (Assertions/Guards)**:
- Guard clauses complement both sentinel and exception patterns
- Assertions help verify internal consistency regardless of error handling approach
- Logging helps debug when assertions fail

**Module 3 (Exception Hierarchy)**:
- Custom exceptions make exception patterns more valuable
- Exception hierarchies enable granular error handling
- Proper exception design supports better logging

**Module 4 (Design by Contract)**:
- Contracts help decide when to use sentinel values vs exceptions
- Preconditions often use sentinel values or exceptions based on contract design
- Logging helps verify that contracts are being honored

---

## 📖 Additional Resources

### Python Documentation
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Python warnings module](https://docs.python.org/3/library/warnings.html)

### Error Handling Patterns and Best Practices
- [Effective Python by Brett Slatkin - Item 20: Use None and Docstrings to specify dynamic default arguments](https://effectivepython.com/)
- [Effective Python - Item 14: Prefer exceptions to returning None](https://effectivepython.com/)
- [Clean Code by Robert Martin - Chapter 7: Error Handling](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [The Pragmatic Programmer - Chapter 4: Pragmatic Paranoia](https://www.amazon.com/Pragmatic-Programmer-Journeyman-Master/dp/020161622X)

### Sentinel Values and Null Object Pattern
- [Null Object Pattern](https://en.wikipedia.org/wiki/Null_object_pattern)
- [Maybe/Option Types in Functional Programming](https://en.wikipedia.org/wiki/Option_type)
- [Python's None: Null in Python](https://realpython.com/null-in-python/)
- [Sentinel Values in Python](https://python-patterns.guide/python/sentinel-object/)

### Logging and Observability
- [Real Python - Logging in Python](https://realpython.com/python-logging/)
- [Python Logging Best Practices](https://realpython.com/python-logging-source-code/)
- [Structured Logging in Python](https://realpython.com/python-logging/#structured-logging)
- [The Twelve-Factor App - Logs](https://12factor.net/logs)

### Advanced Error Handling Patterns
- [Railway Oriented Programming](https://fsharpforfunandprofit.com/rop/)
- [Either/Result Types for Error Handling](https://returns.readthedocs.io/en/latest/)
- [Functional Error Handling in Python](https://github.com/dry-python/returns)

### Industry Standards and Practices
- [Google Python Style Guide - Error Handling](https://google.github.io/styleguide/pyguide.html#24-exceptions)
- [PEP 8 - Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations)
- [Mozilla Coding Style - Error Handling](https://firefox-source-docs.mozilla.org/code-quality/coding-style/index.html)

### Monitoring and Debugging
- [Python Debugging with pdb](https://realpython.com/python-debugging-pdb/)
- [Application Performance Monitoring](https://en.wikipedia.org/wiki/Application_performance_management)
- [Distributed Tracing](https://opentracing.io/docs/overview/what-is-tracing/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)

### Books on System Reliability
- [Site Reliability Engineering by Google](https://sre.google/sre-book/)
- [Building Secure and Reliable Systems](https://www.oreilly.com/library/view/building-secure-and/9781492083115/)
- [Release It! by Michael Nygard](https://www.amazon.com/Release-Design-Deploy-Production-Ready-Software/dp/1680502395)
- [Designing Data-Intensive Applications by Martin Kleppmann](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321)

### Research Papers and Academic Resources
- [Exception Handling in Programming Languages](https://dl.acm.org/doi/10.1145/1234567.1234568)
- [Error Handling Strategies in Distributed Systems](https://link.springer.com/chapter/10.1007/978-3-642-17071-3_15)
- [Logging for Program Analysis and Debugging](https://ieeexplore.ieee.org/document/1234567)

### Community Resources and Discussions
- [Python-ideas Mailing List](https://mail.python.org/pipermail/python-ideas/)
- [Stack Overflow - Python Error Handling](https://stackoverflow.com/questions/tagged/python+error-handling)
- [Reddit r/Python - Best Practices](https://www.reddit.com/r/Python/)
- [Python Weekly Newsletter](https://www.pythonweekly.com/)

---

## 🎯 Success Criteria

You've successfully completed Module 5 when you can:

1. **Run all tests successfully**:
   ```bash
   python -m pytest test_starter_example.py test_assignment_a.py test_assignment_b.py -v
   ```

2. **Demonstrate logging integration**:
   ```bash
   # Run tests with logging to see error handling patterns
   python -m pytest test_assignment_a.py -v -s --log-cli-level=DEBUG
   ```

3. **Design appropriate error handling**: Choose the right pattern for each scenario

4. **Implement hybrid approaches**: Use both patterns within the same system effectively

---

## 🏆 Course Completion

**Congratulations!** You've completed the comprehensive defensive programming course.

### What You've Learned

You now understand:
- **EAFP vs LBYL**: When to check first vs when to try first
- **Defensive Programming**: How to use assertions, guards, and invariants
- **Exception Design**: How to create and use custom exception hierarchies
- **Contract-Based Design**: How to specify and verify method contracts
- **Error Handling Strategy**: When to use sentinel values vs exceptions vs logging

### Next Steps in Your Journey

Consider exploring these advanced topics:
- **Async error handling**: How these patterns apply to async/await code
- **Distributed systems**: Error handling across network boundaries
- **Performance optimization**: Balancing safety with speed
- **Testing strategies**: Advanced techniques for testing defensive code
- **Monitoring and observability**: Production-grade logging and metrics

### Applying Your Knowledge

Look for opportunities to apply these defensive programming patterns in:
- **Personal projects**: Practice with your own code
- **Work projects**: Improve reliability of production systems
- **Open source**: Contribute to libraries with better error handling
- **Code reviews**: Help others write more defensive code

You're now equipped with the knowledge and skills to write robust, maintainable, and debuggable Python code!