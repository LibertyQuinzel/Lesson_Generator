# Module 2: Advanced OOP Concepts - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand OOP principles in Python
- Implement classes and objects
- Utilize inheritance and polymorphism
- Apply encapsulation and abstraction
- Design a simple OOP-based application

---

## 📚 Step 1: Understanding the Concepts

### Advanced OOP Concepts Fundamentals

Advanced OOP concepts in Python enhance code organization and reusability. This module covers inheritance, polymorphism, and encapsulation.

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
- Creating hierarchical class structures
- Extending functionality of existing classes
- Implementing shared behaviors in subclasses

**Advantages**:
- Reduces code duplication
- Enhances code organization
- Facilitates easier maintenance

### Polymorphism

**Philosophy**: Polymorphism allows methods to do different things based on the object it is acting upon, enhancing flexibility.

```python
class Cat(Animal):
    def speak(self):
        return 'Meow'

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())
```

**When to use polymorphism**:
- Implementing different behaviors in subclasses
- Using interfaces in a consistent way across different objects
- Facilitating code that can work on different objects

**Advantages**:
- Increases code flexibility
- Supports generic programming
- Enhances readability and maintainability

### Encapsulation

**Philosophy**: Encapsulation restricts direct access to some of an object's components, promoting data protection.

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance
    def deposit(self, amount):
        self.__balance += amount
    def get_balance(self):
        return self.__balance
```

**When to use encapsulation**:
- Protecting sensitive data
- Controlling access to class attributes
- Implementing data hiding for security

**Advantages**:
- Improves data integrity
- Encourages modularity
- Reduces risk of unintended interference


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Vehicle Inheritance

Demonstrates vehicle hierarchy using inheritance.

```python
class Vehicle:
    def start_engine(self):
        return 'Engine started'

class Car(Vehicle):
    def start_engine(self):
        return 'Car engine started'

my_car = Car()
print(my_car.start_engine())
```

**Key Points**:
- Establishes a base class for shared functionality
- Allows subclass to override methods
- Promotes code reuse

#### Polymorphic Shapes

Illustrates polymorphism with different shape classes.

```python
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * (self.radius ** 2)

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

shapes = [Circle(5), Square(4)]
for shape in shapes:
    print(shape.area())
```

**Key Points**:
- Demonstrates method overriding
- Enhances code flexibility
- Allows use of a common interface


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 2 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Moderate
- **Estimated Time**: 120 minutes
- **Focus**: inheritance, polymorphism, encapsulation
- **File**: `assignment_a.py`

#### Assignment b
- **Difficulty**: Moderate
- **Estimated Time**: 150 minutes
- **Focus**: inheritance, polymorphism, encapsulation
- **File**: `assignment_b.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Unit tests for class methods
- Integration tests for subclasses
- Test cases for data encapsulation

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Multiple Inheritance

A class can inherit from multiple classes, combining their attributes and methods.

```python
class A:
    def method_a(self):
        return 'A'

class B:
    def method_b(self):
        return 'B'

class C(A, B):
    pass

obj = C()
print(obj.method_a(), obj.method_b())
```

#### Abstract Base Classes

Defines methods that must be implemented by subclasses, promoting interface design.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return 'Bark'
```


## 📖 Additional Resources

### Documentation Links
- [<built-in method title of str object at 0x71e92dbde430>]()
- [<built-in method title of str object at 0x71e92dbd1d10>]()

### Further Reading
- https://www.geeksforgeeks.org/python-oops-concepts/
- https://towardsdatascience.com/object-oriented-programming-in-python-7dd2f6f1a7d8

### Practice Exercises

Complete the following exercises in order:

1. **Assignment a**: Start with `assignment_a.py`
2. **Assignment b**: Continue with `assignment_b.py`
3. **Write comprehensive tests**: Create test files with 100% coverage
4. **Review and refactor**: Apply best practices and clean code principles

## 🏁 Completion Checklist

- [ ] Understand the core concepts of Advanced OOP Concepts
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