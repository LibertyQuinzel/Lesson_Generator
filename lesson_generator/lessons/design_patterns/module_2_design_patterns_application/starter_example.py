from typing import Protocol

class Observer(Protocol):
    def update(self, message: str) -> None:
        ...

class ConcreteObserver:
    def update(self, message: str) -> None:
        print(f'Observer received: {message}')

class Subject:
    """Subject class that maintains a list of observers and notifies them of changes."""
    
    def __init__(self) -> None:
        self._observers = []

    def register(self, observer: Observer) -> None:
        """Register an observer to the subject."""
        self._observers.append(observer)

    def notify(self, message: str) -> None:
        """Notify all registered observers with a message."""
        for observer in self._observers:
            observer.update(message)

    def demo(self) -> str:
        return 'ok'

# Example usage
if __name__ == "__main__":
    subject = Subject()
    observer1 = ConcreteObserver()
    observer2 = ConcreteObserver()

    subject.register(observer1)
    subject.register(observer2)

    subject.notify("Hello Observers!")  # Both observers will receive this message.