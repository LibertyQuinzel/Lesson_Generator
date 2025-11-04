```markdown
# Extra Exercises - Module 1: Introduction to OOP in Python

## Challenge 1: Create a Simple Class (Easy)
**Goal:** Define a class `Dog` with attributes `name` and `age`, and a method to bark.  
**Hints:** 
- Use the `__init__` method to initialize attributes.
- Create a method `bark` that prints a barking sound.
  
**Stretch Idea:** Add a method to return a string representation of the dog.

---

## Challenge 2: Class Method and Static Method (Easy)
**Goal:** Implement a class `Circle` with a class method to calculate area from radius and a static method to check if a number is positive.  
**Hints:** 
- Use `@classmethod` for the area calculation.
- Use `@staticmethod` for the positivity check.
  
**Stretch Idea:** Add a method that returns the circumference of the circle.

---

## Challenge 3: Inheritance (Medium)
**Goal:** Create a class `Animal` and a subclass `Cat` that inherits from `Animal`. Add a method specific to `Cat`.  
**Hints:** 
- Define common attributes in `Animal`.
- Override or extend methods in `Cat`.
  
**Stretch Idea:** Implement polymorphism by defining a method in `Animal` and overriding it in `Cat`.

---

## Challenge 4: Encapsulation (Medium)
**Goal:** Create a class `BankAccount` with private attributes for balance and a method to deposit money.  
**Hints:** 
- Use an underscore `_` to indicate private attributes.
- Implement a method `deposit` that modifies the balance.
  
**Stretch Idea:** Add a method to check the balance without directly accessing the attribute.

---

## Challenge 5: Composition (Hard)
**Goal:** Create a class `Library` that contains a list of `Book` objects. Implement methods to add and list books.  
**Hints:** 
- Define a `Book` class with title and author attributes.
- Use a list in `Library` to manage `Book` instances.
  
**Stretch Idea:** Implement a method to search for a book by title.

---

## Challenge 6: Operator Overloading (Hard)
**Goal:** Implement a class `Vector` that overloads addition and string representation.  
**Hints:** 
- Use the `__add__` method for addition.
- Use `__str__` for string representation.
  
**Stretch Idea:** Overload other operators like subtraction or dot product.

---

## Challenge 7: Custom Exceptions (Hard)
**Goal:** Create a custom exception `InsufficientFunds` and use it in the `BankAccount` class.  
**Hints:** 
- Define a custom exception class.
- Raise the exception in the `withdraw` method if funds are insufficient.
  
**Stretch Idea:** Handle the exception in a separate function to showcase error handling.

---

## Challenge 8: Abstract Base Class (Hard)
**Goal:** Create an abstract base class `Shape` with an abstract method `area`, and implement subclasses `Rectangle` and `Triangle`.  
**Hints:** 
- Use the `abc` module to define the abstract class.
- Implement `area` in each subclass based on their formulas.
  
**Stretch Idea:** Add a method in `Shape` to return the type of shape.
```