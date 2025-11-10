"""
Assignment Part B: Student implementation template.
Students need to implement this class to pass the provided tests.
"""


class SimpleCalculator:
    """
    A simple calculator showing EAFP vs LBYL patterns.
    Students must implement methods to pass the tests.
    """
    
    def divide_eafp(self, a, b):
        """
        Divide two numbers using EAFP approach.
        
        Returns:
            float: result of division, or None if error occurs
            
        TODO: Implement using EAFP pattern
        - Try the division operation first
        - Handle ZeroDivisionError exception
        - Return None for any errors
        """
        # TODO: Implement this method
        pass
    
    def divide_lbyl(self, a, b):
        """
        Divide two numbers using LBYL approach.
        
        Returns:
            float: result of division, or None if invalid
            
        TODO: Implement using LBYL pattern
        - Check if denominator is not zero first
        - Only perform division if check passes
        """
        # TODO: Implement this method
        pass
    
    def get_item_eafp(self, items, index):
        """
        Get item from list using EAFP approach.
        
        Returns:
            Any: item at index, or None if error occurs
            
        TODO: Implement using EAFP pattern
        - Try to access items[index] first
        - Handle IndexError exception
        - Return None for any errors
        """
        # TODO: Implement this method
        pass
    
    def get_item_lbyl(self, items, index):
        """
        Get item from list using LBYL approach.
        
        Returns:
            Any: item at index, or None if invalid
            
        TODO: Implement using LBYL pattern
        - Check if index is valid first
        - Only access item if check passes
        """
        # TODO: Implement this method
        pass