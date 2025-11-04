```markdown
# Extra Exercises - Module 1: Introduction to OOP in Python

## Challenge 1: Create a Simple Class
**Goal:** Define a class named `Dog` with attributes `name` and `age`.  
**Hints:** Use the `__init__` method to initialize attributes.  

## Challenge 2: Add a Method
**Goal:** Add a method `bark` to the `Dog` class that prints "Woof!" when called.  
**Hints:** Define the method within the class and use `self` to access instance variables.  

## Challenge 3: Instantiate Objects
**Goal:** Create two instances of the `Dog` class with different names and ages.  
**Hints:** Use the class constructor to create objects and store them in variables.  

## Challenge 4: Class Method for Age
**Goal:** Add a method `get_age` to the `Dog` class that returns the dog's age.  
**Hints:** Use `return self.age` in the method.  

## Challenge 5: Inheritance Basics
**Goal:** Create a subclass `Puppy` that inherits from `Dog` and adds an attribute `breed`.  
**Hints:** Use parentheses to indicate inheritance in the class definition.  

## Challenge 6: Override Method
**Goal:** Override the `bark` method in the `Puppy` class to print "Yip!" instead of "Woof!".  
**Hints:** Use the `def bark(self):` method in the subclass to override the parent class method.  

## Challenge 7: Class Variable
**Goal:** Add a class variable `species` to the `Dog` class that is shared among all instances.  
**Hints:** Define it outside the `__init__` method. Access it with `self.species` within methods.  

## Stretch Challenge: Class Method
**Goal:** Create a class method `create_puppy` in the `Dog` class that returns a `Puppy` instance with a default name and age.  
**Hints:** Use `@classmethod` decorator and `cls` to refer to the class itself.  
```
