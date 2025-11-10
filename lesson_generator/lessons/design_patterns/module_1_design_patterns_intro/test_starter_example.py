import pytest
from module_1_design_patterns_intro import Designpatterns

def test_demo():
    dp = Designpatterns()
    assert dp.demo() == 'ok'

def test_example_method():
    dp = Designpatterns()
    assert dp.example_method() == 'expected_result'  # Replace 'expected_result' with the actual expected output