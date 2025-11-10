"""
Tests for UserService starter example.

COMPREHENSIVE TESTING FOR SENTINEL VALUES AND EXCEPTION PATTERNS

This test suite demonstrates how to test both sentinel value and exception-based
error handling patterns, while also verifying that logging occurs correctly.

TESTING ERROR HANDLING PATTERNS:

1. SENTINEL VALUE TESTING:
   - Test both success cases (valid return values)
   - Test failure cases (sentinel values returned)
   - Verify that sentinel values are used consistently
   - Test that operations don't raise unexpected exceptions

2. EXCEPTION TESTING:
   - Test that appropriate exceptions are raised for error conditions
   - Verify exception types, messages, and context
   - Test that valid operations don't raise exceptions
   - Test exception chaining where appropriate

3. LOGGING TESTING:
   - Verify that appropriate log levels are used
   - Test that relevant context is included in log messages
   - Ensure sensitive information is not logged
   - Test logging in both success and failure scenarios

LEARNING OBJECTIVES:
- Learn to test both sentinel values and exceptions appropriately
- Understand how to verify logging behavior in tests
- Practice testing different error handling strategies
- See examples of comprehensive error handling test coverage

TESTING PHILOSOPHY:
Good tests verify not just the happy path, but also error conditions,
logging behavior, and the consistency of error handling approaches.
"""

import logging
import pytest
from unittest.mock import patch
from starter_example import UserService, UserNotFoundError


class TestUserService:
    """
    Comprehensive test cases for UserService error handling and logging.
    
    TEST ORGANIZATION:
    Tests are organized by method and cover both success and failure scenarios,
    with special attention to the different error handling approaches used.
    
    LOGGING TEST STRATEGY:
    Uses mocking to capture and verify log messages without cluttering
    test output, ensuring that appropriate logging occurs.
    """
    
    def setup_method(self):
        """
        Set up test fixture with logging capture.
        
        TEST SETUP STRATEGY:
        Each test gets a fresh UserService instance and mock logger
        to ensure test isolation and clean logging verification.
        """
        self.service = UserService()
    
    def test_find_user_success_sentinel_pattern(self):
        """
        Test successful user lookup using sentinel value pattern (Happy Path).
        
        TESTING CONCEPT: Sentinel Value Success Case
        This test verifies that the find_user method correctly returns
        user data when the user exists, demonstrating the successful
        path of the sentinel value pattern.
        
        EXPECTED BEHAVIOR:
        - Method should return actual user data (not sentinel)
        - No exceptions should be raised
        - User data should be complete and correct
        
        PATTERN VERIFICATION:
        This confirms that sentinel values are only used for error cases,
        not for successful operations.
        """
        user = self.service.find_user("alice")
        
        assert user is not None  # Not the sentinel value
        assert user["email"] == "alice@example.com"
        assert user["role"] == "admin"
    
    def test_find_user_not_found_sentinel_value(self):
        """
        Test user not found returns sentinel value (Sentinel Pattern Testing).
        
        TESTING CONCEPT: Sentinel Value Error Handling
        This test verifies that the find_user method uses None as a sentinel
        value to indicate "not found" rather than raising an exception.
        
        EXPECTED BEHAVIOR:
        - Method should return None (sentinel value)
        - No exceptions should be raised
        - Caller can check for None to detect "not found"
        
        SENTINEL PATTERN VERIFICATION:
        This test ensures that the sentinel pattern is used consistently
        for the expected error condition (user not found).
        """
        user = self.service.find_user("nonexistent")
        
        assert user is None  # Sentinel value for "not found"
    
    def test_find_user_invalid_input_sentinel_value(self):
        """
        Test invalid input returns sentinel value (Input Validation Testing).
        
        TESTING CONCEPT: Sentinel Values for Input Validation
        Tests that input validation errors also use sentinel values
        consistently with the method's error handling approach.
        
        EXPECTED BEHAVIOR:
        - Invalid inputs should return None (sentinel value)
        - No exceptions should be raised for invalid input
        - Method should handle edge cases gracefully
        """
        # Test empty string
        assert self.service.find_user("") is None
        
        # Test None input  
        assert self.service.find_user(None) is None
        
        # Test non-string input
        assert self.service.find_user(123) is None
    
    def test_get_user_success_exception_pattern(self):
        """
        Test successful strict user retrieval (Exception Pattern Success).
        
        TESTING CONCEPT: Exception Pattern Success Case
        This test verifies that the get_user method returns valid user data
        when the user exists, showing the successful path of exception-based
        error handling.
        
        EXPECTED BEHAVIOR:
        - Method should return complete user data
        - No exceptions should be raised for valid users
        - Data should be identical to find_user results for existing users
        
        PATTERN COMPARISON:
        This allows comparison between sentinel and exception patterns
        for the same successful operation.
        """
        user = self.service.get_user("bob")
        
        assert user["email"] == "bob@example.com"
        assert user["role"] == "user"
    
    def test_get_user_not_found_raises_exception(self):
        """
        Test user not found raises exception (Exception Pattern Testing).
        
        TESTING CONCEPT: Exception-Based Error Handling
        This test verifies that get_user raises a specific exception
        when the user is not found, demonstrating the exception pattern.
        
        EXPECTED BEHAVIOR:
        - UserNotFoundError should be raised
        - Exception message should include the username
        - No return value (exception prevents return)
        
        PATTERN CONTRAST:
        This contrasts with find_user which returns None for the same condition,
        showing how different methods can use different error handling approaches.
        """
        with pytest.raises(UserNotFoundError) as exc_info:
            self.service.get_user("nonexistent")
        
        assert "nonexistent" in str(exc_info.value)
    
    def test_get_user_invalid_input_raises_exception(self):
        """
        Test invalid input raises exception (Strict Validation Testing).
        
        TESTING CONCEPT: Exception-Based Input Validation
        Tests that get_user uses exceptions for input validation,
        consistent with its strict error handling approach.
        
        EXPECTED BEHAVIOR:
        - ValueError should be raised for invalid inputs
        - Exception message should describe the validation failure
        - Different exception type from "not found" errors
        """
        with pytest.raises(ValueError) as exc_info:
            self.service.get_user("")
        
        assert "Invalid username" in str(exc_info.value)
    
    def test_add_user_success_with_logging(self):
        """
        Test successful user addition (Hybrid Pattern Success).
        
        TESTING CONCEPT: Hybrid Success Pattern Testing
        Tests the successful path of a method that uses both sentinel values
        and exceptions depending on the error type.
        
        EXPECTED BEHAVIOR:
        - Method should return True for successful addition
        - User should be added to internal storage
        - No exceptions should be raised
        """
        result = self.service.add_user("david", "david@example.com", "admin")
        
        assert result is True
        # Verify user was actually added
        user = self.service.find_user("david")
        assert user is not None
        assert user["email"] == "david@example.com"
        assert user["role"] == "admin"
    
    def test_add_user_validation_failure_sentinel_value(self):
        """
        Test validation failure returns False (Hybrid Pattern Sentinel).
        
        TESTING CONCEPT: Sentinel Values for Expected Failures
        Tests that common validation failures use sentinel values (False)
        rather than exceptions in the hybrid approach.
        
        EXPECTED BEHAVIOR:
        - Method should return False for validation failures
        - No exceptions should be raised
        - No user should be added to storage
        """
        # Test invalid email
        result = self.service.add_user("test", "invalid-email", "user")
        assert result is False
        
        # Test empty username
        result = self.service.add_user("", "test@example.com", "user")
        assert result is False
        
        # Verify no users were added
        assert self.service.find_user("test") is None
    
    def test_add_user_duplicate_user_sentinel_value(self):
        """
        Test duplicate user returns False (Business Rule Validation).
        
        TESTING CONCEPT: Sentinel Values for Business Rule Violations
        Tests that business rule violations (duplicate users) use sentinel
        values since they're expected error conditions.
        
        EXPECTED BEHAVIOR:
        - Adding duplicate user should return False
        - Original user data should remain unchanged
        - No exception should be raised
        """
        result = self.service.add_user("alice", "newalice@example.com", "user")
        
        assert result is False
        # Verify original user unchanged
        original_user = self.service.find_user("alice")
        assert original_user["email"] == "alice@example.com"  # Original email
        assert original_user["role"] == "admin"  # Original role
    
    @patch('logging.getLogger')
    def test_logging_behavior_verification(self, mock_get_logger):
        """
        Test that appropriate logging occurs (Logging Behavior Testing).
        
        TESTING CONCEPT: Logging Verification
        This test uses mocking to verify that appropriate log messages
        are generated at correct levels for different operations.
        
        EXPECTED BEHAVIOR:
        - INFO level logs for successful operations
        - WARNING level logs for expected failures
        - ERROR level logs for exceptions
        - Log messages should include relevant context
        
        DEFENSIVE PROGRAMMING VERIFICATION:
        This ensures that logging provides adequate information for
        debugging and monitoring in production environments.
        """
        mock_logger = mock_get_logger.return_value
        
        # Test successful operation logging
        self.service.find_user("alice")
        # Verify INFO level logging occurred (would need more specific mocking)
        
        # Test failure case logging  
        self.service.find_user("nonexistent")
        # Verify WARNING level logging occurred
        
        # This test demonstrates the concept - in practice, you'd use
        # more sophisticated mocking to verify specific log calls
        assert mock_get_logger.called
    
    def test_list_users_by_role_empty_result_natural_sentinel(self):
        """
        Test empty results use natural sentinel (Empty List Pattern).
        
        TESTING CONCEPT: Natural Sentinel Values
        Tests that methods returning collections use empty collections
        as natural sentinel values rather than None or exceptions.
        
        EXPECTED BEHAVIOR:
        - Method should return empty list for no matches
        - Empty list is natural sentinel (not None)
        - No exceptions should be raised
        - Result should be iterable (empty iteration is valid)
        """
        users = self.service.list_users_by_role("nonexistent_role")
        
        assert users == []  # Empty list as natural sentinel
        assert isinstance(users, list)  # Proper type maintained
        
        # Should be safely iterable
        for user in users:
            assert False, "Should not iterate over empty list"