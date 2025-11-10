from typing import List

class DesignPatternApplication:
    def __init__(self):
        self.observers: List[Observer] = []

    def register_observer(self, observer: 'Observer') -> None:
        """Register an observer to the notification system."""
        self.observers.append(observer)

    def notify_observers(self, message: str) -> None:
        """Notify all registered observers with a message."""
        for observer in self.observers:
            observer.update(message)

    def execute_strategy(self, strategy: 'Strategy', a: int, b: int) -> int:
        """Execute a given strategy with two numbers."""
        return strategy.compute(a, b)

class Observer:
    def update(self, message: str) -> None:
        """Receive an update message."""
        pass  # Implementation in concrete observer classes

class Strategy:
    def compute(self, a: int, b: int) -> int:
        """Compute a result based on two integers."""
        pass  # Implementation in concrete strategy classes

# Example usage:
# observer = ConcreteObserver()
# app = DesignPatternApplication()
# app.register_observer(observer)
# app.notify_observers("Hello, Observers!")
# result = app.execute_strategy(Addition(), 5, 3)  # Should return 8