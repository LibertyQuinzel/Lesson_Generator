from typing import List

class Animal:
    """Base class for all animals, demonstrating inheritance and polymorphism."""
    
    def speak(self) -> str:
        """Returns a generic animal sound."""
        return 'Animal sound'


class Dog(Animal):
    """Dog class that inherits from Animal and overrides the speak method."""
    
    def speak(self) -> str:
        """Returns the sound a dog makes."""
        return 'Bark'


class Cat(Animal):
    """Cat class that inherits from Animal and overrides the speak method."""
    
    def speak(self) -> str:
        """Returns the sound a cat makes."""
        return 'Meow'


def animal_sounds(animals: List[Animal]) -> List[str]:
    """Returns a list of sounds made by the provided animals."""
    return [animal.speak() for animal in animals]


def demo() -> str:
    """A trivial demo method to enable a minimal smoke test."""
    return 'ok'