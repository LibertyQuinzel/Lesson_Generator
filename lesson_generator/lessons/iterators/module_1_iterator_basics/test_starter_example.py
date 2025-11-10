import pytest
from module_1_iterator_basics import Simplecounter

def test_demo():
    assert Simplecounter.demo() == 'ok'

def test_increment():
    counter = Simplecounter()
    counter.increment()
    assert counter.count == 1

def test_reset():
    counter = Simplecounter()
    counter.increment()
    counter.reset()
    assert counter.count == 0