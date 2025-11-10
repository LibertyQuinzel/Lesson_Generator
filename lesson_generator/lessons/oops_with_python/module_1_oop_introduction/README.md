# Module 1: Introduction to OOP in Python - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand core OOP principles in Python
- Implement classes and objects
- Utilize inheritance and polymorphism
- Apply encapsulation and abstraction
- Create and manage class methods and attributes

---

## 📚 Step 1: Understanding the Concepts

### Introduction to OOP in Python Fundamentals

Object-Oriented Programming (OOP) is a programming paradigm that uses 'objects' to design applications. Python supports OOP principles, enabling code reusability and modularity.

### Classes And Objects

**Philosophy**: Classes define the blueprint for objects. Objects are instances of classes.

```python
class Dog:
    def bark(self):
        return 'Woof!'

my_dog = Dog()
print(my_dog.bark())
```

**When to use Classes and Objects**:
- Modeling real-world entities
- Creating reusable code components

**Advantages**:
- Encapsulation of data
- Improved code organization

### Encapsulation

**Philosophy**: Encapsulation restricts access to certain components, protecting the object's internal state.

```python
class BankAccount:
    def __init__(self, balance=0):
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

**When to use Encapsulation**:
- Data protection in applications
- Controlled access to object properties

**Advantages**:
- Prevents unintended interference
- Enhances security

### Abstraction

**Philosophy**: Abstraction simplifies complex systems by exposing only the necessary parts.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
```

**When to use Abstraction**:
- Creating interfaces for diverse implementations
- Reducing complexity in software design

**Advantages**:
- Focus on high-level functionality
- Improved code maintainability


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Creating a Simple Class

Define a class representing a car with attributes and methods.

```python
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def info(self):
        return f'{self.make} {self.model}'

my_car = Car('Toyota', 'Corolla')
print(my_car.info())
```

**Key Points**:
- Classes encapsulate data and behavior.
- Instances can have unique attributes.

#### Implementing Encapsulation

Create a class with private attributes and methods for interaction.

```python
class Temperature:
    def __init__(self, celsius):
        self.__celsius = celsius

    def to_fahrenheit(self):
        return (self.__celsius * 9/5) + 32

temp = Temperature(25)
print(temp.to_fahrenheit())
```

**Key Points**:
- Private attributes protect data.
- Public methods provide controlled access.


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 1 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Simple
- Estimated Time: 60 minutes
- **Focus**: Classes and Objects, Encapsulation, Abstraction
- **File**: `assignment_a.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Class instantiation
- Method functionality
- Encapsulation enforcement
- Abstraction implementation

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Inheritance

Inheritance allows a class to inherit attributes and methods from another class.

```python
class Animal:
    def speak(self):
        return 'Sound'

class Cat(Animal):
    def speak(self):
        return 'Meow'

my_cat = Cat()
print(my_cat.speak())
```

#### Polymorphism

Polymorphism allows methods to do different things based on the object calling them.

```python
class Bird:
    def fly(self):
        return 'Flies'

class Airplane:
    def fly(self):
        return 'Soars'

for obj in [Bird(), Airplane()]:
    print(obj.fly())
```


## 📖 Additional Resources

### Documentation Links
- [<built-in method title of str object at 0x7dcd48407330>]()
- [<built-in method title of str object at 0x7dcd483f6800>]()

### Further Reading
- https://www.geeksforgeeks.org/python-oops-concepts/
- https://www.learnpython.org/en/Classes_and_Objects

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