"""
Tests for SimpleUserManager starter example.

COMPREHENSIVE EXCEPTION TESTING STRATEGY

This test suite demonstrates how to test custom exceptions, exception hierarchies,
and error handling patterns systematically.

TESTING EXCEPTION HANDLING:

1. POSITIVE TESTING:
   - Verify normal operations work without exceptions
   - Test that valid inputs produce expected results

2. NEGATIVE TESTING:
   - Test that invalid inputs raise appropriate exceptions
   - Verify exception types, messages, and error codes
   - Test exception inheritance relationships

3. EXCEPTION BOUNDARY TESTING:
   - Test error handling at system boundaries
   - Verify exception chaining preserves context
   - Test that internal errors are properly converted

LEARNING OBJECTIVES:
- Learn to test both success and failure scenarios
- Understand how to verify exception types and messages
- Practice testing custom exception hierarchies
- See examples of comprehensive exception testing

TESTING PHILOSOPHY:
Exception testing is crucial because errors are often the most complex
part of a system. Proper testing ensures graceful failure handling.
"""

import pytest
from starter_example import (
    SimpleUserManager, 
    UserManagementError, 
    ValidationError, 
    UserNotFoundError
)


class TestSimpleUserManager:
    """
    Comprehensive test cases for SimpleUserManager exception handling.
    
    TEST ORGANIZATION:
    Tests are organized by functionality (add_user, get_user) and
    include both positive cases (should work) and negative cases (should raise exceptions).
    
    EXCEPTION TESTING STRATEGY:
    Each test that expects an exception verifies the exception type,
    message content, and any custom attributes like error codes.
    """
    
    def setup_method(self):
        """
        Set up test fixture before each test method.
        
        CLEAN TEST ENVIRONMENT:
        Each test gets a fresh UserManager instance to ensure
        test isolation and prevent side effects between tests.
        """
        self.manager = SimpleUserManager()
    
    def test_add_user_success(self):
        """
        Test successful user addition (Happy Path).
        
        TESTING CONCEPT: Normal Operation Verification
        This test ensures that the basic functionality works correctly
        when provided with valid input, without any exceptions.
        
        EXPECTED BEHAVIOR:
        - Method should complete without raising exceptions
        - User should be stored in the system
        - Subsequent retrieval should work correctly
        """
        self.manager.add_user("alice", "alice@example.com")
        user = self.manager.get_user("alice")
        assert user["email"] == "alice@example.com"
    
    def test_add_user_empty_username(self):
        """
        Test ValidationError for empty username (Custom Exception Testing).
        
        TESTING CONCEPT: Input Validation Exception Testing
        This test verifies that our custom ValidationError is raised
        with appropriate message and error code for invalid username.
        
        EXPECTED BEHAVIOR:
        - ValidationError should be raised (not generic Exception)
        - Error message should be descriptive and helpful
        - Error code should be set correctly for programmatic handling
        
        EXCEPTION TESTING PATTERN:
        Using pytest.raises() to capture and verify exception details.
        """
        with pytest.raises(ValidationError) as exc_info:
            self.manager.add_user("", "test@example.com")
        
        # Verify exception details
        assert "Username must be a non-empty string" in str(exc_info.value)
        assert exc_info.value.error_code == "INVALID_USERNAME"
    
    def test_add_user_invalid_email(self):
        """
        Test ValidationError for invalid email format (Validation Testing).
        
        TESTING CONCEPT: Business Rule Validation
        This test ensures that business rules (email format) are properly
        enforced through custom exceptions.
        
        EXPECTED BEHAVIOR:
        - ValidationError should be raised for emails without @ symbol
        - Error message should indicate email validation failure
        - Appropriate error code should be provided
        """
        with pytest.raises(ValidationError) as exc_info:
            self.manager.add_user("bob", "invalid-email")
        
        assert "Email must be valid" in str(exc_info.value)
        assert exc_info.value.error_code == "INVALID_EMAIL"
    
    def test_get_user_not_found(self):
        """
        Test UserNotFoundError for missing user (Domain-Specific Exception).
        
        TESTING CONCEPT: Domain-Specific Error Testing
        Tests that domain-specific exceptions (UserNotFoundError) are raised
        appropriately when business conditions aren't met.
        
        EXPECTED BEHAVIOR:
        - UserNotFoundError should be raised (specific exception type)
        - Error message should include the username that wasn't found
        - Error code should indicate the specific error type
        
        EXCEPTION HIERARCHY TESTING:
        UserNotFoundError inherits from UserManagementError, so it can
        be caught by either specific or general exception handlers.
        """
        with pytest.raises(UserNotFoundError) as exc_info:
            self.manager.get_user("nonexistent")
        
        assert "User 'nonexistent' not found" in str(exc_info.value)
        assert exc_info.value.error_code == "USER_NOT_FOUND"
    
    def test_exception_hierarchy(self):
        """
        Test that custom exceptions inherit from base exception (Hierarchy Testing).
        
        TESTING CONCEPT: Exception Inheritance Verification
        This test verifies that our exception hierarchy works correctly,
        allowing both specific and general exception handling.
        
        EXPECTED BEHAVIOR:
        - ValidationError should be instance of UserManagementError
        - UserNotFoundError should be instance of UserManagementError  
        - Both should be catchable by base exception handler
        
        PRACTICAL IMPORTANCE:
        This allows callers to catch all user-related errors with one
        except block if desired, or handle specific errors separately.
        """
        # Test that ValidationError can be caught as UserManagementError
        with pytest.raises(UserManagementError):
            self.manager.add_user("", "test@example.com")
        
        # Test that UserNotFoundError can be caught as UserManagementError  
        with pytest.raises(UserManagementError):
            self.manager.get_user("missing")