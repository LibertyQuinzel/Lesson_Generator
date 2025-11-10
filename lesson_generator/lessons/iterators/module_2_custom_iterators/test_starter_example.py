import pytest
from module_2_custom_iterators import Customrange

def test_demo():
    assert Customrange.demo() == 'ok'

def test_length():
    custom_range = Customrange(5)
    assert len(custom_range) == 5

def test_get_item():
    custom_range = Customrange(3)
    assert custom_range[1] == 1