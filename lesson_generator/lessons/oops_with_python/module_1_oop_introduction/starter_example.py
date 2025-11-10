class Car:
    """A class representing a car with make and model attributes."""
    
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model

    def info(self) -> str:
        """Return the information of the car."""
        return f'{self.make} {self.model}'

    def start_engine(self) -> str:
        """Simulate starting the car's engine."""
        return f'The engine of {self.make} {self.model} has started.'

    def stop_engine(self) -> str:
        """Simulate stopping the car's engine."""
        return f'The engine of {self.make} {self.model} has stopped.'

    def demo(self) -> str:
        """A trivial demo method."""
        return 'ok'