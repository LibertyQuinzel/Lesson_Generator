"""
Starter Example: Custom Exception Hierarchy

A comprehensive demonstration of Python's exception hierarchy and creating
custom exceptions for better error handling and code maintainability.

LEARNING OBJECTIVES:
- Understand Python's built-in exception hierarchy
- Learn to create custom exceptions with proper inheritance
- Master exception chaining and error boundaries
- See practical examples of structured error handling

KEY EXCEPTION CONCEPTS:

1. EXCEPTION HIERARCHY:
   BaseException -> Exception -> Specific Exceptions
   Most custom exceptions should inherit from Exception
   
2. CUSTOM EXCEPTIONS:
   Purpose: Create domain-specific error types
   Benefits: Better error categorization, clearer error handling
   
3. EXCEPTION CHAINING:
   Purpose: Preserve original error context while adding new information
   Pattern: raise CustomError("message") from original_error
   
4. ERROR BOUNDARIES:
   Purpose: Establish clear points where errors are caught and handled
   Benefits: Prevent error propagation, convert internal errors to user-friendly messages

DESIGN PHILOSOPHY:
This example shows how to create a hierarchy of custom exceptions for a
simple user management system, demonstrating practical error handling patterns.
"""


class UserManagementError(Exception):
    """
    Base exception for all user management operations.
    
    EXCEPTION DESIGN PRINCIPLES:
    - Inherit from Exception (not BaseException) 
    - Provide clear, descriptive exception names
    - Include helpful error messages and context
    - Support exception chaining for debugging
    
    This serves as the root of our custom exception hierarchy,
    allowing callers to catch all user-related errors with one except block.
    """
    
    def __init__(self, message, error_code=None):
        """
        Initialize with message and optional error code.
        
        CUSTOM EXCEPTION DESIGN:
        Adding error codes helps with programmatic error handling
        and provides structured error information for logging/debugging.
        
        Args:
            message (str): Human-readable error description
            error_code (str, optional): Machine-readable error identifier
        """
        super().__init__(message)
        self.error_code = error_code


class ValidationError(UserManagementError):
    """Exception raised when user data fails validation."""
    pass


class UserNotFoundError(UserManagementError):
    """Exception raised when requested user doesn't exist."""
    pass


class SimpleUserManager:
    """
    A simple user management system demonstrating exception handling patterns.
    
    EXCEPTION HANDLING STRATEGY:
    - Use specific custom exceptions for different error types
    - Implement error boundaries to handle internal vs external errors  
    - Provide clear error messages with context
    - Use exception chaining to preserve debugging information
    """
    
    def __init__(self):
        """Initialize with empty user storage."""
        self.users = {}
    
    def add_user(self, username, email):
        """
        Add a user with validation and custom exception handling.
        
        VALIDATION WITH CUSTOM EXCEPTIONS:
        Rather than returning error codes or None, this method raises
        specific exceptions that clearly indicate what went wrong.
        
        Args:
            username (str): User's username
            email (str): User's email address
            
        Raises:
            ValidationError: If username or email is invalid
            
        Example:
            >>> manager = SimpleUserManager()
            >>> manager.add_user("alice", "alice@example.com")
            >>> manager.add_user("", "bad")  # Raises ValidationError
        """
        # Validation with specific exceptions
        if not username or not isinstance(username, str):
            raise ValidationError("Username must be a non-empty string", "INVALID_USERNAME")
        
        if not email or "@" not in email:
            raise ValidationError("Email must be valid", "INVALID_EMAIL")
        
        # Store user
        self.users[username] = {"email": email}
    
    def get_user(self, username):
        """
        Get user by username with exception-based error handling.
        
        EXCEPTION VS RETURN VALUE:
        Instead of returning None for missing users, this method raises
        a specific exception. This makes error handling explicit and
        prevents silent failures.
        
        Args:
            username (str): Username to look up
            
        Returns:
            dict: User information
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        if username not in self.users:
            raise UserNotFoundError(f"User '{username}' not found", "USER_NOT_FOUND")
        
        return self.users[username]