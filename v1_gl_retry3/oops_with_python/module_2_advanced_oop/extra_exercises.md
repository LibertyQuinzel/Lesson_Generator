```markdown
# Extra Exercises - Module 2: Advanced OOP Concepts

## Challenge 1: Basic Inheritance
**Goal:** Create a base class `Animal` with a method `speak()` and a derived class `Dog` that overrides `speak()`.  
**Hints:**  
- Use the `class` keyword to define `Animal` and `Dog`.  
- The `speak()` method in `Dog` should return "Woof!".  

**Stretch Idea:** Add another derived class `Cat` that returns "Meow!" in its `speak()` method.

---

## Challenge 2: Method Overriding
**Goal:** Extend the previous challenge by adding a method `info()` in the `Animal` class that returns the type of animal. Override this method in the `Dog` class.  
**Hints:**  
- Use the `super()` function to call the base class method in the override.  
- Ensure the `info()` method in `Dog` specifies it is a dog.  

**Stretch Idea:** Add a `Bird` class that also overrides `info()`.

---

## Challenge 3: Encapsulation
**Goal:** Implement a class `BankAccount` with private attributes for balance and a public method to deposit money.  
**Hints:**  
- Use double underscores (`__`) for private attributes.  
- Create a method `deposit(amount)` that increases the balance.  

**Stretch Idea:** Add a method to check the balance, ensuring it is also encapsulated.

---

## Challenge 4: Polymorphism
**Goal:** Create a function `make_animal_speak(animal)` that accepts an `Animal` object and calls its `speak()` method.  
**Hints:**  
- Ensure your function works with any derived class of `Animal`.  
- Test with instances of `Dog` and `Cat` (if created).  

**Stretch Idea:** Add a `Parrot` class that can also be passed to `make_animal_speak()`.

---

## Challenge 5: Abstract Base Class
**Goal:** Define an abstract base class `Shape` with an abstract method `area()`. Create derived classes `Circle` and `Rectangle`.  
**Hints:**  
- Use the `abc` module to define the abstract class.  
- Implement `area()` in both derived classes.  

**Stretch Idea:** Add a method `perimeter()` in both derived classes.

---

## Challenge 6: Multiple Inheritance
**Goal:** Create classes `Person` and `Employee`. The `Employee` class should inherit from `Person` and add an attribute for job title.  
**Hints:**  
- Use the `__init__` method to initialize both `Person` and `Employee` attributes.  
- Make sure to call the parent class constructor.  

**Stretch Idea:** Implement a method in `Employee` that displays both the person's name and job title.

---

## Challenge 7: Composition vs Inheritance
**Goal:** Create a class `Car` that uses a class `Engine` through composition instead of inheritance.  
**Hints:**  
- The `Car` class should have an `Engine` object as an attribute.  
- Implement a method in `Car` that utilizes the `Engine` to start the car.  

**Stretch Idea:** Add methods to both classes demonstrating their interaction (e.g., `Engine` status).

---

## Challenge 8: Real-World OOP Design
**Goal:** Design a simple library system with classes `Book`, `Member`, and `Library`. Implement methods for borrowing and returning books.  
**Hints:**  
- `Library` should manage a collection of `Book` objects.  
- `Member` should be able to borrow and return books, updating the library's collection accordingly.  

**Stretch Idea:** Implement a method to check the availability of books before borrowing.
```