from typing import Iterator, List

class CustomIterator:
    """A custom iterator that iterates over a list with a specific step."""

    def __init__(self, data: List[int], step: int = 1) -> None:
        """Initialize the iterator with a list and a step size.
        
        Args:
            data: A list of integers to iterate over.
            step: The step size for iteration.
        """
        self.data = data
        self.step = step
        self.index = 0

    def __iter__(self) -> 'CustomIterator':
        """Return the iterator object itself."""
        return self

    def __next__(self) -> int:
        """Return the next value in the iteration.
        
        Raises:
            StopIteration: If the end of the data is reached.
        """
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += self.step
        return value

    def reset(self) -> None:
        """Reset the iterator to the beginning of the data."""
        self.index = 0

# Example usage:
# iterator = CustomIterator([1, 2, 3, 4, 5], step=2)
# for value in iterator:
#     print(value)  # Output: 1, 3, 5
# iterator.reset()
# for value in iterator:
#     print(value)  # Output: 1, 3, 5