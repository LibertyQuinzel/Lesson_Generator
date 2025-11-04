"""
Starter Example: Understanding Iterators and Generators

A basic introduction to iterators and generators in Python.


LEARNING OBJECTIVES:
- Understand what iterators are.
- Learn how to create generators using functions.
- Explore the benefits of lazy evaluation.

Iterators allow you to traverse through a collection without needing to store the entire collection in memory. Generators provide a simple way to create iterators using a function that yields values one at a time.
"""

from typing import Generator


class Simplegenerator:
    """
    A basic generator class to illustrate the concept of lazy evaluation.
    
    This class demonstrates Iterators, Generators, Lazy Evaluation through practical examples.
    """
    
    def count_up_to(self, n):
        """
        A generator that counts up to n.
        
        This method demonstrates: Using a generator to yield values lazily.
        
        Args:
            n (int): The upper limit to count up to.
        
        Returns:
            Generator: Yields numbers from 1 to n.
        
        Example:
            >>> helper = Simplegenerator()
            >>> for number in SimpleGenerator.count_up_to(5): print(number)
            1
2
3
4
5

        """
        # The function yields one number at a time, allowing you to handle large ranges without using much memory.
        def count_up_to(n: int) -> Generator[int, None, None]:
            for i in range(1, n + 1):
                yield i
    



if __name__ == "__main__":
    """
    Demonstration script showing Understanding Iterators and Generators concepts.
    
    Run this file to see the examples in action:
    python 
    """
    
    print("Understanding Iterators and Generators - Interactive Examples")
    print("=" * 60)
    
    for number in SimpleGenerator.count_up_to(5): print(number)
    
    print("\\n" + "=" * 60)
    print("🎉 Examples completed! Review the code above to understand:")
    print("   • Iterators")
    print("   • Generators")
    print("   • Lazy Evaluation")
    print("\\nNext steps:")
    print("   1. Experiment with the code above")
    print("   2. Try modifying the examples")  
    print("   3. Move on to the assignment files")
    print("=" * 60)