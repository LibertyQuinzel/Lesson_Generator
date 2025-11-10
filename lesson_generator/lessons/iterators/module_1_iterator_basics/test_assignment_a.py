"""
Student-facing test template for Assignment A

This template intentionally contains TODOs and failing placeholders so students
can iteratively implement tests for the provided assignment code. It follows
the GIVEN / WHEN / THEN structure and encourages four focused tests: happy-path,
edge-case, error-handling and an additional contract/behaviour test.
"""

import pytest

pytest
module_1_introduction_to_iterators.SimpleCounter
from module_1_iterator_basics import Simplecounter

"""
STUDENT TASK

Replace the TODO sections below with concrete tests for Simplecounter.
Use the GIVEN / WHEN / THEN comments to keep tests well-structured.
Aim for at least four focused tests: happy-path, edge-case, error-handling and an
additional behavioural/contract test.
"""

def test_happy_path_todo():
    """Happy-path: replace with a concrete assertion."""
    # GIVEN
    obj = Simplecounter() if 'Simplecounter' else None
    # WHEN
    # TODO: call a representative method on obj
    # THEN
    pytest.fail("TODO: implement happy-path assertion")


def test_edge_case_todo():
    """Edge-case: invalid or boundary inputs should be handled."""
    # GIVEN
    obj = Simplecounter() if 'Simplecounter' else None
    # WHEN
    # TODO: trigger an edge-case
    # THEN
    pytest.fail("TODO: implement edge-case assertion")


def test_error_handling_todo():
    """Error handling: ensure validation or exceptions behave as documented."""
    # GIVEN
    obj = Simplecounter() if 'Simplecounter' else None
    # WHEN / THEN
    pytest.fail("TODO: assert expected exception or error message")


def test_additional_contracts_todo():
    """Additional behavioural/contract test."""
    # GIVEN
    obj = Simplecounter() if 'Simplecounter' else None
    # WHEN
    # TODO: exercise additional behaviour
    # THEN
    pytest.fail("TODO: implement additional behavioural assertion")

if __name__ == "__main__":
    pytest.main([__file__, "-q"])