```markdown
# Extra Exercises - Module 2: Advanced OOP Concepts: Inheritance and Polymorphism

## Challenge 1: Basic Inheritance
**Goal:** Create a base class `Animal` with a method `speak()`. Derive a class `Dog` that overrides `speak()`.

**Hints:** 
- Use the `__init__` method to initialize the name of the animal.
- Override the `speak()` method in the `Dog` class to return "Woof!".

**Stretch Idea:** Add more animal classes (e.g., `Cat`, `Bird`) with their own `speak()` implementations.

---

## Challenge 2: Method Overriding
**Goal:** Create a base class `Shape` with a method `area()`. Derive classes `Rectangle` and `Circle` that implement `area()`.

**Hints:**
- Use the formula for area: Rectangle (width * height), Circle (π * radius²).
- Consider using `math.pi` for π.

**Stretch Idea:** Implement a `total_area()` function that calculates the sum of areas for a list of shapes.

---

## Challenge 3: Polymorphism in Action
**Goal:** Write a function `print_area(shape)` that takes any object of type `Shape` and prints its area.

**Hints:**
- Ensure `print_area()` calls the `area()` method on the passed shape object.
- Use a list of different shape objects to demonstrate polymorphism.

**Stretch Idea:** Modify `print_area()` to also handle shapes that do not have an `area()` method gracefully.

---

## Challenge 4: Encapsulation
**Goal:** Create a class `BankAccount` with private attributes for `balance` and `account_number`. Implement methods to deposit and withdraw.

**Hints:**
- Use getter methods to retrieve the balance.
- Ensure withdrawals cannot exceed the balance.

**Stretch Idea:** Implement a method to transfer funds between two accounts.

---

## Challenge 5: Abstract Classes
**Goal:** Define an abstract class `Vehicle` with an abstract method `drive()`. Derive classes `Car` and `Bike` that implement `drive()`.

**Hints:**
- Use the `abc` module to create an abstract base class.
- Ensure each derived class provides its own implementation of `drive()`.

**Stretch Idea:** Add additional methods like `stop()` and override them in derived classes.

---

## Challenge 6: Multiple Inheritance
**Goal:** Create classes `Person` and `Employee`. Derive a class `Manager` from both.

**Hints:**
- Ensure `Manager` can access attributes and methods from both `Person` and `Employee`.
- Implement a method `manage()` in `Manager`.

**Stretch Idea:** Handle potential method resolution order (MRO) issues by adding a method to demonstrate which class method is called.

---

## Challenge 7: Composition vs Inheritance
**Goal:** Create a class `Engine` and a class `Car` that uses `Engine` as a component.

**Hints:**
- Define methods in `Engine` that provide functionality (e.g., `start()`).
- Use composition to include an `Engine` instance in `Car`.

**Stretch Idea:** Implement a `Car` method that starts the engine and outputs a message.

---

## Challenge 8: Real-World Application
**Goal:** Model a simple library system with classes `Book`, `Member`, and `Library`. Implement methods for borrowing and returning books.

**Hints:**
- Use inheritance to create specialized book types (e.g., `Ebook`, `PrintedBook`).
- Maintain a list of borrowed books in the `Library` class.

**Stretch Idea:** Implement a method to check if a book is available before borrowing.
```