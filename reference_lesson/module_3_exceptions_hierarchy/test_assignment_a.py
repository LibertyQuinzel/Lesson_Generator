"""
Assignment Part A: Test template for students.
Students need to complete these tests to achieve 100% coverage.
"""

import pytest
from assignment_a import FileProcessor, ProcessingError, FileNotFoundError, InvalidFormatError


class TestFileProcessor:
    """Test template - students should complete these tests."""
    
    def setup_method(self):
        """Setup test fixture."""
        self.processor = FileProcessor()
    
    def test_process_file_success(self):
        """Test processing valid file."""
        # TODO: Test process_file("test.txt") returns success message
        pass
    
    def test_process_file_empty_filename(self):
        """Test processing with empty filename."""
        # TODO: Test process_file("") raises ProcessingError
        pass
    
    def test_process_file_invalid_format(self):
        """Test processing file with invalid format."""
        # TODO: Test process_file("test.pdf") raises InvalidFormatError
        pass
    
    def test_read_file_success(self):
        """Test reading existing file."""
        # TODO: Test read_file("existing.txt") returns content
        pass
    
    def test_read_file_not_found(self):
        """Test reading non-existent file."""
        # TODO: Test read_file("missing.txt") raises FileNotFoundError
        pass
    
    def test_validate_file_valid(self):
        """Test validating valid file."""
        # TODO: Test validate_file("test.txt") returns True
        pass
    
    def test_validate_file_invalid(self):
        """Test validating invalid file."""
        # TODO: Test validate_file("test.pdf") returns False
        pass
    
    def test_exception_hierarchy(self):
        """Test exception inheritance relationships."""
        # TODO: Test that InvalidFormatError is instance of ProcessingError
        # TODO: Test that FileNotFoundError is instance of ProcessingError
        pass
    
    # TODO: Add more tests to achieve 100% coverage
    # Consider edge cases like None input, different file extensions