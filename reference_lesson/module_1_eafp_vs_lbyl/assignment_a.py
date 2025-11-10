"""
Assignment Part A: Simple Number Processor to be tested by students.
Students need to write tests to achieve 100% coverage.
"""

class NumberProcessor:
    """
    Simple class showing EAFP and LBYL patterns.
    Students should write tests to cover all code paths.
    """
    
    def parse_number_eafp(self, value):
        """
        Parse value to integer using EAFP approach.
        Returns None if parsing fails.
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def parse_number_lbyl(self, value):
        """
        Parse value to integer using LBYL approach.
        Checks type and format before converting.
        """
        if not isinstance(value, (int, str)):
            return None
        
        if isinstance(value, int):
            return value
        
        if value.isdigit():
            return int(value)
        
        return None
    
    def get_first_eafp(self, items):
        """Get first item from list using EAFP."""
        try:
            return items[0]
        except (IndexError, TypeError):
            return None
    
    def get_first_lbyl(self, items):
        """Get first item from list using LBYL."""
        if items and len(items) > 0:
            return items[0]
        return None