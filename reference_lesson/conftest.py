"""
Shared pytest configuration and fixtures for the Defensive Programming course.

This file provides common fixtures and configuration that can be used across
all modules in the defensive programming lesson.
"""

import pytest
import sys
import os
import logging
from typing import Any, Dict, List
from unittest.mock import Mock, patch
import tempfile
import shutil


# Add all module directories to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module_1_eafp_vs_lbyl'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module_2_invariants_assertions'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module_3_exceptions_hierarchy'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module_4_design_by_contract'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'module_5_sentinel_values_logging'))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests that need file system operations."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_file():
    """Create a temporary file for tests."""
    fd, temp_file_path = tempfile.mkstemp()
    os.close(fd)  # Close the file descriptor, keep the path
    yield temp_file_path
    try:
        os.unlink(temp_file_path)
    except OSError:
        pass  # File might have been deleted by test


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        'users': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
        ],
        'products': [
            {'id': 101, 'name': 'Widget A', 'price': 10.99, 'stock': 50},
            {'id': 102, 'name': 'Widget B', 'price': 15.99, 'stock': 0},
            {'id': 103, 'name': 'Widget C', 'price': 8.99, 'stock': 25},
        ],
        'orders': [
            {'id': 1001, 'user_id': 1, 'product_id': 101, 'quantity': 2},
            {'id': 1002, 'user_id': 2, 'product_id': 103, 'quantity': 1},
        ]
    }


@pytest.fixture
def mock_database():
    """Mock database connection for testing."""
    mock_db = Mock()
    mock_db.connect.return_value = True
    mock_db.disconnect.return_value = True
    mock_db.execute.return_value = {'rows_affected': 1}
    mock_db.query.return_value = []
    return mock_db


@pytest.fixture
def mock_network():
    """Mock network operations for testing."""
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = Mock()
        mock_response.read.return_value = b'{"status": "success"}'
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response
        yield mock_urlopen


@pytest.fixture
def capture_logs():
    """Capture logging output for testing."""
    log_capture_string = []
    
    class ListHandler(logging.Handler):
        def emit(self, record):
            log_capture_string.append(self.format(record))
    
    # Create and configure the handler
    handler = ListHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to root logger
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    yield log_capture_string
    
    # Clean up
    logger.removeHandler(handler)


@pytest.fixture
def mock_file_system():
    """Mock file system operations."""
    with patch('os.path.exists') as mock_exists, \
         patch('open', create=True) as mock_open, \
         patch('os.remove') as mock_remove:
        
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = "mock file content"
        
        yield {
            'exists': mock_exists,
            'open': mock_open,
            'remove': mock_remove
        }


@pytest.fixture
def defensive_programming_examples():
    """Provide examples for defensive programming concepts."""
    return {
        'valid_inputs': [
            1, 2, 3, "hello", [1, 2, 3], {"key": "value"}
        ],
        'invalid_inputs': [
            None, "", [], {}, -1, 0
        ],
        'edge_cases': [
            float('inf'), float('-inf'), float('nan'),
            sys.maxsize, -sys.maxsize, 2**64
        ],
        'error_conditions': [
            'file_not_found', 'permission_denied', 'network_timeout',
            'invalid_format', 'out_of_memory', 'disk_full'
        ]
    }


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    # Clear all existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Reset logging level
    logging.root.setLevel(logging.WARNING)
    
    yield
    
    # Clean up after test
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.perf_counter()
        
        def stop(self):
            self.end_time = time.perf_counter()
            return self.elapsed
        
        @property
        def elapsed(self):
            if self.start_time is None:
                return 0
            if self.end_time is None:
                return time.perf_counter() - self.start_time
            return self.end_time - self.start_time
    
    return Timer()


# Pytest markers configuration (also defined in pytest.ini)
pytest_plugins = []

# Custom assertion helpers
def assert_defensive_behavior(func, invalid_input, expected_exception=None):
    """
    Helper function to test defensive programming behavior.
    
    Args:
        func: Function to test
        invalid_input: Input that should trigger defensive behavior
        expected_exception: Expected exception type (if any)
    """
    if expected_exception:
        with pytest.raises(expected_exception):
            func(invalid_input)
    else:
        # Should handle gracefully without raising
        result = func(invalid_input)
        assert result is not None or result == []  # Some form of safe handling


def assert_contract_violation(func, *args, **kwargs):
    """
    Helper to test contract violations (preconditions, postconditions, invariants).
    
    Args:
        func: Function that should violate a contract
        *args, **kwargs: Arguments to pass to function
    """
    with pytest.raises(AssertionError):
        func(*args, **kwargs)


# Module-specific fixtures can be added here or in individual test files
@pytest.fixture
def eafp_examples():
    """Examples for EAFP (Easier to Ask for Forgiveness than Permission) testing."""
    return {
        'existing_keys': ['key1', 'key2', 'key3'],
        'missing_keys': ['missing1', 'missing2'],
        'sample_dict': {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
        'sample_list': [1, 2, 3, 4, 5]
    }


@pytest.fixture
def lbyl_examples():
    """Examples for LBYL (Look Before You Leap) testing."""
    return {
        'valid_indices': [0, 1, 2],
        'invalid_indices': [-1, 10, 100],
        'sample_data': ['a', 'b', 'c'],
        'conditions_to_check': ['length', 'type', 'range', 'existence']
    }


# Parametrized fixtures for common test scenarios
@pytest.fixture(params=[
    (ValueError, "Invalid value"),
    (TypeError, "Invalid type"),
    (KeyError, "Missing key"),
    (IndexError, "Index out of range")
])
def exception_scenarios(request):
    """Parametrized fixture for testing different exception scenarios."""
    exception_type, message = request.param
    return exception_type, message


@pytest.fixture(params=[
    None, "", 0, [], {}, False
])
def falsy_values(request):
    """Parametrized fixture for testing falsy values."""
    return request.param


@pytest.fixture(params=[
    1, "hello", [1, 2, 3], {"key": "value"}, True
])
def truthy_values(request):
    """Parametrized fixture for testing truthy values."""
    return request.param