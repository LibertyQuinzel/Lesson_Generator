"""
Starter Example: User Service with Sentinel Values and Logging

A comprehensive demonstration of when to use sentinel values vs exceptions
and how to implement proper logging for defensive programming.

LEARNING OBJECTIVES:
- Understand when to use sentinel values vs exceptions
- Learn proper logging techniques for defensive programming
- See practical examples of error handling strategies
- Master logging levels and structured error reporting

KEY ERROR HANDLING CONCEPTS:

1. SENTINEL VALUES:
   Purpose: Indicate error conditions with special return values
   Benefits: Fast, simple to check, no exception overhead
   Use when: Errors are expected, simple binary conditions

2. EXCEPTIONS:
   Purpose: Signal exceptional conditions that disrupt normal flow
   Benefits: Rich error information, separate error handling
   Use when: Errors are unexpected, need detailed error context

3. LOGGING:
   Purpose: Record events, errors, and system state for debugging
   Benefits: Production debugging, audit trails, monitoring
   Strategy: Use appropriate levels, include context, protect sensitive data

DESIGN PHILOSOPHY:
This example shows a user service that uses both approaches appropriately:
sentinel values for common cases, exceptions for exceptional cases,
and comprehensive logging throughout.
"""

import logging


# Configure logging for this module
logger = logging.getLogger(__name__)


class UserNotFoundError(Exception):
    """Exception raised when user is not found in exceptional cases."""
    pass


class UserService:
    """
    User service demonstrating sentinel values vs exceptions with logging.
    
    ERROR HANDLING STRATEGY:
    - find_user(): Uses sentinel values (None) for common "not found" case
    - get_user(): Uses exceptions for strict "must exist" requirements
    - Both methods include appropriate logging for debugging and monitoring
    
    LOGGING STRATEGY:
    - INFO level: Normal operations and important events
    - WARNING level: Unexpected but recoverable conditions
    - ERROR level: Error conditions that affect functionality
    - DEBUG level: Detailed information for troubleshooting
    """
    
    def __init__(self):
        """
        Initialize user service with sample data and logging.
        
        DEFENSIVE PROGRAMMING WITH LOGGING:
        Log service initialization to help with system startup debugging
        and provide audit trail of service lifecycle.
        """
        self.users = {
            "alice": {"email": "alice@example.com", "role": "admin"},
            "bob": {"email": "bob@example.com", "role": "user"},
            "charlie": {"email": "charlie@example.com", "role": "user"}
        }
        
        logger.info(f"UserService initialized with {len(self.users)} users")
    
    def find_user(self, username):
        """
        Find user using sentinel value approach (returns None if not found).
        
        SENTINEL VALUE PATTERN:
        This method uses None as a sentinel value to indicate "user not found".
        This approach is appropriate because:
        - Looking up non-existent users is a common, expected operation
        - Callers can easily check for None
        - No exception overhead for common case
        - Simple binary result (found/not found)
        
        LOGGING STRATEGY:
        - DEBUG: Log all lookup attempts for troubleshooting
        - INFO: Log successful finds for audit trail  
        - WARNING: Log not found cases (may indicate issues)
        
        Args:
            username (str): Username to search for
            
        Returns:
            dict or None: User data if found, None if not found (sentinel value)
            
        Example:
            >>> service = UserService()
            >>> user = service.find_user("alice")
            >>> if user is not None:
            ...     print(f"Found user: {user['email']}")
            >>> 
            >>> missing = service.find_user("missing")
            >>> if missing is None:
            ...     print("User not found")
        """
        logger.debug(f"Looking up user: {username}")
        
        # Input validation with logging
        if not username or not isinstance(username, str):
            logger.warning(f"Invalid username provided: {repr(username)}")
            return None  # Sentinel value for invalid input
        
        # Perform lookup
        user = self.users.get(username)
        
        if user is not None:
            logger.info(f"User found: {username}")
            return user
        else:
            logger.warning(f"User not found: {username}")
            return None  # Sentinel value for "not found"
    
    def get_user(self, username):
        """
        Get user using exception approach (raises exception if not found).
        
        EXCEPTION PATTERN:
        This method raises an exception when user is not found because:
        - Method name implies user MUST exist (get vs find)
        - Caller expects valid user object, not None
        - Exception provides rich error information
        - Separates error handling from main logic flow
        
        LOGGING STRATEGY:
        - INFO: Log successful retrievals
        - ERROR: Log failed retrievals before raising exception
        - Include context in error messages for debugging
        
        Args:
            username (str): Username to retrieve
            
        Returns:
            dict: User data (guaranteed to exist)
            
        Raises:
            UserNotFoundError: If user doesn't exist
            ValueError: If username is invalid
            
        Example:
            >>> service = UserService()
            >>> try:
            ...     user = service.get_user("alice")
            ...     print(f"Got user: {user['email']}")
            ... except UserNotFoundError:
            ...     print("Handle missing user error")
        """
        logger.debug(f"Getting user (strict): {username}")
        
        # Input validation with exceptions (strict mode)
        if not username or not isinstance(username, str):
            error_msg = f"Invalid username: {repr(username)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Perform lookup
        user = self.users.get(username)
        
        if user is not None:
            logger.info(f"User retrieved successfully: {username}")
            return user
        else:
            error_msg = f"User not found: {username}"
            logger.error(error_msg)
            raise UserNotFoundError(error_msg)
    
    def add_user(self, username, email, role="user"):
        """
        Add user with comprehensive logging and error handling.
        
        HYBRID APPROACH:
        This method demonstrates using both patterns appropriately:
        - Sentinel value (False) for common validation failures
        - Exception for unexpected system errors
        - Comprehensive logging throughout
        
        LOGGING STRATEGY:
        - INFO: Successful user additions (important business events)
        - WARNING: Validation failures and duplicate users
        - ERROR: System errors that prevent operation
        - Include all relevant context in log messages
        
        Args:
            username (str): Username for new user
            email (str): Email address
            role (str): User role (default: "user")
            
        Returns:
            bool: True if user added successfully, False if validation failed
            
        Raises:
            RuntimeError: If system error prevents addition
        """
        logger.debug(f"Adding user: {username}, email: {email}, role: {role}")
        
        # Input validation using sentinel values (common validation errors)
        if not username or not isinstance(username, str):
            logger.warning(f"Invalid username for user creation: {repr(username)}")
            return False  # Sentinel value for validation failure
        
        if not email or "@" not in email:
            logger.warning(f"Invalid email for user {username}: {repr(email)}")
            return False  # Sentinel value for validation failure
        
        # Check for duplicate user (common business rule violation)
        if username in self.users:
            logger.warning(f"Attempted to add duplicate user: {username}")
            return False  # Sentinel value for business rule violation
        
        try:
            # Simulate potential system error during user creation
            self.users[username] = {"email": email, "role": role}
            
            logger.info(f"User added successfully: {username} ({role})")
            return True
            
        except Exception as e:
            # Unexpected system errors use exceptions
            error_msg = f"System error adding user {username}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def list_users_by_role(self, role):
        """
        List users by role with logging for audit and debugging.
        
        SENTINEL VALUE FOR EMPTY RESULTS:
        Returns empty list (natural sentinel) rather than None or exception
        because "no users found" is a valid, expected result.
        
        Args:
            role (str): Role to filter by
            
        Returns:
            list: List of usernames with specified role (empty if none found)
        """
        logger.debug(f"Listing users with role: {role}")
        
        matching_users = [
            username for username, user_data in self.users.items()
            if user_data.get("role") == role
        ]
        
        logger.info(f"Found {len(matching_users)} users with role '{role}'")
        return matching_users