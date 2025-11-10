class DesignPatterns:
    """A class to demonstrate core design patterns in Python."""

    class Singleton:
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(DesignPatterns.Singleton, cls).__new__(cls)
            return cls._instance

    class Factory:
        class Car:
            def drive(self):
                return "Driving a car."

        class Bike:
            def ride(self):
                return "Riding a bike."

        def create_vehicle(self, vehicle_type):
            if vehicle_type == 'car':
                return self.Car()
            elif vehicle_type == 'bike':
                return self.Bike()
            else:
                raise ValueError("Unknown vehicle type")

    def demo(self):
        return 'ok'