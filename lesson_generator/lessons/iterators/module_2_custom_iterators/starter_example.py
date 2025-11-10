class CustomRange:
    """A custom iterator that mimics the behavior of the built-in range function."""
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.current = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if (self.step > 0 and self.current >= self.end) or (self.step < 0 and self.current <= self.end):
            raise StopIteration
        current_value = self.current
        self.current += self.step
        return current_value

    def sum(self) -> int:
        """Returns the sum of the range values."""
        total = 0
        for value in self:
            total += value
        return total

    def count(self) -> int:
        """Returns the count of numbers in the range."""
        count = 0
        for _ in self:
            count += 1
        return count

def demo() -> str:
    return 'ok'