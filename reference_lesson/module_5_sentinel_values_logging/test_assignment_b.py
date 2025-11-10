"""
Tests for Assignment B: Data Validator

COMPREHENSIVE TESTING FOR DATA VALIDATION PATTERNS

This test suite demonstrates how to test both soft and hard validation
patterns, verifying that appropriate error handling strategies are used
for different types of validation scenarios.

TESTING STRATEGY:

1. SOFT VALIDATION TESTING:
   - Test optional validation returns None for failures
   - Verify successful validation returns cleaned values
   - Test invalid rules don't cause exceptions

2. HARD VALIDATION TESTING:
   - Test required validation raises ValidationError for failures
   - Verify successful validation returns cleaned values
   - Test invalid inputs raise appropriate exceptions

3. BATCH VALIDATION TESTING:
   - Test hybrid approach collects both successes and failures
   - Verify processing continues despite individual failures
   - Test proper result structure and statistics

LEARNING OBJECTIVES:
- Learn to test different validation strategies appropriately
- Understand how to verify soft vs hard validation behavior
- Practice testing batch processing with error collection
- See examples of testing validation statistics and logging
"""

import pytest
from assignment_b import DataValidator, ValidationError


class TestDataValidator:
    """
    Test cases for DataValidator error handling patterns.
    
    TEST ORGANIZATION:
    Tests are grouped by validation method and cover both success
    and failure scenarios, with emphasis on verifying the correct
    error handling approach for each validation type.
    """
    
    def setup_method(self):
        """Set up fresh DataValidator for each test."""
        self.validator = DataValidator()
    
    def test_validate_optional_success(self):
        """Test successful optional validation (Soft Validation Success)."""
        result = self.validator.validate_optional("test@example.com", ["email"])
        assert result == "test@example.com"
        
        result = self.validator.validate_optional("1234567890", ["phone"])
        assert result == "1234567890"
        
        result = self.validator.validate_optional("25", ["age"])
        assert result == "25"
    
    def test_validate_optional_failure_returns_none_sentinel(self):
        """Test optional validation failure returns None (Sentinel Pattern)."""
        # Invalid email
        result = self.validator.validate_optional("invalid-email", ["email"])
        assert result is None  # Sentinel for validation failure
        
        # Invalid phone
        result = self.validator.validate_optional("abc", ["phone"])
        assert result is None  # Sentinel for validation failure
        
        # Invalid age
        result = self.validator.validate_optional("150", ["age"])
        assert result is None  # Sentinel for validation failure
    
    def test_validate_optional_invalid_rules_returns_none_sentinel(self):
        """Test optional validation with invalid rules returns None (Sentinel Pattern)."""
        # Non-list rules
        result = self.validator.validate_optional("test@example.com", "email")
        assert result is None  # Sentinel for invalid rules
        
        # Unknown rule
        result = self.validator.validate_optional("value", ["unknown_rule"])
        assert result is None  # Sentinel for unknown rule
    
    def test_validate_optional_type_conversion_failure_returns_none_sentinel(self):
        """Test optional validation handles type conversion failures (Sentinel Pattern)."""
        # Object that can't be converted to string cleanly
        class UnconvertibleObject:
            def __str__(self):
                raise ValueError("Cannot convert to string")
        
        result = self.validator.validate_optional(UnconvertibleObject(), ["email"])
        assert result is None  # Sentinel for conversion failure
    
    def test_validate_required_success(self):
        """Test successful required validation (Hard Validation Success)."""
        result = self.validator.validate_required("test@example.com", ["email"])
        assert result == "test@example.com"
        
        result = self.validator.validate_required("valid text", ["required"])
        assert result == "valid text"
    
    def test_validate_required_none_value_raises_exception(self):
        """Test required validation with None raises ValidationError (Exception Pattern)."""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_required(None, ["email"])
        
        assert "cannot be None" in str(exc_info.value)
    
    def test_validate_required_empty_value_raises_exception(self):
        """Test required validation with empty value raises ValidationError (Exception Pattern)."""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_required("", ["required"])
        
        assert "cannot be empty" in str(exc_info.value)
        
        # Test whitespace-only value
        with pytest.raises(ValidationError):
            self.validator.validate_required("   ", ["required"])
    
    def test_validate_required_invalid_rules_raises_exception(self):
        """Test required validation with invalid rules raises ValueError (Exception Pattern)."""
        with pytest.raises(ValueError) as exc_info:
            self.validator.validate_required("value", "not_a_list")
        
        assert "Invalid rules" in str(exc_info.value)
    
    def test_validate_required_validation_failure_raises_exception(self):
        """Test required validation failure raises ValidationError (Exception Pattern)."""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_required("invalid-email", ["email"])
        
        assert "failed validation rule 'email'" in str(exc_info.value)
    
    def test_validate_required_conversion_failure_raises_exception(self):
        """Test required validation handles conversion failures (Exception Pattern)."""
        class UnconvertibleObject:
            def __str__(self):
                raise ValueError("Cannot convert")
        
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_required(UnconvertibleObject(), ["email"])
        
        assert "Cannot convert" in str(exc_info.value)
    
    def test_validate_batch_success_cases(self):
        """Test batch validation with all successful items (Hybrid Pattern Success)."""
        data = [
            {"email": "alice@example.com"},
            {"email": "bob@example.com"},
            {"email": "charlie@example.com"}
        ]
        
        successes, failures = self.validator.validate_batch(data)
        
        assert len(successes) == 3
        assert len(failures) == 0
        assert all(item["email"].endswith("@example.com") for item in successes)
    
    def test_validate_batch_mixed_results(self):
        """Test batch validation with mixed success/failure (Hybrid Pattern Mixed)."""
        data = [
            {"email": "valid@example.com"},
            {"email": "invalid-email"},
            {"not_email": "missing email field"},
            {"email": "another@valid.com"}
        ]
        
        successes, failures = self.validator.validate_batch(data)
        
        assert len(successes) == 2
        assert len(failures) == 2
        
        # Check success structure
        success_emails = [item["email"] for item in successes]
        assert "valid@example.com" in success_emails
        assert "another@valid.com" in success_emails
        
        # Check failure structure
        assert all("index" in failure for failure in failures)
        assert all("error" in failure for failure in failures)
    
    def test_validate_batch_all_failures(self):
        """Test batch validation with all failed items (Hybrid Pattern All Failures)."""
        data = [
            {"email": "invalid-email1"},
            {"email": "invalid-email2"},
            {"not_email": "missing field"}
        ]
        
        successes, failures = self.validator.validate_batch(data)
        
        assert len(successes) == 0
        assert len(failures) == 3
    
    def test_validate_batch_invalid_input_returns_empty(self):
        """Test batch validation with invalid input returns empty results."""
        successes, failures = self.validator.validate_batch("not_a_list")
        
        assert successes == []
        assert failures == []
    
    def test_validate_batch_empty_list(self):
        """Test batch validation with empty list returns empty results."""
        successes, failures = self.validator.validate_batch([])
        
        assert successes == []
        assert failures == []
    
    def test_get_validation_stats_initial(self):
        """Test initial validation statistics (Statistics Pattern)."""
        stats = self.validator.get_validation_stats()
        
        assert stats["optional_attempts"] == 0
        assert stats["optional_failures"] == 0
        assert stats["required_attempts"] == 0
        assert stats["required_failures"] == 0
        assert stats["batch_processed"] == 0
        assert stats["optional_success_rate"] == 1.0  # 0/0 → 1.0 (no failures)
        assert stats["required_success_rate"] == 1.0
    
    def test_get_validation_stats_after_operations(self):
        """Test validation statistics after operations (Statistics Tracking)."""
        # Perform various operations
        self.validator.validate_optional("valid@example.com", ["email"])  # Success
        self.validator.validate_optional("invalid", ["email"])  # Failure
        
        try:
            self.validator.validate_required("valid@example.com", ["email"])  # Success
        except ValidationError:
            pass
        
        try:
            self.validator.validate_required("invalid", ["email"])  # Failure
        except ValidationError:
            pass
        
        self.validator.validate_batch([{"email": "test@example.com"}])  # Batch
        
        stats = self.validator.get_validation_stats()
        
        assert stats["optional_attempts"] == 2
        assert stats["optional_failures"] == 1
        assert stats["required_attempts"] == 2
        assert stats["required_failures"] == 1
        assert stats["batch_processed"] == 1
        
        # Success rates should be calculated correctly
        assert stats["optional_success_rate"] == 0.5  # 1 success out of 2
        assert stats["required_success_rate"] == 0.5  # 1 success out of 2
    
    def test_email_validation_rule(self):
        """Test email validation rule specifically."""
        # Valid emails
        assert self.validator.validate_optional("test@example.com", ["email"]) is not None
        assert self.validator.validate_optional("user.name@domain.co.uk", ["email"]) is not None
        
        # Invalid emails
        assert self.validator.validate_optional("invalid-email", ["email"]) is None
        assert self.validator.validate_optional("@domain.com", ["email"]) is None
        assert self.validator.validate_optional("user@", ["email"]) is None
    
    def test_phone_validation_rule(self):
        """Test phone validation rule specifically."""
        # Valid phones
        assert self.validator.validate_optional("1234567890", ["phone"]) is not None
        assert self.validator.validate_optional("(123) 456-7890", ["phone"]) is not None
        
        # Invalid phones
        assert self.validator.validate_optional("abc", ["phone"]) is None
        assert self.validator.validate_optional("123", ["phone"]) is None  # Too short
    
    def test_age_validation_rule(self):
        """Test age validation rule specifically."""
        # Valid ages
        assert self.validator.validate_optional("25", ["age"]) is not None
        assert self.validator.validate_optional("18", ["age"]) is not None
        assert self.validator.validate_optional("120", ["age"]) is not None
        
        # Invalid ages
        assert self.validator.validate_optional("17", ["age"]) is None  # Too young
        assert self.validator.validate_optional("121", ["age"]) is None  # Too old
        assert self.validator.validate_optional("abc", ["age"]) is None  # Not a number
    
    def test_error_handling_consistency(self):
        """Test that error handling is consistent within each method."""
        # validate_optional should never raise exceptions
        assert self.validator.validate_optional("invalid", ["email"]) is None
        assert self.validator.validate_optional(None, ["email"]) is None
        assert self.validator.validate_optional("value", "invalid_rules") is None
        
        # validate_required should raise for problems
        with pytest.raises((ValidationError, ValueError)):
            self.validator.validate_required(None, ["email"])
        
        with pytest.raises((ValidationError, ValueError)):
            self.validator.validate_required("invalid", ["email"])
        
        # validate_batch should never raise exceptions
        successes, failures = self.validator.validate_batch("invalid_input")
        assert isinstance(successes, list)
        assert isinstance(failures, list)