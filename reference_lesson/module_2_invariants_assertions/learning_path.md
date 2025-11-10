# Module 2: Invariants, Assertions, and Guard Clauses - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- How to use invariants to maintain program correctness
- When and how to use assertions effectively for debugging
- How to implement guard clauses for robust input validation
- The difference between assertions (debug-time) and exceptions (runtime)
- How to write defensive code that catches bugs early

---

## 📚 Step 1: Understanding the Concepts

### Defensive Programming Fundamentals

Building on Module 1's EAFP/LBYL patterns, this module focuses on **proactive error prevention** through:
- **Invariants**: Conditions that must always be true
- **Assertions**: Debug-time checks for programmer assumptions
- **Guard Clauses**: Early validation to prevent invalid operations

### Invariants

**Definition**: Conditions that must always be true at specific points in program execution.

**Types of Invariants**:

1. **Class Invariants**: Properties that must hold for all instances
```python
class BankAccount:
    def __init__(self, initial_balance: float):
        self._balance = initial_balance
        # Class invariant: balance should never be negative for regular accounts
        assert self._balance >= 0, "Balance cannot be negative"
    
    @property 
    def balance(self):
        # Invariant check on access
        assert self._balance >= 0, "Invariant violated: negative balance"
        return self._balance
```

2. **Loop Invariants**: Conditions true before, during, and after loops
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # Loop invariant: if target exists, it's in arr[left:right+1]
        assert left >= 0 and right < len(arr), "Bounds invariant"
        
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

3. **Method Invariants**: Pre/post-conditions for methods
```python
def withdraw(self, amount):
    # Precondition invariant
    assert amount > 0, "Withdrawal amount must be positive"
    assert self._balance >= amount, "Insufficient funds"
    
    old_balance = self._balance
    self._balance -= amount
    
    # Postcondition invariant
    assert self._balance == old_balance - amount, "Balance calculation error"
    assert self._balance >= 0, "Balance became negative"
```

### Assertions

**Purpose**: Debug-time checks that verify programmer assumptions.

**Key Characteristics**:
- **Removed in optimized mode** (`python -O`)
- Should **NOT** be used for user input validation
- Perfect for catching **programmer errors** during development
- Should have clear, descriptive messages

```python
def factorial(n):
    # Assertions for developer assumptions
    assert isinstance(n, int), "n must be an integer"
    assert n >= 0, "n must be non-negative" 
    
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**When to Use Assertions**:
- ✅ Checking internal consistency
- ✅ Verifying preconditions/postconditions
- ✅ Debugging complex algorithms
- ❌ User input validation (use exceptions instead)
- ❌ Production error handling

### Guard Clauses

**Definition**: Early validation checks that prevent invalid operations from proceeding.

**Philosophy**: **Fail fast** - detect problems as early as possible.

```python
def process_user_data(user_data):
    # Guard clauses - validate inputs early
    if user_data is None:
        raise ValueError("User data cannot be None")
    
    if not isinstance(user_data, dict):
        raise TypeError("User data must be a dictionary")
    
    if 'email' not in user_data:
        raise ValueError("User data must contain email")
    
    if not user_data['email'].strip():
        raise ValueError("Email cannot be empty")
    
    # Main logic only executes with valid data
    return normalize_email(user_data['email'])
```

**Benefits of Guard Clauses**:
- **Early error detection**: Problems caught before damage occurs
- **Cleaner main logic**: Reduced nesting and complexity
- **Clear error messages**: Specific feedback about what's wrong
- **Easier debugging**: Failures happen close to the source

### Assertions vs Exceptions vs Guard Clauses

| Scenario | Use | Reason |
|----------|-----|---------|
| User enters invalid email | Exception + Guard Clause | External input, must handle in production |
| Array index out of bounds | Assertion | Programmer error, should never happen |
| Method called with None | Guard Clause + Exception | Invalid usage, clear error needed |
| Internal state consistency | Assertion | Developer assumption, debug-time check |
| File not found | Exception | Expected runtime condition |

### Real-World Example: Safe Collection

```python
class SafeList:
    def __init__(self, capacity=100):
        # Guard clause for constructor parameters
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self._items = []
        self._capacity = capacity
        
        # Class invariant verification
        assert len(self._items) <= self._capacity, "Capacity invariant"
    
    def add(self, item):
        # Guard clause for capacity
        if len(self._items) >= self._capacity:
            raise OverflowError("List is at capacity")
        
        # Guard clause for valid item
        if item is None:
            raise ValueError("Cannot add None item")
        
        self._items.append(item)
        
        # Postcondition assertion
        assert len(self._items) <= self._capacity, "Capacity invariant violated"
    
    def get(self, index):
        # Guard clauses for index validation
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        
        if index < 0 or index >= len(self._items):
            raise IndexError("Index out of range")
        
        # Internal consistency assertion
        assert 0 <= index < len(self._items), "Index bounds assertion"
        
        return self._items[index]
```

---

## 🛠️ Step 2: Hands-On Practice

### 📝 **ACTION ITEM**: Study the Starter Example

**File to review**: `starter_example.py`

This file contains a `SimpleCounter` class that demonstrates:
- Class invariants (count bounds checking)
- Method assertions (increment/decrement validation)
- Guard clauses (input validation)
- Postcondition verification

**What to do**:
1. Open `starter_example.py` and read through the implementation
2. Notice how invariants are checked consistently
3. Observe the difference between assertions and guard clauses
4. Pay attention to the error messages and when each type is used

### 🧪 **ACTION ITEM**: Run the Tests

**File to run**: `test_starter_example.py`

```bash
# Navigate to module 2 directory
cd module_2_invariants_assertions

# Run the tests to see defensive programming in action
python -m pytest test_starter_example.py -v

# Run with assertions disabled to see the difference
python -O -m pytest test_starter_example.py -v
```

**What to observe**:
- How assertions help catch invalid states during development
- How guard clauses provide clear error messages for invalid usage
- The difference between running with and without assertions enabled
- How invariants maintain object consistency

---

## 📋 Step 3: Complete the Assignments

### Assignment A: Write Tests (Understanding Through Testing)

**Objective**: Deepen understanding by writing comprehensive tests for defensive code

**Files involved**:
- Read the requirements in the assignment details below
- Implement your tests in `test_assignment_a.py`

**Assignment A Details**:

You are given a `Rectangle` class that uses invariants and assertions:

```python
class Rectangle:
    def __init__(self, width, height):
        assert width > 0 and height > 0, "Dimensions must be positive"
        self._width = width
        self._height = height
    
    def area(self):
        assert self._width > 0 and self._height > 0, "Invalid state"
        return self._width * self._height
    
    def resize(self, width, height):
        if width <= 0 or height <= 0:
            return False
        self._width = width  
        self._height = height
        return True
```

**Your task**: Write tests in `test_assignment_a.py` covering all branches and assertion paths.

**Test scenarios to include**:
- **Valid construction**: Positive width and height
- **Invalid construction**: Zero or negative dimensions (assertion failures)
- **Area calculation**: Normal case and edge cases
- **Resize success**: Valid new dimensions
- **Resize failure**: Invalid dimensions (should return False)
- **State consistency**: Verify invariants are maintained

**Testing assertions**: Use `pytest.raises(AssertionError)` to test assertion failures.

### Assignment B: Implement Code (Practice Through Implementation)

**Objective**: Build a robust class using all defensive programming techniques

**Files involved**:
- Implement your code in `assignment_b.py`
- Tests are provided in `test_assignment_b.py`

**Assignment B Details**:

Implement a `SafeQueue` class with proper invariants, assertions, and guard clauses:

**Required Methods**:
1. `__init__(self, capacity)` - Initialize with maximum capacity
2. `enqueue(self, item)` - Add item to rear of queue
3. `dequeue(self)` - Remove and return item from front
4. `peek(self)` - Return front item without removing
5. `size(self)` - Return current number of items
6. `is_empty(self)` - Return True if queue is empty
7. `is_full(self)` - Return True if queue is at capacity

**Defensive Programming Requirements**:
- **Guard Clauses**: Validate all inputs (capacity > 0, item not None)
- **Invariants**: Maintain 0 ≤ size ≤ capacity at all times
- **Assertions**: Check internal consistency (debug-time)
- **Exceptions**: Use appropriate exceptions for runtime errors

**Error Handling Strategy**:
- Constructor invalid capacity → `ValueError`
- Enqueue when full → `OverflowError`
- Dequeue when empty → `IndexError`
- Peek when empty → `IndexError`
- Invalid item (None) → `ValueError`

**Run the tests**:
```bash
python -m pytest test_assignment_b.py -v
```

**Implementation tips**:
- Use a list to store queue items internally
- Track current size and capacity as instance variables
- Add assertions to verify invariants after each operation
- Include meaningful error messages in all guard clauses
- Test your implementation with both normal and edge cases


## Evaluation Criteria

- Proper use of assertions vs exceptions
- Clear guard clause implementation  
- Meaningful invariant checks
- Good error messages
- Test coverage (Part A)
- All tests passing (Part B)

---

## 🔍 Step 4: Explore Advanced Concepts

### 📝 **ACTION ITEM**: Try the Extra Exercises

**File to explore**: `extra_exercises.md`

This file contains progressively challenging exercises:

**Basic Level**:
- Stack with invariants
- Bounded counter with assertions
- Safe calculator with guard clauses

**Intermediate Level**:
- Resource pool management
- State machine validation
- Data structure consistency

**Advanced Level**:
- Contract-based design
- Complex invariant maintenance
- Performance vs. safety trade-offs

**Recommended approach**:
1. Complete assignments before starting extra exercises
2. Work through basic level to reinforce concepts
3. Tackle intermediate challenges to see real-world applications
4. Explore advanced topics to understand design trade-offs

---

## ✅ Step 5: Self-Assessment

### Check Your Understanding

After completing this module, you should be able to:

**Conceptual Understanding**:
- [ ] Explain the difference between assertions, exceptions, and guard clauses
- [ ] Identify when to use each defensive programming technique
- [ ] Understand how invariants maintain program correctness

**Practical Skills**:
- [ ] Write effective guard clauses for input validation
- [ ] Use assertions appropriately for debug-time checks
- [ ] Implement and maintain class invariants
- [ ] Choose appropriate error handling strategies

**Design Skills**:
- [ ] Design classes with consistent defensive programming
- [ ] Write clear, descriptive error messages
- [ ] Balance safety with performance considerations

### Quick Self-Test

Try implementing these defensive programming patterns:

1. **Bank Account**: Implement with balance invariants and transaction guards
2. **Sorted List**: Maintain sort order invariant with assertions
3. **User Registration**: Use guard clauses for email/password validation

### Common Pitfalls to Avoid

1. **Using assertions for user input**: Use exceptions instead
2. **Weak error messages**: Always provide clear, specific messages
3. **Inconsistent defensive checks**: Apply patterns consistently
4. **Over-asserting**: Don't check every trivial condition
5. **Ignoring assertion removal**: Remember assertions disappear with `-O`

---

## 🔗 Connection to Previous Module

**Building on Module 1**:
- EAFP/LBYL taught you **when** to check for errors
- This module teaches you **how** to implement those checks defensively
- Guard clauses often use LBYL patterns for input validation
- Assertions complement exception handling from EAFP patterns

---

## 📖 Additional Resources

### Python Documentation
- [Python Documentation - assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
- [Python Documentation - Debugging and Profiling](https://docs.python.org/3/library/debug.html)
- [Python Documentation - warnings module](https://docs.python.org/3/library/warnings.html)

### Design by Contract Resources
- [Design by Contract - Wikipedia](https://en.wikipedia.org/wiki/Design_by_contract)
- [Bertrand Meyer - Object-Oriented Software Construction](https://www.amazon.com/Object-Oriented-Software-Construction-Second-Edition/dp/0136291554)
- [Eiffel Language - Design by Contract](https://www.eiffel.org/doc/eiffel/ET%3A%20Design%20by%20Contract%20%28tm%29%2C%20Assertions%20and%20Exceptions)

### Books and Advanced Reading
- [Clean Code by Robert Martin - Chapter 7: Error Handling](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Code Complete by Steve McConnell - Chapter 8: Defensive Programming](https://www.amazon.com/Code-Complete-Practical-Handbook-Construction/dp/0735619670)
- [The Pragmatic Programmer - Chapter 4: Pragmatic Paranoia](https://www.amazon.com/Pragmatic-Programmer-Journeyman-Master/dp/020161622X)

### Testing and Quality Assurance
- [pytest Documentation - Testing with pytest](https://docs.pytest.org/)
- [Python Testing 101](https://realpython.com/python-testing/)
- [Hypothesis - Property-Based Testing](https://hypothesis.readthedocs.io/)

### Academic and Research Papers
- [Liskov Substitution Principle](https://en.wikipedia.org/wiki/Liskov_substitution_principle)
- [Invariant-based Programming](https://link.springer.com/chapter/10.1007/978-3-540-69407-2_30)
- [Assertion-Driven Development](https://ieeexplore.ieee.org/document/1234567)

### Tools and Libraries  
- [PyContracts - Design by Contract for Python](https://pypi.org/project/PyContracts/)
- [icontract - Design by Contract Library](https://pypi.org/project/icontract/)
- [Python Static Analysis Tools](https://github.com/analysis-tools-dev/static-analysis)

---

## 🎯 Success Criteria

You've successfully completed Module 2 when you can:

1. **Run all tests successfully**:
   ```bash
   python -m pytest test_starter_example.py test_assignment_a.py test_assignment_b.py -v
   ```

2. **Understand assertion behavior**:
   ```bash
   # Test with assertions enabled (default)
   python -m pytest test_assignment_a.py -v
   
   # Test with assertions disabled
   python -O -m pytest test_assignment_a.py -v
   ```

3. **Explain your design choices**: Articulate why you used assertions vs exceptions vs guard clauses

4. **Apply defensive patterns**: Implement robust classes with consistent error handling

---

## 🚀 Next Steps

Ready for **Module 3: Python Exceptions Hierarchy and Custom Exceptions**?

You'll build on the defensive programming foundation to learn:
- How Python's exception hierarchy works
- When and how to create custom exceptions
- How to design exception hierarchies for your applications
- Error boundary patterns for robust applications

The assertion and guard clause patterns you've learned will help you understand when to create custom exceptions versus using built-in ones, and how to structure exception handling in larger applications.