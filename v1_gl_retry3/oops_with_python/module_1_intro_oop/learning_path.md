# Module 1: Introduction to OOP in Python - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand OOP principles in Python
- Implement classes and objects
- Utilize inheritance and polymorphism
- Apply encapsulation and abstraction
- Design a simple OOP-based application

---

## 📚 Step 1: Understanding the Concepts

### Introduction to OOP in Python Fundamentals

Object-Oriented Programming (OOP) in Python allows for structuring code using classes and objects, promoting modularity and reuse.

### Classes and objects

**Philosophy**: Classes are blueprints for creating objects, encapsulating data and behavior.

```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return 'Woof!'
```

**When to use classes_and_objects**:
- Modeling real-world entities
- Code organization and maintenance
- Creating reusable components

**Advantages**:
- Encapsulation of data
- Inheritance for code reuse
- Polymorphism for flexibility

### Basic principles

**Philosophy**: OOP principles include encapsulation, inheritance, and polymorphism.

```python
class Animal:
    def speak(self):
        raise NotImplementedError

class Cat(Animal):
    def speak(self):
        return 'Meow'
```

**When to use basic_principles**:
- Developing large applications
- Game development
- Data modeling

**Advantages**:
- Improved code organization
- Easier debugging and testing
- Enhanced collaboration


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Creating a Simple Class

Define a class representing a geometric shape.

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * (self.radius ** 2)
```

**Key Points**:
- Classes encapsulate properties and methods.
- Use __init__ for initialization.
- Methods define behavior.

#### Inheritance Example

Demonstrate inheritance with a base and derived class.

```python
class Vehicle:
    def start(self):
        return 'Vehicle starting'

class Car(Vehicle):
    def honk(self):
        return 'Honk!'

my_car = Car()
my_car.start()
```

**Key Points**:
- Derived classes inherit attributes and methods.
- Use 'super()' to access base class methods.
- Promotes code reuse.


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 1 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Simple
- **Estimated Time**: 90 minutes
- **Focus**: classes_and_objects, basic_principles
- **File**: `assignment_a.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Unit testing of classes
- Integration testing for class interactions
- Behavioral testing of methods

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Duck Typing

Concept where the type of an object is determined by its behavior rather than its explicit type.

```python
def make_sound(animal):
    print(animal.speak())  # Works with any object that has a speak method.
```

#### Abstract Classes

Define a blueprint for other classes using the abc module.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
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
3. **Write comprehensive tests**: Create test files with 100% coverage
4. **Review and refactor**: Apply best practices and clean code principles

## 🏁 Completion Checklist

- [ ] Understand the core concepts of Introduction to OOP in Python
- [ ] Complete starter example walkthrough
- [ ] Implement Assignment a
- [ ] Write tests for Assignment a
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