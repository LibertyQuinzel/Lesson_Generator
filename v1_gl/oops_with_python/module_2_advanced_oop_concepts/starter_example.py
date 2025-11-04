"""
Starter Example: Advanced OOP Concepts: Inheritance and Polymorphism

This module demonstrates the principles of inheritance and polymorphism in Python OOP.

LEARNING OBJECTIVES:
- Understand the principles of OOP in Python
- Implement classes and objects
- Use inheritance and polymorphism
- Apply encapsulation and abstraction
- Design a simple OOP-based application

This module explores advanced OOP concepts focusing on inheritance, polymorphism, and encapsulation/abstraction to enhance code organization and reusability.
"""



class Animal:
    """
    Base class for different animal types that defines a common interface for speaking.
    
    This class demonstrates Inheritance, Polymorphism, Encapsulation, Abstraction through practical examples.
    """
    
    def speak(self):
        """
Returns the sound made by the animal.
        
        This method demonstrates: Polymorphism
        
        Args:
        
        Returns:
            str: Sound made by the animal.
        
        Example:
            >>> helper = Animal()
            >>> dog = Dog(); dog.speak()
            Bark
        """
        # This method is overridden in derived classes to provide specific sounds.
        def speak(self): pass
    



if __name__ == "__main__":
    """
    Demonstration script showing Advanced OOP Concepts: Inheritance and Polymorphism concepts.
    
    Run this file to see the examples in action:
    python starter_example.py
    """
    
    print("Advanced OOP Concepts: Inheritance and Polymorphism - Interactive Examples")
    print("=" * 60)
    
    animal_sound(Dog())
    animal_sound(Cat())
    
    print("\\n" + "=" * 60)
    print("🎉 Examples completed! Review the code above to understand:")
    print("   • Inheritance")
    print("   • Polymorphism")
    print("   • Encapsulation")
    print("   • Abstraction")
    print("\\nNext steps:")
    print("   1. Experiment with the code above")
    print("   2. Try modifying the examples")  
    print("   3. Move on to the assignment files")
    print("=" * 60)