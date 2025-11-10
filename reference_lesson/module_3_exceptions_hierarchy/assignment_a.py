"""
Assignment Part A: FileProcessor class to be tested by students.
Students need to write tests to achieve 100% coverage.
"""


class ProcessingError(Exception):
    """Base exception for file processing operations."""
    pass


class FileNotFoundError(ProcessingError):
    """Exception raised when file doesn't exist."""
    pass


class InvalidFormatError(ProcessingError):
    """Exception raised when file format is invalid."""
    pass


class FileProcessor:
    """
    Simple file processor with custom exception hierarchy.
    Students should write comprehensive tests for this class.
    """
    
    def process_file(self, filename):
        """
        Process a file with validation.
        
        Raises:
            ProcessingError: If filename is empty
            InvalidFormatError: If file format is not .txt
        """
        if not filename:
            raise ProcessingError("Filename cannot be empty")
        
        if not filename.endswith('.txt'):
            raise InvalidFormatError(f"Invalid format: {filename}")
        
        return f"Processed {filename}"
    
    def read_file(self, filename):
        """
        Read file content with error handling.
        
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if filename == "missing.txt":
            raise FileNotFoundError(f"File not found: {filename}")
        
        return f"Content of {filename}"
    
    def validate_file(self, filename):
        """
        Validate file without processing.
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not filename or not filename.endswith('.txt'):
                return False
            return True
        except Exception:
            return False