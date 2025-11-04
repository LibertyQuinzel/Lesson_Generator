# Module 1: Introduction to OOP in Python - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand the principles of OOP in Python
- Implement classes and objects effectively
- Utilize inheritance and polymorphism
- Apply encapsulation in Python code
- Design simple OOP-based applications

---

## 📚 Step 1: Understanding the Concepts

### Introduction to OOP in Python Fundamentals

Object-Oriented Programming (OOP) in Python allows for organizing code into reusable structures called classes and objects. It enhances code modularity and readability.

### Classes and objects

**Philosophy**: Classes are blueprints for creating objects. Objects are instances of classes that encapsulate data and functionality.

```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return 'Woof!'
```

**When to use classes_and_objects**:
- Modeling real-world entities
- Creating reusable code components
- Implementing complex data structures

**Advantages**:
- Improved code organization
- Enhanced code reuse
- Easier maintenance

### Encapsulation

**Philosophy**: Encapsulation restricts access to certain components of an object, protecting the integrity of the data and providing a controlled interface.

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance
    def deposit(self, amount):
        self.__balance += amount
    def get_balance(self):
        return self.__balance
```

**When to use encapsulation**:
- Protecting sensitive data
- Controlling access to class properties
- Simplifying complex interfaces

**Advantages**:
- Increased security
- Reduced complexity
- Improved code maintainability


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Basic Class and Object Creation

Demonstrating how to define a class and create an object.

```python
class Car:
    def __init__(self, model):
        self.model = model

my_car = Car('Toyota')
print(my_car.model)
```

**Key Points**:
- Define a class with the 'class' keyword.
- Use '__init__' for initialization.
- Create objects by calling the class.

#### Using Encapsulation in Classes

Implementing private attributes in a class.

```python
class User:
    def __init__(self, username):
        self.__username = username
    def get_username(self):
        return self.__username

user = User('alice')
print(user.get_username())
```

**Key Points**:
- Use double underscores for private attributes.
- Provide public methods to access private data.
- Enhances data security.


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 1 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Simple
- **Estimated Time**: 90 minutes
- **Focus**: classes_and_objects, encapsulation
- **File**: `assignment_a.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Creating and using classes
- Implementing encapsulation
- Testing class methods

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Inheritance

Inheritance allows a class to inherit attributes and methods from another class, promoting code reuse.

```python
class Animal:
    def speak(self):
        return 'Animal sound'

class Dog(Animal):
    def speak(self):
        return 'Woof!'

dog = Dog()
print(dog.speak())
```

#### Polymorphism

Polymorphism enables different classes to be treated as instances of the same class through a common interface.

```python
class Cat(Animal):
    def speak(self):
        return 'Meow!'

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())
```


## 📖 Additional Resources

### Documentation Links
- [<built-in method title of str object at 0x76a257c4a550>]()
- [<built-in method title of str object at 0x76a257c39df0>]()

### Further Reading
- https://www.geeksforgeeks.org/python-oops-concept/

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