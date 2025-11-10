from typing import List

class Vehicle:
    def __init__(self, make: str, model: str) -> None:
        """Initialize a Vehicle with make and model."""
        self.make = make
        self.model = model

    def info(self) -> str:
        """Return a string with the vehicle's make and model."""
        return f'{self.make} {self.model}'

    def start_engine(self) -> str:
        """Simulate starting the vehicle's engine."""
        return f'The engine of {self.info()} is now running.'

    def stop_engine(self) -> str:
        """Simulate stopping the vehicle's engine."""
        return f'The engine of {self.info()} has been turned off.'

# Example usage:
# my_vehicle = Vehicle('Honda', 'Civic')
# print(my_vehicle.info())  # Honda Civic
# print(my_vehicle.start_engine())  # The engine of Honda Civic is now running.
# print(my_vehicle.stop_engine())  # The engine of Honda Civic has been turned off.