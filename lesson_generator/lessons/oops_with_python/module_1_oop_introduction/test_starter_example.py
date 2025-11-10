import pytest
from module_1_oop_introduction import Car

def test_demo():
    car = Car()
    assert car.demo() == 'ok'

def test_start_engine():
    car = Car()
    assert car.start_engine() == 'Engine started'

def test_stop_engine():
    car = Car()
    assert car.stop_engine() == 'Engine stopped'