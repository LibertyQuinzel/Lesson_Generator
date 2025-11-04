# Module 1: Introduction to OOP in Python - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand the principles of OOP in Python
- Implement classes and objects
- Use inheritance and polymorphism
- Apply encapsulation and abstraction
- Design a simple OOP-based application

---

## 📚 Step 1: Understanding the Concepts

### Introduction to OOP in Python Fundamentals

Object-Oriented Programming (OOP) is a programming paradigm that uses objects and classes to structure software. Python supports OOP principles, enabling code reusability and modularity.

### Classes and objects

**Philosophy**: Classes define blueprints for objects. Objects are instances of classes, encapsulating data and behavior.

```python
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return f'{self.name} says woof!'

my_dog = Dog('Buddy')
print(my_dog.bark())
```

**When to use classes_and_objects**:
- Modeling real-world entities.
- Creating reusable code components.
- Building complex systems with ease.

**Advantages**:
- Encapsulation of data.
- Inheritance for code reuse.
- Polymorphism for flexibility.

### Basic principles

**Philosophy**: The four basic principles of OOP are encapsulation, abstraction, inheritance, and polymorphism. They enhance code organization and maintainability.

```python
class Animal:
    def speak(self):
        raise NotImplementedError

class Cat(Animal):
    def speak(self):
        return 'Meow'

class Dog(Animal):
    def speak(self):
        return 'Woof'
```

**When to use basic_principles**:
- Creating frameworks and libraries.
- Developing games and simulations.
- Implementing data-driven applications.

**Advantages**:
- Improved data security.
- Reduced code duplication.
- Easier troubleshooting and debugging.


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Creating a Simple Banking System

Demonstrates classes and object interactions in a banking context.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            return 'Insufficient funds'

account = Account('Alice', 100)
account.deposit(50)
print(account.balance)
account.withdraw(30)
print(account.balance)
```

**Key Points**:
- Encapsulates account properties and methods.
- Demonstrates interaction between methods.
- Shows error handling for insufficient funds.


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 1 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Simple
- **Estimated Time**: 60 minutes
- **Focus**: classes_and_objects, basic_principles
- **File**: `assignment_a.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Unit testing for class methods.
- Integration testing for object interactions.
- Performance testing for large-scale applications.

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Inheritance and Method Overriding

Inheritance allows a new class to inherit attributes and methods from an existing class. Method overriding enables specific implementations in derived classes.

```python
class Vehicle:
    def start(self):
        return 'Vehicle starting'

class Car(Vehicle):
    def start(self):
        return 'Car starting with key'

my_car = Car()
print(my_car.start())
```

#### Duck Typing

Duck typing is a concept where the type or class of an object is less important than the methods it defines. It emphasizes behavior over explicit type.

```python
def make_it_speak(animal):
    print(animal.speak())

class Duck:
    def speak(self):
        return 'Quack'

make_it_speak(Duck())
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