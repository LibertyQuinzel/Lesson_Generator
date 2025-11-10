"""
Assignment B: Data Validator Implementation

EDUCATIONAL CONTEXT: Error Handling Patterns in Data Validation

This module demonstrates different error handling strategies for different
types of validation failures. The key insight is that validation failures
can be either expected (soft validation) or critical (hard validation).

DESIGN DECISIONS EXPLAINED:

1. SENTINEL VALUES USED FOR:
   - Optional field validation (failure is acceptable)
   - Soft validation warnings (continue processing)
   - Batch processing results (collect rather than fail fast)

2. EXCEPTIONS USED FOR:
   - Required field validation (failure is critical)
   - Invalid rule specifications (programming errors)
   - System-level validation failures (unexpected errors)

3. LOGGING STRATEGY:
   - INFO: Validation statistics, batch results
   - WARNING: Soft validation failures, optional field issues
   - ERROR: Hard validation failures, critical errors
   - DEBUG: Individual validation steps and decisions

4. HYBRID APPROACH FOR:
   - Batch validation (continue on soft failures, collect results)
   - Statistics tracking (accumulate both successes and failures)

LEARNING OBJECTIVES:
- Understand soft vs hard validation failure patterns
- Practice implementing validation with appropriate error handling
- Learn to design validation systems that balance strict and lenient checking
- See how logging supports validation debugging and monitoring
"""

import re
import logging
from typing import List, Dict, Tuple, Optional, Any

# Configure logging for the module
logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """
    Custom exception for critical validation failures.
    
    Used when required validation fails, indicating data that
    cannot be processed safely and must be rejected.
    """
    pass


class DataValidator:
    """
    Data validation with hybrid error handling patterns.
    
    VALIDATION PHILOSOPHY:
    - Optional validation → soft failures → sentinel values
    - Required validation → hard failures → exceptions
    - Batch processing → collect failures → hybrid approach
    - Statistics tracking → accumulate all results
    
    ERROR HANDLING CONTRACT:
    - validate_optional(): Returns cleaned value or None (never raises)
    - validate_required(): Returns value or raises ValidationError
    - validate_batch(): Returns (successes, failures) tuple
    - get_validation_stats(): Returns statistics dictionary
    """
    
    def __init__(self):
        """Initialize validator with empty statistics."""
        self._stats = {
            'optional_attempts': 0,
            'optional_failures': 0,
            'required_attempts': 0,
            'required_failures': 0,
            'batch_processed': 0
        }
        logger.info("DataValidator initialized")
    
    def validate_optional(self, value: Any, rules: List[str]) -> Optional[str]:
        """
        Soft validation for optional fields (SENTINEL PATTERN).
        
        PATTERN CHOICE: Sentinel values
        Optional field validation failure is expected and acceptable.
        Return None to indicate failure without disrupting flow.
        
        Args:
            value: Value to validate
            rules: List of validation rules to apply
            
        Returns:
            Cleaned string value or None (sentinel for failure)
        """
        self._stats['optional_attempts'] += 1
        
        if not isinstance(rules, list):
            logger.warning(f"Invalid rules for optional validation: {rules}")
            self._stats['optional_failures'] += 1
            return None  # Sentinel for invalid rules
        
        # Convert to string if possible
        try:
            str_value = str(value).strip() if value is not None else ""
        except Exception:
            logger.debug(f"Could not convert value to string: {value}")
            self._stats['optional_failures'] += 1
            return None  # Sentinel for conversion failure
        
        # Apply validation rules
        for rule in rules:
            if not self._apply_rule(str_value, rule, soft=True):
                logger.warning(f"Optional validation failed for rule '{rule}': {str_value}")
                self._stats['optional_failures'] += 1
                return None  # Sentinel for rule failure
        
        logger.debug(f"Optional validation passed: {str_value}")
        return str_value
    
    def validate_required(self, value: Any, rules: List[str]) -> str:
        """
        Hard validation for required fields (EXCEPTION PATTERN).
        
        PATTERN CHOICE: Exceptions
        Required field validation failure is critical and unexpected.
        Force caller to handle this serious condition explicitly.
        
        Args:
            value: Value to validate (must not be None/empty)
            rules: List of validation rules to apply
            
        Returns:
            Cleaned string value
            
        Raises:
            ValidationError: If validation fails
            ValueError: If rules are invalid
        """
        self._stats['required_attempts'] += 1
        
        if not isinstance(rules, list):
            raise ValueError(f"Invalid rules specification: {rules}")
        
        # Required values cannot be None or empty
        if value is None:
            self._stats['required_failures'] += 1
            logger.error("Required validation failed: value is None")
            raise ValidationError("Required field cannot be None")
        
        try:
            str_value = str(value).strip()
        except Exception as e:
            self._stats['required_failures'] += 1
            logger.error(f"Required validation failed: cannot convert to string: {e}")
            raise ValidationError(f"Cannot convert required field to string: {e}")
        
        if not str_value:
            self._stats['required_failures'] += 1
            logger.error("Required validation failed: empty value")
            raise ValidationError("Required field cannot be empty")
        
        # Apply validation rules strictly
        for rule in rules:
            if not self._apply_rule(str_value, rule, soft=False):
                self._stats['required_failures'] += 1
                logger.error(f"Required validation failed for rule '{rule}': {str_value}")
                raise ValidationError(f"Required field failed validation rule '{rule}'")
        
        logger.debug(f"Required validation passed: {str_value}")
        return str_value
    
    def validate_batch(self, data_list: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Batch validation with error collection (HYBRID PATTERN).
        
        PATTERN CHOICE: Hybrid approach
        Continue processing on individual failures, collect both
        successes and failures for caller to handle appropriately.
        
        Args:
            data_list: List of dictionaries to validate
            
        Returns:
            Tuple of (successful_items, failed_items)
        """
        if not isinstance(data_list, list):
            logger.error(f"Batch validation failed: expected list, got {type(data_list)}")
            return [], []  # Empty results for invalid input
        
        successes = []
        failures = []
        
        for i, item in enumerate(data_list):
            try:
                # Validate each item (simplified validation)
                if isinstance(item, dict) and 'email' in item:
                    validated_email = self.validate_optional(item['email'], ['email'])
                    if validated_email:
                        successes.append({**item, 'email': validated_email})
                    else:
                        failures.append({'index': i, 'item': item, 'error': 'invalid email'})
                else:
                    failures.append({'index': i, 'item': item, 'error': 'missing email field'})
            except Exception as e:
                failures.append({'index': i, 'item': item, 'error': str(e)})
        
        self._stats['batch_processed'] += len(data_list)
        logger.info(f"Batch validation completed: {len(successes)} successes, {len(failures)} failures")
        
        return successes, failures
    
    def _apply_rule(self, value: str, rule: str, soft: bool = True) -> bool:
        """
        Apply individual validation rule.
        
        Args:
            value: String value to validate
            rule: Validation rule name
            soft: Whether this is soft validation (affects logging)
            
        Returns:
            True if validation passes, False otherwise
        """
        if rule == 'email':
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, value))
        elif rule == 'phone':
            # Simple phone validation (digits, spaces, dashes, parentheses)
            pattern = r'^[\d\s\-\(\)]{10,15}$'
            return bool(re.match(pattern, value))
        elif rule == 'age':
            try:
                age = int(value)
                return 18 <= age <= 120
            except ValueError:
                return False
        elif rule == 'required':
            return bool(value and value.strip())
        else:
            # Unknown rule
            log_level = logger.warning if soft else logger.error
            log_level(f"Unknown validation rule: {rule}")
            return False
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Get validation statistics (INFORMATION PATTERN).
        
        Returns comprehensive statistics about validation operations.
        Never fails - returns current statistics state.
        """
        stats = self._stats.copy()
        stats['optional_success_rate'] = (
            (stats['optional_attempts'] - stats['optional_failures']) / 
            max(stats['optional_attempts'], 1)
        )
        stats['required_success_rate'] = (
            (stats['required_attempts'] - stats['required_failures']) / 
            max(stats['required_attempts'], 1)
        )
        
        logger.info(f"Validation statistics requested: {stats}")
        return stats