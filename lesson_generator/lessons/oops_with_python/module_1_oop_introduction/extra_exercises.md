```markdown
# Extra Exercises - Module 1: Introduction to OOP in Python

## Exercise 1: Basic Class Definition
**Goal:** Create a simple class called `Dog` with attributes `name` and `age`.  
**Hints:**  
- Use the `__init__` method to initialize attributes.  
- Create an instance of the class and print its attributes.  
**Stretch Idea:** Add a method to bark that prints the dog's name.

---

## Exercise 2: Method Implementation
**Goal:** Add a method `get_info` to the `Dog` class that returns a string with the dog's name and age.  
**Hints:**  
- Use `self` to access instance variables.  
- Return a formatted string.  
**Stretch Idea:** Modify the method to include the dog's breed.

---

## Exercise 3: Encapsulation
**Goal:** Implement encapsulation in the `Dog` class by making the `age` attribute private.  
**Hints:**  
- Prefix the attribute with a double underscore (`__`).  
- Provide a public method to get the age.  
**Stretch Idea:** Add a method to set the age, ensuring it cannot be negative.

---

## Exercise 4: Class Inheritance
**Goal:** Create a subclass `Puppy` that inherits from `Dog` and has an additional attribute `training_level`.  
**Hints:**  
- Use the `super()` function to initialize the parent class.  
- Add a method to display the training level.  
**Stretch Idea:** Override the `get_info` method to include training level.

---

## Exercise 5: Abstraction with Abstract Base Class
**Goal:** Create an abstract base class `Animal` with an abstract method `sound`.  
**Hints:**  
- Use the `abc` module to define the abstract class.  
- Implement the `sound` method in the `Dog` class.  
**Stretch Idea:** Create another subclass `Cat` that also implements the `sound` method.

---

## Exercise 6: Composition
**Goal:** Create a class `Owner` that has a `Dog` as an attribute.  
**Hints:**  
- Initialize the `Dog` object within the `Owner` class.  
- Provide a method to display both owner and dog's information.  
**Stretch Idea:** Allow the `Owner` class to manage multiple dogs.

---

## Exercise 7: Polymorphism
**Goal:** Create a list of different animal objects and call their `sound` methods.  
**Hints:**  
- Define at least two classes that inherit from `Animal`.  
- Store instances in a list and iterate through it.  
**Stretch Idea:** Add a method to each class that returns the type of animal.

---

## Exercise 8: Custom Exception Handling
**Goal:** Implement a custom exception `AgeError` in the `Dog` class for invalid ages.  
**Hints:**  
- Define the exception class.  
- Raise the exception in the setter method for age.  
**Stretch Idea:** Write a test case that demonstrates the exception being raised.
```