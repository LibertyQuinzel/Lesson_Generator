class SimpleCounter:
    """A simple iterator that counts from a start value to an end value."""

    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.end:
            value = self.current
            self.current += 1
            return value
        raise StopIteration

def demo():
    return 'ok'