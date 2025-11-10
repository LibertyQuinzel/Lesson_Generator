# Module 2: Advanced OOP Concepts: Inheritance and Polymorphism - Complete Learning Path

## 🎯 Learning Objectives

By the end of this module, you will understand:
- Understand core OOP principles in Python
- Implement classes and objects
- Utilize inheritance and polymorphism
- Apply encapsulation and abstraction
- Create and manage class methods and attributes

---

## 📚 Step 1: Understanding the Concepts

### Advanced OOP Concepts: Inheritance and Polymorphism Fundamentals

This module covers advanced OOP concepts in Python, focusing on inheritance and polymorphism. These concepts enhance code reusability and flexibility.

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

**When to use Inheritance**:
- Creating a class hierarchy
- Extending functionality of existing classes
- Implementing shared behavior among classes

**Advantages**:
- Encourages code reuse
- Simplifies code maintenance
- Facilitates polymorphism

### Polymorphism

**Philosophy**: Polymorphism enables objects of different classes to be treated as objects of a common superclass, allowing for dynamic method resolution.

```python
class Cat(Animal):
    def speak(self):
        return 'Meow'

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())
```

**When to use Polymorphism**:
- Implementing interchangeable class behavior
- Simplifying code with interfaces
- Enhancing system flexibility

**Advantages**:
- Reduces code complexity
- Increases flexibility and scalability
- Promotes code interoperability


## 🔧 Step 2: Hands-On Implementation

### Practical Examples

#### Vehicle Inheritance

Demonstrates inheritance with vehicle types.

```python
class Vehicle:
    def wheels(self):
        return 0

class Car(Vehicle):
    def wheels(self):
        return 4

class Bike(Vehicle):
    def wheels(self):
        return 2

vehicles = [Car(), Bike()]
for v in vehicles:
    print(v.wheels())
```

**Key Points**:
- Base class Vehicle defines a method.
- Car and Bike classes override the method.
- Demonstrates dynamic method resolution.

#### Shape Polymorphism

Illustrates polymorphism in geometric shapes.

```python
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def area(self, radius):
        return 3.14 * radius ** 2

class Square(Shape):
    def area(self, side):
        return side ** 2

shapes = [Circle(), Square()]
for shape in shapes:
    print(shape.area(5))
```

**Key Points**:
- Shape class serves as an interface.
- Circle and Square implement area calculation.
- Promotes flexibility with different shapes.


## 📝 Step 3: Assignment Tasks

### Assignment Overview
This module includes 2 assignment(s) to practice the concepts:

#### Assignment a
- **Difficulty**: Moderate
- Estimated Time: 90 minutes
- **Focus**: Inheritance, Polymorphism
- **File**: `assignment_a.py`

#### Assignment b
- **Difficulty**: Moderate
- Estimated Time: 120 minutes
- **Focus**: Inheritance, Polymorphism
- **File**: `assignment_b.py`


## 🧪 Step 4: Testing Your Understanding

### What You'll Test
- Test method overriding in inherited classes.
- Validate polymorphic behavior with different objects.
- Check for proper encapsulation and access control.

### Testing Strategy
- Write comprehensive unit tests for your implementations
- Aim for 100% code coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions

## 🎓 Step 5: Advanced Concepts

### Going Further

#### Multiple Inheritance

Implementing a class that inherits from multiple classes.

```python
class A:
    pass

class B:
    pass

class C(A, B):
    pass
```

#### Abstract Base Classes (ABC)

Creating abstract classes to define interfaces that must be implemented by subclasses.

```python
from abc import ABC, abstractmethod

class AbstractShape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(AbstractShape):
    def area(self, width, height):
        return width * height
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