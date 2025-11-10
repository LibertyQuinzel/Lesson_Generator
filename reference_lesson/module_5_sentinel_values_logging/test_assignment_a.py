"""
Tests for Assignment A: Configuration Manager

COMPREHENSIVE TESTING FOR CONFIGURATION MANAGEMENT PATTERNS

This test suite demonstrates how to test both sentinel value and exception
patterns in configuration management, verifying that appropriate error
handling strategies are used for different types of configuration operations.

TESTING STRATEGY:

1. SENTINEL VALUE TESTING:
   - Test optional configuration retrieval with defaults
   - Verify None is returned for invalid keys
   - Test file loading with invalid formats returns False

2. EXCEPTION TESTING:
   - Test required configuration raises ConfigurationError
   - Verify invalid parameters raise ValueError
   - Test file system errors are properly propagated

3. HYBRID PATTERN TESTING:
   - Test file loading success/failure scenarios
   - Verify consistent error handling within methods
   - Test proper exception vs sentinel value usage

LEARNING OBJECTIVES:
- Learn to test different error handling patterns appropriately
- Understand how to verify that methods use consistent error strategies
- Practice testing configuration management functionality
- See examples of testing both success and failure scenarios
"""

import pytest
import tempfile
import json
import os
from assignment_a import ConfigurationManager, ConfigurationError


class TestConfigurationManager:
    """
    Test cases for ConfigurationManager error handling patterns.
    
    TEST ORGANIZATION:
    Tests are grouped by method and cover both success and error cases,
    with special attention to verifying the correct error handling
    approach is used in each scenario.
    """
    
    def setup_method(self):
        """Set up fresh ConfigurationManager for each test."""
        self.config_mgr = ConfigurationManager()
        self.config_mgr.set_config("test_key", "test_value")
        self.config_mgr.set_config("database_url", "postgresql://localhost/test")
    
    def test_get_config_existing_key_success(self):
        """Test retrieving existing configuration (Happy Path)."""
        value = self.config_mgr.get_config("test_key")
        assert value == "test_value"
    
    def test_get_config_missing_key_returns_none_sentinel(self):
        """Test missing key returns None (Sentinel Pattern)."""
        value = self.config_mgr.get_config("nonexistent_key")
        assert value is None  # Sentinel value for missing key
    
    def test_get_config_missing_key_with_default_sentinel(self):
        """Test missing key with default returns default (Sentinel Pattern)."""
        value = self.config_mgr.get_config("nonexistent_key", "default_value")
        assert value == "default_value"
    
    def test_get_config_invalid_key_returns_none_sentinel(self):
        """Test invalid key parameters return None (Sentinel Pattern)."""
        # Empty string key
        assert self.config_mgr.get_config("") is None
        
        # None key
        assert self.config_mgr.get_config(None) is None
        
        # Non-string key
        assert self.config_mgr.get_config(123) is None
    
    def test_require_config_existing_key_success(self):
        """Test requiring existing configuration (Happy Path)."""
        value = self.config_mgr.require_config("database_url")
        assert value == "postgresql://localhost/test"
    
    def test_require_config_missing_key_raises_exception(self):
        """Test requiring missing key raises ConfigurationError (Exception Pattern)."""
        with pytest.raises(ConfigurationError) as exc_info:
            self.config_mgr.require_config("missing_required_key")
        
        assert "missing_required_key" in str(exc_info.value)
    
    def test_require_config_invalid_key_raises_exception(self):
        """Test requiring with invalid key raises ValueError (Exception Pattern)."""
        with pytest.raises(ValueError) as exc_info:
            self.config_mgr.require_config("")
        
        assert "Invalid configuration key" in str(exc_info.value)
    
    def test_set_config_success(self):
        """Test setting configuration successfully (Happy Path)."""
        result = self.config_mgr.set_config("new_key", "new_value")
        assert result is True
        
        # Verify it was actually set
        assert self.config_mgr.get_config("new_key") == "new_value"
    
    def test_set_config_invalid_key_raises_exception(self):
        """Test setting invalid key raises ValueError (Exception Pattern)."""
        with pytest.raises(ValueError):
            self.config_mgr.set_config("", "value")
        
        with pytest.raises(ValueError):
            self.config_mgr.set_config(None, "value")
    
    def test_set_config_none_value_raises_exception(self):
        """Test setting None value raises ValueError (Exception Pattern)."""
        with pytest.raises(ValueError) as exc_info:
            self.config_mgr.set_config("key", None)
        
        assert "cannot be None" in str(exc_info.value)
    
    def test_load_from_file_success(self):
        """Test loading valid JSON file (Happy Path)."""
        test_config = {"api_key": "secret123", "debug": True}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_filename = f.name
        
        try:
            result = self.config_mgr.load_from_file(temp_filename)
            assert result is True
            
            # Verify configuration was loaded
            assert self.config_mgr.get_config("api_key") == "secret123"
            assert self.config_mgr.get_config("debug") is True
        finally:
            os.unlink(temp_filename)
    
    def test_load_from_file_not_found_raises_exception(self):
        """Test loading nonexistent file raises FileNotFoundError (Exception Pattern)."""
        with pytest.raises(FileNotFoundError):
            self.config_mgr.load_from_file("nonexistent_file.json")
    
    def test_load_from_file_invalid_json_returns_false_sentinel(self):
        """Test loading invalid JSON returns False (Sentinel Pattern)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json content")  # Invalid JSON
            temp_filename = f.name
        
        try:
            result = self.config_mgr.load_from_file(temp_filename)
            assert result is False  # Sentinel value for invalid format
        finally:
            os.unlink(temp_filename)
    
    def test_load_from_file_non_object_returns_false_sentinel(self):
        """Test loading non-object JSON returns False (Sentinel Pattern)."""
        # JSON array instead of object
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(["not", "an", "object"], f)
            temp_filename = f.name
        
        try:
            result = self.config_mgr.load_from_file(temp_filename)
            assert result is False  # Sentinel value for wrong format
        finally:
            os.unlink(temp_filename)
    
    def test_get_all_config_returns_copy(self):
        """Test getting all configuration returns defensive copy."""
        all_config = self.config_mgr.get_all_config()
        
        # Should contain our test data
        assert all_config["test_key"] == "test_value"
        assert all_config["database_url"] == "postgresql://localhost/test"
        
        # Should be a copy (modifying shouldn't affect original)
        all_config["test_key"] = "modified"
        assert self.config_mgr.get_config("test_key") == "test_value"  # Unchanged
    
    def test_get_all_config_empty_manager(self):
        """Test getting all config from empty manager returns empty dict."""
        empty_mgr = ConfigurationManager()
        all_config = empty_mgr.get_all_config()
        
        assert all_config == {}
        assert isinstance(all_config, dict)
    
    def test_error_handling_consistency(self):
        """Test that error handling is consistent within each method."""
        # get_config should never raise exceptions
        assert self.config_mgr.get_config("") is None
        assert self.config_mgr.get_config(None) is None
        assert self.config_mgr.get_config("missing") is None
        
        # require_config should always raise for problems
        with pytest.raises((ConfigurationError, ValueError)):
            self.config_mgr.require_config("")
        
        with pytest.raises((ConfigurationError, ValueError)):
            self.config_mgr.require_config("missing")
        
        # set_config should raise for invalid input
        with pytest.raises(ValueError):
            self.config_mgr.set_config("", "value")
        
        with pytest.raises(ValueError):
            self.config_mgr.set_config("key", None)
    
    def test_logging_integration_basic(self):
        """Test that logging calls don't cause errors (Basic Integration Test)."""
        # This test verifies that logging calls work without detailed verification
        # In a real scenario, you'd use mocking to verify specific log messages
        
        # These operations should all log without causing errors
        self.config_mgr.get_config("test_key")
        self.config_mgr.get_config("missing_key", "default")
        
        try:
            self.config_mgr.require_config("missing")
        except ConfigurationError:
            pass  # Expected
        
        # If we reach here, logging didn't cause exceptions
        assert True