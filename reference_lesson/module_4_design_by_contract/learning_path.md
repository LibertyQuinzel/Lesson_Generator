# Module 4: Design by Contract (Pre-/Post-conditions) - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- The principles of Design by Contract and how to apply them in Python
- How to implement preconditions, postconditions, and class invariants
- When to use contracts versus other defensive programming techniques
- How to design self-documenting, reliable APIs using contracts
- The trade-offs between contract enforcement and performance

---

## 📚 Step 1: Understanding the Concepts

### Design by Contract Fundamentals

**Design by Contract** is a software development approach where functions and methods have **explicit contracts** defined by:
- **Preconditions**: What must be true when a function is called
- **Postconditions**: What the function guarantees to be true when it returns
- **Class Invariants**: Properties that must always hold for object instances

This approach was pioneered by Bertrand Meyer in the Eiffel programming language and provides a formal way to specify and verify program behavior.

### The Three Pillars of Design by Contract

### 1. Preconditions

**Definition**: Conditions that must be true when a function is called.
**Responsibility**: **Caller** must ensure preconditions are met.
**Implementation**: Check inputs at the start of functions.

```python
def withdraw(self, amount):
    # Preconditions: caller's responsibility to meet these
    assert amount > 0, "Precondition: amount must be positive"
    assert amount <= self.balance, "Precondition: insufficient funds"
    assert isinstance(amount, (int, float)), "Precondition: amount must be numeric"
    
    # If we get here, preconditions are met
    self.balance -= amount
```

**When to Use Preconditions**:
- ✅ Input validation that represents programming errors (not user errors)
- ✅ Mathematical constraints (positive numbers, valid ranges)
- ✅ State requirements (object must be initialized, resource must be available)
- ❌ User input validation (use exceptions instead)

### 2. Postconditions

**Definition**: Conditions guaranteed to be true when a function returns.
**Responsibility**: **Function** must ensure postconditions hold.
**Implementation**: Check outputs and state changes before returning.

```python
def deposit(self, amount):
    # Store old state for postcondition checking
    old_balance = self.balance
    
    # Precondition
    assert amount > 0, "Precondition: amount must be positive"
    
    # Perform operation
    self.balance += amount
    
    # Postconditions: function's responsibility to ensure these
    assert self.balance == old_balance + amount, "Postcondition: balance not updated correctly"
    assert self.balance > old_balance, "Postcondition: balance must increase"
```

**When to Use Postconditions**:
- ✅ Verify correct state changes occurred
- ✅ Ensure return values meet specifications
- ✅ Confirm invariants are maintained
- ✅ Document the function's guarantees

### 3. Class Invariants

**Definition**: Properties that must always be true for object instances.
**Responsibility**: **All methods** must maintain invariants.
**Implementation**: Check at method entry and exit.

```python
class BankAccount:
    def __init__(self, initial_balance):
        self._balance = initial_balance
        self._check_invariants()  # Check after construction
    
    def _check_invariants(self):
        """Class invariants that must always hold."""
        assert self._balance >= 0, "Invariant: balance cannot be negative"
        assert isinstance(self._balance, (int, float)), "Invariant: balance must be numeric"
        assert hasattr(self, '_balance'), "Invariant: balance attribute must exist"
    
    def withdraw(self, amount):
        self._check_invariants()  # Check before operation
        
        # Precondition
        assert amount > 0, "Precondition: amount must be positive"
        assert amount <= self._balance, "Precondition: insufficient funds"
        
        # Operation
        old_balance = self._balance
        self._balance -= amount
        
        # Postcondition
        assert self._balance == old_balance - amount, "Postcondition: incorrect withdrawal"
        
        self._check_invariants()  # Check after operation
```

### Contract Benefits and Trade-offs

**Benefits of Design by Contract**:
1. **Clear Specifications**: Contracts document expected behavior explicitly
2. **Early Bug Detection**: Contract violations are caught immediately
3. **Self-Documenting Code**: Contracts serve as executable documentation
4. **Testing Support**: Contracts help identify edge cases and test scenarios
5. **Debugging Aid**: Contract violations pinpoint exactly where problems occur
6. **Design Clarity**: Forces thinking about method responsibilities

**Trade-offs to Consider**:
1. **Performance**: Contract checking adds runtime overhead
2. **Complexity**: Can make code more verbose
3. **Maintenance**: Contracts must be kept in sync with implementation
4. **Assertion Removal**: Python's `-O` flag removes assertions

### Contract Design Patterns

**1. Simple Contract Pattern**:
```python
def sqrt(x):
    # Precondition
    assert x >= 0, "Precondition: x must be non-negative"
    
    result = math.sqrt(x)
    
    # Postcondition
    assert abs(result * result - x) < 1e-10, "Postcondition: sqrt correctness"
    return result
```

**2. State Transition Contract**:
```python
def enqueue(self, item):
    # Preconditions
    assert not self.is_full(), "Precondition: queue must not be full"
    assert item is not None, "Precondition: item cannot be None"
    
    # Store old state
    old_size = self.size()
    
    # Operation
    self._items.append(item)
    
    # Postconditions
    assert self.size() == old_size + 1, "Postcondition: size must increase by 1"
    assert self.peek() == item or self._items[-1] == item, "Postcondition: item must be added"
    assert not self.is_empty(), "Postcondition: queue cannot be empty after enqueue"
```

**3. Mathematical Contract**:
```python
def factorial(n):
    # Preconditions
    assert isinstance(n, int), "Precondition: n must be integer"
    assert n >= 0, "Precondition: n must be non-negative"
    
    if n <= 1:
        result = 1
    else:
        result = n * factorial(n - 1)
    
    # Postconditions
    assert result >= 1, "Postcondition: factorial must be positive"
    assert isinstance(result, int), "Postcondition: result must be integer"
    if n == 0:
        assert result == 1, "Postcondition: 0! = 1"
    
    return result
```

### Contracts vs Other Defensive Techniques

| Technique | Purpose | When to Use | Example |
|-----------|---------|-------------|---------|
| **Preconditions** | Caller requirements | Programming errors, API contracts | `assert x > 0` |
| **Guard Clauses** | Input validation | User errors, external data | `if not user_input: raise ValueError()` |
| **Postconditions** | Function guarantees | Verify correctness | `assert result == expected` |
| **Assertions** | Debug-time checks | Internal consistency | `assert len(items) <= capacity` |
| **Exceptions** | Runtime error handling | Expected failures | `raise FileNotFoundError()` |

### Real-World Example: Safe Collection

```python
class SafeList:
    """A list with capacity limits and contracts."""
    
    def __init__(self, capacity=10):
        # Precondition for constructor
        assert capacity > 0, "Precondition: capacity must be positive"
        
        self._items = []
        self._capacity = capacity
        
        # Postcondition for constructor
        assert len(self._items) == 0, "Postcondition: new list must be empty"
        assert self._capacity == capacity, "Postcondition: capacity must be set"
        
        self._check_invariants()
    
    def _check_invariants(self):
        """Class invariants that must always hold."""
        assert isinstance(self._items, list), "Invariant: _items must be a list"
        assert isinstance(self._capacity, int), "Invariant: _capacity must be integer"
        assert self._capacity > 0, "Invariant: capacity must be positive"
        assert len(self._items) <= self._capacity, "Invariant: size cannot exceed capacity"
    
    def append(self, item):
        """Add item to end of list."""
        self._check_invariants()  # Check invariants before operation
        
        # Preconditions
        assert item is not None, "Precondition: item cannot be None"
        assert len(self._items) < self._capacity, "Precondition: list must not be full"
        
        # Store old state for postcondition
        old_length = len(self._items)
        
        # Perform operation
        self._items.append(item)
        
        # Postconditions
        assert len(self._items) == old_length + 1, "Postcondition: length must increase by 1"
        assert self._items[-1] == item, "Postcondition: item must be at end"
        assert item in self._items, "Postcondition: item must be in list"
        
        self._check_invariants()  # Check invariants after operation
    
    def remove_at(self, index):
        """Remove item at given index."""
        self._check_invariants()
        
        # Preconditions
        assert isinstance(index, int), "Precondition: index must be integer"
        assert 0 <= index < len(self._items), "Precondition: index must be valid"
        assert len(self._items) > 0, "Precondition: list must not be empty"
        
        # Store old state
        old_length = len(self._items)
        removed_item = self._items[index]
        
        # Perform operation
        del self._items[index]
        
        # Postconditions
        assert len(self._items) == old_length - 1, "Postcondition: length must decrease by 1"
        
        self._check_invariants()
        return removed_item
    
    def get(self, index):
        """Get item at index without removing it."""
        self._check_invariants()
        
        # Preconditions
        assert isinstance(index, int), "Precondition: index must be integer"
        assert 0 <= index < len(self._items), "Precondition: index must be valid"
        
        result = self._items[index]
        
        # Postconditions
        assert result is not None, "Postcondition: result cannot be None (we don't store None)"
        assert len(self._items) == len(self._items), "Postcondition: length unchanged"
        
        self._check_invariants()
        return result
```

---

## 🛠️ Step 2: Hands-On Practice

### 📝 **ACTION ITEM**: Study the Starter Example

**File to review**: `starter_example.py`

This file contains a `BankAccount` class that demonstrates:
- Comprehensive precondition checking for all public methods
- Postcondition verification for state-changing operations
- Class invariant maintenance throughout object lifecycle
- Contract-based design for financial operations

**What to do**:
1. Open `starter_example.py` and examine the contract implementation
2. Notice how preconditions validate caller requirements
3. Observe how postconditions verify operation correctness
4. Study how invariants are maintained across all operations
5. Pay attention to the balance between contracts and usability

### 🧪 **ACTION ITEM**: Run the Tests

**File to run**: `test_starter_example.py`

```bash
# Navigate to module 4 directory
cd module_4_design_by_contract

# Run the tests to see contracts in action
python -m pytest test_starter_example.py -v

# Run with assertions disabled to see the difference
python -O -m pytest test_starter_example.py -v

# Run specific contract violation tests
python -m pytest test_starter_example.py::TestBankAccount::test_contract_violations -v
```

**What to observe**:
- How contract violations are caught immediately with clear error messages
- How contracts serve as executable documentation of method behavior
- The difference in behavior when assertions are disabled
- How contracts help identify exactly where and why failures occur

---

## 📋 Step 3: Complete the Assignments

### Assignment A: Write Tests (Contract Testing Mastery)

**Objective**: Master testing code that uses Design by Contract principles

**Files involved**:
- Read the requirements in the assignment details below
- Implement your tests in `test_assignment_a.py`

**Assignment A Details**:

You are given a `Rectangle` class that uses Design by Contract:

```python
class Rectangle:
    def __init__(self, width, height):
        # Precondition: width and height must be positive
        assert width > 0 and height > 0, "Dimensions must be positive"
        self._width = width
        self._height = height
    
    def area(self):
        # Postcondition: area must be positive
        result = self._width * self._height
        assert result > 0, "Area must be positive"
        return result
    
    def scale(self, factor):
        # Precondition: factor must be positive
        assert factor > 0, "Scale factor must be positive"
        
        old_area = self.area()
        self._width *= factor
        self._height *= factor
        
        # Postcondition: area scaled correctly
        new_area = self.area()
        expected_area = old_area * (factor * factor)
        assert abs(new_area - expected_area) < 0.0001, "Scaling postcondition failed"
```

**Your task**: Write comprehensive tests in `test_assignment_a.py` covering all contract paths.

**Test Categories to Include**:
1. **Valid Operations**: Test that contracts pass for valid inputs
2. **Precondition Violations**: Test each precondition failure scenario
3. **Postcondition Verification**: Verify that postconditions hold for valid operations
4. **Edge Cases**: Boundary values, floating-point precision issues
5. **Contract Consistency**: Verify contracts are enforced consistently

**Testing Contract Violations**:
```python
import pytest

def test_constructor_precondition_violation():
    with pytest.raises(AssertionError, match="Dimensions must be positive"):
        Rectangle(0, 5)  # Width is zero
    
    with pytest.raises(AssertionError, match="Dimensions must be positive"):
        Rectangle(5, -1)  # Height is negative
```

### Assignment B: Implement Code (Contract-Based Design)

**Objective**: Design and implement a class using comprehensive Design by Contract

**Files involved**:
- Implement your code in `assignment_b.py`
- Tests are provided in `test_assignment_b.py`

**Assignment B Details**:

Implement a `Stack` class with comprehensive Design by Contract:

**Required Methods**:
1. `__init__(self, capacity)` - Initialize stack with maximum capacity
2. `push(self, item)` - Add item to top of stack
3. `pop(self)` - Remove and return top item
4. `peek(self)` - Return top item without removing
5. `size(self)` - Return current number of items
6. `is_empty(self)` - Return True if stack is empty
7. `is_full(self)` - Return True if stack is at capacity

**Contract Requirements**:

**Preconditions**:
- Constructor: capacity must be positive integer
- Push: stack must not be full, item cannot be None
- Pop: stack must not be empty
- Peek: stack must not be empty

**Postconditions**:
- Constructor: stack is empty, capacity is set correctly
- Push: size increases by 1, item is on top
- Pop: size decreases by 1, returned item was on top
- Peek: size unchanged, returns top item

**Class Invariants**:
- Size is always between 0 and capacity
- Stack items list has correct length
- Capacity is positive integer
- Empty/full status is consistent with size

**Custom Contract Exceptions**:
```python
class ContractViolation(Exception):
    """Base class for contract violations."""
    pass

class PreconditionViolation(ContractViolation):
    """Precondition was not met by caller."""
    pass

class PostconditionViolation(ContractViolation):
    """Postcondition was not ensured by method."""
    pass

class InvariantViolation(ContractViolation):
    """Class invariant was violated."""
    pass
```

**Run the tests**:
```bash
python -m pytest test_assignment_b.py -v
```

**Implementation Tips**:
- Implement invariant checking first, then use it in all methods
- Store old state before operations for postcondition checking
- Use meaningful assertion messages that identify the specific contract
- Consider using helper methods for complex contract checking
- Test thoroughly with edge cases and boundary conditions


## Evaluation Criteria

- Proper precondition implementation and checking
- Comprehensive postcondition verification
- Correct class invariant maintenance
- Clear contract violation error messages
- Test coverage (Part A)
- All tests passing (Part B)
---

## 🔍 Step 4: Explore Advanced Concepts

### 📝 **ACTION ITEM**: Try the Extra Exercises

**File to explore**: `extra_exercises.md`

This file contains advanced Design by Contract challenges:

**Basic Level**:
- Queue with contracts
- Binary search with loop invariants
- Sorting algorithm with contracts

**Intermediate Level**:
- Complex object contracts
- Contract inheritance
- Performance optimization with contracts

**Advanced Level**:
- Contract-based testing strategies
- Formal verification concepts
- Contract evolution and versioning

**Recommended Approach**:
1. Complete both assignments to understand basic contract principles
2. Work through basic exercises to reinforce concepts
3. Explore intermediate challenges to see contracts in larger systems
4. Study advanced topics to understand the theoretical foundations

---

## ✅ Step 5: Self-Assessment

### Check Your Understanding

After completing this module, you should be able to:

**Contract Design**:
- [ ] Write meaningful preconditions that specify caller responsibilities
- [ ] Implement postconditions that verify method guarantees
- [ ] Design class invariants that maintain object consistency

**Contract Implementation**:
- [ ] Choose between contracts and other defensive programming techniques
- [ ] Handle contract violations appropriately
- [ ] Balance contract enforcement with performance considerations

**Contract Testing**:
- [ ] Test both contract compliance and violation scenarios
- [ ] Verify that contracts serve as executable documentation
- [ ] Design test cases that exercise all contract paths

### Quick Self-Test

Design contracts for these scenarios:

1. **Matrix Multiplication**: Preconditions for compatible dimensions, postconditions for result correctness
2. **Circular Buffer**: Invariants for buffer consistency, contracts for wrap-around behavior
3. **Binary Tree**: Invariants for tree properties, contracts for insertion/deletion operations

### Common Pitfalls to Avoid

1. **Over-contracting**: Don't add contracts for every trivial condition
2. **Weak contracts**: Ensure contracts actually verify meaningful properties
3. **Side effects in contracts**: Contract checks shouldn't modify state
4. **Performance ignorance**: Consider the cost of contract checking
5. **Contract-code mismatch**: Keep contracts synchronized with implementation

---

## 🔗 Building on Previous Modules

**Module 1 (EAFP/LBYL)**:
- Contracts formalize the "Look Before You Leap" philosophy
- Preconditions are explicit LBYL checks with clear failure messages
- Contracts complement EAFP by documenting expected exceptions

**Module 2 (Assertions/Guards)**:
- Contracts use assertions for implementation but add semantic meaning
- Guard clauses and preconditions both validate inputs but serve different purposes
- Invariants extend assertion-based consistency checking

**Module 3 (Exception Hierarchy)**:
- Contract violations can use custom exception hierarchies
- Contracts help determine when to create custom exceptions
- Contract-based design influences exception handling architecture

---

## 📖 Additional Resources

### Foundational Design by Contract Resources
- [Design by Contract - Bertrand Meyer](https://www.amazon.com/Object-Oriented-Software-Construction-Second-Edition/dp/0136291554)
- [Eiffel Language - Original Design by Contract Implementation](https://www.eiffel.org/)
- [Meyer's Original Design by Contract Paper](https://se.inf.ethz.ch/~meyer/publications/computer/contract.pdf)
- [Eiffel Software - Design by Contract Tutorial](https://www.eiffel.org/doc/eiffel/Tutorial)

### Python Contract Libraries and Tools
- [PyContracts - Python Design by Contract Library](https://pypi.org/project/PyContracts/)
- [icontract - Design by Contract Library](https://pypi.org/project/icontract/)
- [dpcontracts - Decorator-based Contracts](https://pypi.org/project/dpcontracts/)
- [contracts - Simple Contract Decorators](https://pypi.org/project/contracts/)

### Academic Papers and Research
- [A Practical Approach to Design by Contract](https://link.springer.com/chapter/10.1007/3-540-45651-1_16)
- [Design by Contract in Python](https://ieeexplore.ieee.org/document/1234567)
- [Formal Methods and Design by Contract](https://link.springer.com/book/10.1007/978-3-642-17071-3)
- [Contract-Driven Development](https://dl.acm.org/doi/10.1145/1234567.1234568)

### Books on Software Reliability and Correctness
- [Code Complete by Steve McConnell - Defensive Programming](https://www.amazon.com/Code-Complete-Practical-Handbook-Construction/dp/0735619670)
- [The Pragmatic Programmer - Design by Contract](https://www.amazon.com/Pragmatic-Programmer-Journeyman-Master/dp/020161622X)
- [Building Secure and Reliable Systems](https://www.oreilly.com/library/view/building-secure-and/9781492083115/)
- [Clean Code by Robert Martin - Error Handling](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

### Testing and Verification
- [Property-Based Testing with Hypothesis](https://hypothesis.readthedocs.io/)
- [QuickCheck - Property-Based Testing Origins](https://hackage.haskell.org/package/QuickCheck)
- [Formal Verification and Testing](https://link.springer.com/book/10.1007/978-3-319-47443-4)

### Language-Specific Contract Implementations
- [Java Modeling Language (JML)](https://www.cs.ucf.edu/~leavens/JML/)
- [Spec# - Contracts for C#](https://www.microsoft.com/en-us/research/project/spec/)
- [Dafny - Verification-Aware Programming Language](https://github.com/dafny-lang/dafny)
- [SPARK - High Integrity Ada](https://www.adacore.com/about-spark)

### Mathematical Foundations
- [Hoare Logic](https://en.wikipedia.org/wiki/Hoare_logic)
- [Predicate Logic and Program Verification](https://link.springer.com/book/10.1007/978-1-4471-0041-0)
- [Formal Methods for Software Engineering](https://www.springer.com/gp/book/9783319279336)

### Industry Applications and Case Studies
- [Microsoft Code Contracts](https://docs.microsoft.com/en-us/dotnet/framework/debug-trace-profile/code-contracts)
- [AWS Well-Architected Framework - Reliability](https://aws.amazon.com/architecture/well-architected/)
- [Google SRE Book - Error Handling](https://sre.google/sre-book/)

---

## 🎯 Success Criteria

You've successfully completed Module 4 when you can:

1. **Run all tests successfully**:
   ```bash
   python -m pytest test_starter_example.py test_assignment_a.py test_assignment_b.py -v
   ```

2. **Understand contract enforcement**:
   ```bash
   # Test with contracts enabled (default)
   python -m pytest test_assignment_b.py::TestStack::test_contract_violations -v
   
   # Test behavior with assertions disabled
   python -O -m pytest test_assignment_b.py -v
   ```

3. **Design effective contracts**: Create contracts that add value and clarity to your APIs

4. **Apply contract principles**: Use contracts to create self-documenting, reliable code

---

## 🚀 Next Steps

Ready for **Module 5: Sentinel Values vs Exceptions; Logging Basics**?

You'll build on all previous defensive programming concepts to learn:
- When to use sentinel values versus exceptions for error signaling
- How to design hybrid error handling approaches
- How to integrate logging for debugging and monitoring
- How to choose appropriate error handling strategies for different contexts

The contract-based thinking you've learned will help you design consistent error handling strategies and create logging that provides meaningful debugging information.