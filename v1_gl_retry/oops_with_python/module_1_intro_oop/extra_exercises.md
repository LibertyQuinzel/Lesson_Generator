```markdown
# Extra Exercises - Module 1: Introduction to OOP in Python

## Challenge 1: Create a Basic Class
**Goal:** Define a class named `Car` with attributes `make`, `model`, and `year`.  
**Hints:**  
- Use the `__init__` method to initialize attributes.  
- Create an instance of the class and print its attributes.

## Challenge 2: Add a Method to Class
**Goal:** Add a method `display_info` to the `Car` class that prints all car details.  
**Hints:**  
- Define the method within the class.  
- Use `self` to access instance attributes.  

## Challenge 3: Implement Encapsulation
**Goal:** Modify the `Car` class to use private attributes for `make` and `model`.  
**Hints:**  
- Prefix attribute names with a double underscore (`__`).  
- Create getter methods for these attributes.

## Challenge 4: Inheritance
**Goal:** Create a subclass `ElectricCar` that inherits from `Car`. Add an attribute `battery_size`.  
**Hints:**  
- Use the `super()` function to initialize the parent class.  
- Add a method to display battery size.

## Challenge 5: Method Overriding
**Goal:** Override the `display_info` method in `ElectricCar` to include battery information.  
**Hints:**  
- Use the `def` keyword to redefine the method in the subclass.  
- Call the parent class's method within the overridden method.

## Challenge 6: Class Attributes
**Goal:** Add a class attribute `num_wheels` to the `Car` class and set it to 4.  
**Hints:**  
- Define the attribute outside of any methods.  
- Access this attribute using the class name and instance.

## Challenge 7: Class Method for Instance Creation
**Goal:** Create a class method `from_string` in `Car` that initializes an instance from a string.  
**Hints:**  
- Use `@classmethod` decorator.  
- Split the string to extract `make`, `model`, and `year`.

## Stretch Idea: Implement a `Vehicle` Class
**Goal:** Create a base class `Vehicle` with methods `start` and `stop`, then have `Car` and `ElectricCar` inherit from it.  
**Hints:**  
- Define the base class with common attributes/methods.  
- Ensure both subclasses implement or override these methods.
```