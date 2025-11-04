```markdown
# Extra Exercises - Module 2: Advanced OOP Concepts in Python

## Exercise 1: Inheritance Basics
**Goal:** Create a base class `Animal` with a method `speak()` and derive a class `Dog` that overrides this method.

**Hints:**
- Use the `class` keyword to define the base class and the derived class.
- Override the `speak()` method in the `Dog` class to return "Woof!".

**Stretch Idea:** Add another derived class `Cat` that returns "Meow!" in its `speak()` method.

---

## Exercise 2: Method Overriding
**Goal:** Extend the `Animal` class from Exercise 1 to include an attribute `name` and modify the `speak()` method to include the name.

**Hints:**
- Use the `__init__` method to initialize the `name` attribute.
- In the `speak()` method, return a string that combines the name and the sound.

**Stretch Idea:** Implement a `get_info()` method in `Animal` that returns the name and the sound.

---

## Exercise 3: Encapsulation
**Goal:** Create a class `BankAccount` with private attributes for `balance` and methods to deposit and withdraw money.

**Hints:**
- Use the underscore `_` prefix to indicate private attributes.
- Ensure the `withdraw` method checks for sufficient funds before allowing a withdrawal.

**Stretch Idea:** Implement a method `get_balance()` that returns the current balance.

---

## Exercise 4: Polymorphism in Action
**Goal:** Define a function `animal_sound(animal)` that accepts any object of type `Animal` and calls its `speak()` method.

**Hints:**
- Ensure `animal` can be of type `Dog` or `Cat`.
- Use the `isinstance()` function to check the type if needed.

**Stretch Idea:** Modify the function to handle a list of `Animal` objects and print the sounds for each.

---

## Exercise 5: Multiple Inheritance
**Goal:** Create two base classes `Vehicle` and `Machine`, and derive a class `Car` that inherits from both.

**Hints:**
- Implement a method `describe()` in both base classes.
- Override the `describe()` method in `Car` to combine descriptions from both base classes.

**Stretch Idea:** Add a method `start_engine()` in `Car` that indicates the car is starting.

---

## Exercise 6: Abstract Base Classes
**Goal:** Define an abstract class `Shape` with an abstract method `area()`, and create classes `Circle` and `Rectangle` that implement this method.

**Hints:**
- Use the `abc` module to create an abstract base class.
- Implement the `area()` method in derived classes using appropriate formulas.

**Stretch Idea:** Add a method `perimeter()` to each shape class and implement it accordingly.

---

## Exercise 7: Composition
**Goal:** Create a class `Person` that has a `Car` object as an attribute. Implement a method `drive()` in `Person` that calls a method from `Car`.

**Hints:**
- Define a `Car` class with a method `start()`.
- In `Person`, initialize the `Car` object and call its `start()` method in `drive()`.

**Stretch Idea:** Allow `Person` to have multiple `Car` objects and implement a method to drive all cars.

---

## Exercise 8: Decorators for Method Access Control
**Goal:** Create a class `User` with a method `login()` that can only be accessed by a specific role using a custom decorator.

**Hints:**
- Define a decorator that checks the role before allowing access to `login()`.
- Use a class attribute to store the role of the user.

**Stretch Idea:** Implement a `logout()` method that can be accessed by any role and logs the user out.

```
