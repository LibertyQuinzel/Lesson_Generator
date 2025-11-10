```markdown
# Extra Exercises - Module 2: Advanced OOP Concepts: Inheritance and Polymorphism

## Challenge 1: Basic Inheritance
**Goal:** Create a base class `Animal` with a method `speak()` that returns a generic sound. Derive a class `Dog` that overrides `speak()` to return "Woof!"  
**Hints:**  
- Use the `class` keyword to define classes.  
- Use `super()` to call the base class method if needed.  

## Challenge 2: Multiple Inheritance  
**Goal:** Define two classes, `Vehicle` and `Electric`, and create a class `ElectricCar` that inherits from both. Implement a method to display the type of vehicle.  
**Hints:**  
- Remember to use commas for multiple inheritance in the class definition.  

## Challenge 3: Method Overriding  
**Goal:** Extend the `Dog` class to add a new method `fetch()`. Implement it so that it returns "Fetching the ball!"  
**Hints:**  
- Ensure you are still overriding the `speak()` method correctly.  

## Challenge 4: Polymorphism  
**Goal:** Create a function `animal_sound(animal)` that takes an `Animal` object and prints the sound it makes. Test it with `Dog` and another class `Cat` that inherits from `Animal`.  
**Hints:**  
- Use dynamic typing in Python to achieve polymorphism.  
- Implement `speak()` in the `Cat` class to return "Meow!".  

## Challenge 5: Abstract Base Class  
**Goal:** Create an abstract base class `Shape` with an abstract method `area()`. Derive classes `Circle` and `Square`, implementing `area()` for each.  
**Hints:**  
- Use the `abc` module to define the abstract base class.  

## Challenge 6: Class Relationships  
**Goal:** Define a class `Library` that holds a collection of `Book` objects. Implement methods to add books and list all titles.  
**Hints:**  
- Use a list to store the `Book` objects in the `Library`.  

## Challenge 7: Composition vs. Inheritance  
**Goal:** Create a class `Person` that has a `Car` as an attribute instead of inheriting from it. Implement methods to display the person's name and their car details.  
**Hints:**  
- Focus on composition, which means using instances of one class within another.  

## Stretch Idea: Advanced Polymorphism  
**Goal:** Implement a system where you can add any shape (circle, square, triangle) to a list and calculate the total area of all shapes.  
**Hints:**  
- Use polymorphism to call `area()` on each shape in the list.  
- Consider using a `Triangle` class as an additional shape.  
```
