```markdown
# Extra Exercises - Module 1: Introduction to Object-Oriented Programming

## Exercise 1: Define a Class (Easy)
**Goal:** Create a simple class called `Dog` with attributes `name` and `age`.  
**Hints:** Use the `__init__` method to initialize attributes.  
**Stretch Idea:** Add a method to return a string describing the dog.

---

## Exercise 2: Create Object Instances (Easy)
**Goal:** Instantiate two objects of the `Dog` class created in Exercise 1.  
**Hints:** Assign different names and ages to each instance.  
**Stretch Idea:** Print the attributes of each instance in a formatted string.

---

## Exercise 3: Class Method Creation (Medium)
**Goal:** Add a method to the `Dog` class called `bark` that returns the string "Woof!"  
**Hints:** Define the method within the class and use `self` to refer to the instance.  
**Stretch Idea:** Modify the `bark` method to include the dog's name in the output.

---

## Exercise 4: Inheritance (Medium)
**Goal:** Create a subclass called `Bulldog` that inherits from `Dog`.  
**Hints:** Use the class definition syntax to create a subclass.  
**Stretch Idea:** Override the `bark` method in the `Bulldog` class to return "Woof! Woof!".

---

## Exercise 5: Class Attributes (Hard)
**Goal:** Add a class attribute `species` to the `Dog` class with the value "Canine".  
**Hints:** Define the attribute outside of any methods, directly within the class.  
**Stretch Idea:** Create a method to return the species along with the name and age.

---

## Exercise 6: Private Attributes (Hard)
**Goal:** Modify the `Dog` class to have a private attribute `_owner`.  
**Hints:** Prefix the attribute with an underscore. Provide a method to set and get the owner.  
**Stretch Idea:** Implement a method that checks if the owner is set and returns a message accordingly.

---

## Exercise 7: Composition (Hard)
**Goal:** Create a class `Owner` that has a name and a list of `Dog` objects.  
**Hints:** Use a list to hold multiple dog instances.  
**Stretch Idea:** Add a method to the `Owner` class that returns the names of all owned dogs.

---

## Exercise 8: Polymorphism (Hard)
**Goal:** Create another subclass of `Dog` called `Poodle` that has a unique `bark` method.  
**Hints:** Ensure the `Poodle` class can still use methods from the `Dog` class.  
**Stretch Idea:** Implement a method that demonstrates polymorphism by calling `bark` on both `Bulldog` and `Poodle` instances.
```