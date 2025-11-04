"""
Starter Example: Advanced OOP Concepts in Python

Explore advanced object-oriented programming concepts including inheritance, polymorphism, and method overriding.

LEARNING OBJECTIVES:
- Understand the principles of OOP in Python
- Implement classes and objects effectively
- Utilize inheritance and polymorphism
- Apply encapsulation in Python code
- Design simple OOP-based applications

This module covers how inheritance allows classes to inherit properties and methods from other classes, how polymorphism enables different classes to be treated as instances of the same class through a common interface, and how method overriding customizes inherited methods.
"""



class Animal:
    """
    Base class for different animal types which defines a common interface.
    
    This class demonstrates Inheritance, Polymorphism, Method Overriding through practical examples.
    """
    
    def speak(self):
        """
Returns the sound the animal makes.
        
        This method demonstrates: Polymorphism
        
        Args:
        
        Returns:
            str: The sound made by the animal.
        
        Example:
            >>> helper = Animal()
            >>> Dog().speak()
            Bark
        """
        # The speak method is overridden in subclasses to provide specific sounds.
        class Animal:
            def speak(self):
                raise NotImplementedError

        class Dog(Animal):
            def speak(self):
                return 'Bark'

        class Cat(Animal):
            def speak(self):
                return 'Meow'

        for animal in [Dog(), Cat()]:
            print(animal.speak())
    



if __name__ == "__main__":
    """
    Demonstration script showing Advanced OOP Concepts in Python concepts.
    
    Run this file to see the examples in action:
    python starter_example.py
    """
    
    print("Advanced OOP Concepts in Python - Interactive Examples")
    print("=" * 60)
    
    for animal in [Dog(), Cat()]: print(animal.speak())
    
    print("\\n" + "=" * 60)
    print("🎉 Examples completed! Review the code above to understand:")
    print("   • Inheritance")
    print("   • Polymorphism")
    print("   • Method Overriding")
    print("\\nNext steps:")
    print("   1. Experiment with the code above")
    print("   2. Try modifying the examples")  
    print("   3. Move on to the assignment files")
    print("=" * 60)