# Module 2: Advanced OOP Concepts: Inheritance and Polymorphism - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand the principles of OOP in Python
- Implement classes and objects
- Use inheritance and polymorphism
- Apply encapsulation and abstraction
- Design a simple OOP-based application

---

## 📚 Step 1: Understanding the Concepts

### Advanced OOP Concepts: Inheritance and Polymorphism Fundamentals

This module explores advanced OOP concepts in Python, focusing on inheritance, polymorphism, and encapsulation/abstraction. These principles enhance code organization and reusability.

### Inheritance

**Philosophy**: Inheritance allows a class to inherit attributes and methods from another class, promoting code reuse.

```python
class Animal:
    def speak(self):
        return 'Animal sound'

class Dog(Animal):
    def speak(self):
        return 'Bark'
```

**When to use inheritance**:
- Creating a hierarchy of classes
- Extending functionalities of existing classes
- Implementing shared behavior across multiple classes

**Advantages**:
- Reduces code duplication
- Enhances code maintainability
- Facilitates polymorphism

### Polymorphism

**Philosophy**: Polymorphism allows methods to do different things based on the object it is acting upon, enabling a single interface for different data types.

```python
class Cat(Animal):
    def speak(self):
        return 'Meow'

def animal_sound(animal):
    print(animal.speak())
```

**When to use polymorphism**:
- Implementing different behaviors for the same method
- Designing flexible interfaces
- Enhancing code scalability

**Advantages**:
- Promotes code flexibility
- Encourages interface consistency
- Supports dynamic method binding

### Encapsulation abstraction

**Philosophy**: Encapsulation restricts access to certain components of an object, while abstraction simplifies complex systems by exposing only necessary parts.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance
    def deposit(self, amount):
        self.__balance += amount
    def get_balance(self):
        return self.__balance
```

**When to use encapsulation_abstraction**:
- Protecting sensitive data
- Simplifying user interactions with complex systems
- Controlling access to class attributes and methods

**Advantages**:
- Enhances data security
- Improves code readability
- Facilitates maintenance and updates


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Animal Sound Simulation

A simulation that demonstrates inheritance and polymorphism through different animal sounds.

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return 'Bark'

class Cat(Animal):
    def speak(self):
        return 'Meow'

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())
```

**Key Points**:
- Demonstrates polymorphism via a common interface
- Shows inheritance by deriving Dog and Cat from Animal
- Outputs different results based on object type

#### Bank Account Management

An example showcasing encapsulation and abstraction in a banking system.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance
    def deposit(self, amount):
        self.__balance += amount
    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
print(account.get_balance())
```

**Key Points**:
- Encapsulates balance with private access
- Allows controlled access through public methods
- Demonstrates abstraction by hiding internal details


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 2 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Moderate
- **Estimated Time**: 90 minutes
- **Focus**: inheritance, polymorphism, encapsulation_abstraction
- **File**: `assignment_a.py`

#### Assignment b
- **Difficulty**: Moderate
- **Estimated Time**: 120 minutes
- **Focus**: inheritance, polymorphism, encapsulation_abstraction
- **File**: `assignment_b.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Test inheritance behavior for derived classes
- Verify polymorphic behavior with different object types
- Evaluate encapsulation by attempting to access private attributes

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Multiple Inheritance

Inheriting from multiple classes to combine behaviors and attributes.

```python
class A:
    def method_a(self):
        return 'Method A'

class B:
    def method_b(self):
        return 'Method B'

class C(A, B):
    pass

obj = C()
print(obj.method_a(), obj.method_b())
```

#### Abstract Base Classes (ABCs)

Defining abstract methods that must be implemented by derived classes.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2
```


## 📖 Additional Resources

### Documentation Links
- [<built-in method title of str object at 0x7532a4216430>]()
- [<built-in method title of str object at 0x7532a4205df0>]()

### Further Reading
- https://www.geeksforgeeks.org/python-oops-concept/
- https://www.tutorialsteacher.com/python/python_oops_concepts.asp

### Practice Exercises

Complete the following exercises in order:

1. **Assignment a**: Start with `assignment_a.py`
2. **Assignment b**: Continue with `assignment_b.py`
3. **Write comprehensive tests**: Create test files with 100% coverage
4. **Review and refactor**: Apply best practices and clean code principles

## 🏁 Completion Checklist

- [ ] Understand the core concepts of Advanced OOP Concepts: Inheritance and Polymorphism
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