"""
Assignment A: Configuration Manager Implementation

EDUCATIONAL CONTEXT: Sentinel Values vs Exceptions in Configuration Management

This module demonstrates when to use sentinel values versus exceptions
in a configuration management system. The choice depends on whether
the error condition is expected or unexpected, and whether the caller
needs to handle the error or should be forced to notice it.

DESIGN DECISIONS EXPLAINED:

1. SENTINEL VALUES USED FOR:
   - Optional configuration keys (missing is expected behavior)
   - Invalid file formats (common, recoverable failure)
   - Default value scenarios (explicit "not found" handling)

2. EXCEPTIONS USED FOR:
   - Required configuration keys (missing is unexpected)
   - File system errors (unexpected, needs attention)
   - Invalid parameter types (programming errors)

3. LOGGING STRATEGY:
   - INFO: Normal operations, configuration changes
   - WARNING: Using defaults, expected missing values
   - ERROR: Required values missing, system failures
   - DEBUG: Detailed operation traces

LEARNING OBJECTIVES:
- Practice choosing appropriate error handling patterns
- Implement consistent error handling within a single class
- Design effective logging for configuration management
- Create methods with clear error handling contracts
"""

import logging
import json

# Configure logging for the module
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """
    Custom exception for configuration-related errors.
    
    Used when required configuration is missing or invalid,
    indicating a critical system failure that must be addressed.
    """
    pass


class ConfigurationManager:
    """
    Configuration management with hybrid error handling patterns.
    
    PATTERN EXPLANATION:
    This class demonstrates both sentinel value and exception patterns:
    - Sentinel values for optional/expected failures
    - Exceptions for required/unexpected failures
    - Logging for operational visibility
    
    ERROR HANDLING CONTRACT:
    - get_config(): Returns value, default, or None (never raises)
    - require_config(): Returns value or raises exception
    - set_config(): Returns True or raises for invalid input
    - load_from_file(): Returns True/False or raises for system errors
    """
    
    def __init__(self):
        """Initialize with empty configuration and logging setup."""
        self._config = {}
        logger.info("ConfigurationManager initialized")
    
    def get_config(self, key, default=None):
        """
        Get configuration value with optional default (SENTINEL PATTERN).
        
        PATTERN CHOICE: Sentinel values
        Missing configuration is often expected, so we return defaults
        rather than raising exceptions. Callers can handle None explicitly.
        
        Returns:
            Configuration value, default, or None (sentinel)
        """
        if not isinstance(key, str) or not key.strip():
            logger.warning(f"Invalid config key requested: {key}")
            return None  # Sentinel for invalid input
        
        value = self._config.get(key, default)
        if value == default and key not in self._config:
            logger.debug(f"Config key '{key}' not found, using default: {default}")
        else:
            logger.debug(f"Config key '{key}' retrieved: {value}")
        
        return value
    
    def require_config(self, key):
        """
        Get required configuration value (EXCEPTION PATTERN).
        
        PATTERN CHOICE: Exceptions
        Required configuration missing is unexpected and critical.
        Force caller to handle this serious condition explicitly.
        
        Returns:
            Configuration value
        Raises:
            ConfigurationError: If required key is missing
            ValueError: If key is invalid
        """
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"Invalid configuration key: {key}")
        
        if key not in self._config:
            logger.error(f"Required configuration missing: {key}")
            raise ConfigurationError(f"Required configuration key '{key}' not found")
        
        value = self._config[key]
        logger.debug(f"Required config '{key}' retrieved: {value}")
        return value
    
    def set_config(self, key, value):
        """
        Set configuration value with validation (EXCEPTION PATTERN).
        
        PATTERN CHOICE: Exceptions
        Invalid parameters are programming errors that should not
        be silently ignored. Force caller to provide valid input.
        
        Returns:
            True if successful
        Raises:
            ValueError: If key or value is invalid
        """
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"Invalid configuration key: {key}")
        
        if value is None:
            raise ValueError("Configuration value cannot be None")
        
        old_value = self._config.get(key)
        self._config[key] = value
        
        if old_value != value:
            logger.info(f"Configuration updated: {key} = {value}")
        
        return True
    
    def load_from_file(self, filename):
        """
        Load configuration from file (HYBRID PATTERN).
        
        PATTERN CHOICE: Hybrid approach
        - File system errors → exceptions (unexpected, critical)
        - Invalid JSON format → False (expected, recoverable)
        
        Returns:
            True if successful, False if invalid format
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file cannot be read
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                logger.warning(f"Invalid config format in {filename}: not a JSON object")
                return False  # Sentinel for invalid format
            
            self._config.update(data)
            logger.info(f"Configuration loaded from {filename}: {len(data)} keys")
            return True
            
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"File system error loading config: {e}")
            raise  # Re-raise system errors
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in {filename}: {e}")
            return False  # Sentinel for invalid format
    
    def get_all_config(self):
        """
        Get copy of all configuration (SAFE ACCESS PATTERN).
        
        Returns copy to prevent external modification of internal state.
        Never fails - returns empty dict if no configuration loaded.
        """
        logger.debug(f"All configuration requested: {len(self._config)} keys")
        return self._config.copy()  # Defensive copy