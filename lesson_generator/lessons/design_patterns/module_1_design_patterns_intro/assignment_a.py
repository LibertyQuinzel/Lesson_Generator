from typing import Any

class DesignPatterns:
    """A class to demonstrate various design patterns."""

    def singleton(self) -> Any:
        """Demonstrates the Singleton pattern."""
        class Singleton:
            _instance = None

            def __new__(cls):
                if cls._instance is None:
                    cls._instance = super(Singleton, cls).__new__(cls)
                return cls._instance
        
        return Singleton()

    def factory(self, vehicle_type: str) -> Any:
        """Creates a vehicle based on the type provided."""
        class Car:
            def drive(self):
                return "Driving a car."

        class Bike:
            def ride(self):
                return "Riding a bike."

        if vehicle_type == 'car':
            return Car()
        elif vehicle_type == 'bike':
            return Bike()
        else:
            raise ValueError("Unknown vehicle type")

    def adapter(self, adaptee: Any) -> str:
        """Adapts the interface of an adaptee to a target interface."""
        class Adapter:
            def __init__(self, adaptee):
                self.adaptee = adaptee

            def request(self):
                return self.adaptee.specific_request()

        return Adapter(adaptee).request()

    # Example usage:
    # singleton_instance = self.singleton()
    # vehicle = self.factory('car')
    # adapted_result = self.adapter(adaptee_instance)