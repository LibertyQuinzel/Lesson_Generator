# Module 2: Applying Design Patterns - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand core design patterns in Python
- Implement common design patterns in code
- Identify appropriate design patterns for specific problems
- Evaluate the benefits and drawbacks of different patterns
- Apply design patterns in real-world scenarios

---

## 📚 Step 1: Understanding the Concepts

### Applying Design Patterns Fundamentals

This module explores the application of design patterns, focusing on behavioral patterns, design principles, and real-world use cases. Understanding these elements enhances software design and architecture.

### Behavioral patterns

**Philosophy**: Behavioral patterns focus on how objects interact and communicate to achieve specific behaviors.

```python
class Observer:
    def update(self, message):
        pass

class ConcreteObserver(Observer):
    def update(self, message):
        print(f'Observer received: {message}')
```

**When to use behavioral_patterns**:
- Event handling systems
- Notification systems
- Data streaming applications

**Advantages**:
- Decouples sender and receiver
- Facilitates dynamic communication
- Enhances code maintainability

### Design principles

**Philosophy**: Design principles guide the creation of software that is easy to maintain, understand, and extend.

```python
# Single Responsibility Principle
class Invoice:
    def calculate_total(self):
        pass

class InvoicePrinter:
    def print_invoice(self, invoice):
        pass
```

**When to use design_principles**:
- Modular application development
- Code reviews and refactoring
- Agile development practices

**Advantages**:
- Improves code clarity
- Reduces complexity
- Enhances testability

### Real world use cases

**Philosophy**: Real-world use cases illustrate the practical application of design patterns in solving common software challenges.

```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self):
        pass

class ConcreteStrategyA(Strategy):
    def execute(self):
        return 'Strategy A'

class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def do_action(self):
        return self._strategy.execute()
```

**When to use real_world_use_cases**:
- Payment processing systems
- Routing algorithms
- Game development

**Advantages**:
- Demonstrates practical solutions
- Enhances understanding of patterns
- Promotes best practices


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Observer Pattern

Implementing a notification system using the Observer pattern.

```python
class Subject:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
```

**Key Points**:
- Decouples components
- Supports dynamic subscriptions
- Promotes loose coupling

#### Strategy Pattern

Using the Strategy pattern to define a family of algorithms.

```python
class Addition:
    def compute(self, a, b):
        return a + b

class Subtraction:
    def compute(self, a, b):
        return a - b

class Calculator:
    def __init__(self, strategy):
        self._strategy = strategy

    def calculate(self, a, b):
        return self._strategy.compute(a, b)
```

**Key Points**:
- Encapsulates algorithms
- Allows dynamic switching of algorithms
- Enhances flexibility


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 2 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Complex
- Estimated Time: 120 minutes
- **Focus**: behavioral_patterns, design_principles, real_world_use_cases
- **File**: `assignment_a.py`

#### Assignment b
- **Difficulty**: Complex
- Estimated Time: 150 minutes
- **Focus**: behavioral_patterns, design_principles, real_world_use_cases
- **File**: `assignment_b.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Unit testing behavioral patterns
- Integration testing with design principles
- Performance testing of real-world applications

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Chain of Responsibility

A behavioral design pattern that allows passing requests along a chain of handlers.

```python
class Handler:
    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None
```

#### Command Pattern

Encapsulates a request as an object, thereby allowing for parameterization and queuing of requests.

```python
class Command:
    def execute(self):
        pass

class ConcreteCommand(Command):
    def execute(self):
        print('Command executed')
```


## 📖 Additional Resources

### Documentation Links
- [<built-in method title of str object at 0x750b724d7390>]()
- [<built-in method title of str object at 0x750b724d73f0>]()

### Further Reading
- Design Patterns: Elements of Reusable Object-Oriented Software by Gamma et al.
- Head First Design Patterns by Freeman & Freeman

### Practice Exercises

Complete the following exercises in order:

1. **Assignment a**: Start with `assignment_a.py`
2. **Assignment b**: Continue with `assignment_b.py`
3. **Write comprehensive tests**: Create test files with 100% coverage
4. **Review and refactor**: Apply best practices and clean code principles

## 🏁 Completion Checklist

- [ ] Understand the core concepts of Applying Design Patterns
- [ ] Complete starter example walkthrough
- [ ] Implement Assignment a
- [ ] Write tests for Assignment a
- [ ] Implement Assignment b
- [ ] Write tests for Assignment b
- [ ] Achieve 100% test coverage
- [ ] Code passes all quality checks (pylint, black)
- [ ] Review additional resources
- [ ] Ready to move to next module

---

## 💡 Tips for Success

1. **Start Small**: Begin with the starter example to understand the concepts
2. **Test Early**: Write tests as you develop your solutions  
3. **Experiment**: Try different approaches and see what works best
4. **Ask Questions**: Use the discussion forum if you get stuck
5. **Practice**: The more you code, the better you'll understand the concepts

Remember: The goal is not just to complete the assignments, but to deeply understand the underlying principles that will make you a better developer.