from typing import Iterator

class SimpleCounter:
    """A simple iterator that counts from a start value to an end value."""

    def __init__(self, start: int, end: int) -> None:
        """Initialize the counter with a start and end value."""
        self.current = start
        self.end = end

    def __iter__(self) -> Iterator[int]:
        """Return the iterator object itself."""
        return self

    def __next__(self) -> int:
        """Return the next number in the count or raise StopIteration."""
        if self.current < self.end:
            result = self.current
            self.current += 1
            return result
        raise StopIteration

    def reset(self) -> None:
        """Reset the counter to the start value."""
        self.current = self.start

# Example usage:
# counter = SimpleCounter(1, 5)
# for number in counter:
#     print(number)  # Outputs: 1, 2, 3, 4
# counter.reset()  # Resets the counter to start from 1 again.