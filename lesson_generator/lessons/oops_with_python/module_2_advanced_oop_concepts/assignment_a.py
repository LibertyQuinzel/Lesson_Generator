from typing import List

class AdvancedOOP:
    """Demonstrates inheritance and polymorphism in OOP."""

    def describe_shapes(self, shapes: List[str]) -> List[str]:
        """Returns descriptions of the given shapes.
        
        Args:
            shapes: A list of shape names.
        
        Returns:
            A list of descriptions for each shape.
        
        Example:
            >>> shapes = ['Circle', 'Square']
            >>> obj.describe_shapes(shapes)
            ['This is a Circle', 'This is a Square']
        """
        return [f'This is a {shape}' for shape in shapes]

    def calculate_area(self, shape: str, dimension: float) -> float:
        """Calculates the area of a given shape based on its dimension.
        
        Args:
            shape: The name of the shape (e.g., 'Circle', 'Square').
            dimension: The dimension (radius for Circle, side for Square).
        
        Returns:
            The area of the shape.
        
        Example:
            >>> obj.calculate_area('Circle', 5)
            78.5
        """
        if shape == 'Circle':
            return 3.14 * (dimension ** 2)
        elif shape == 'Square':
            return dimension ** 2
        else:
            raise ValueError("Unsupported shape")

    def list_shapes(self) -> List[str]:
        """Lists common shapes.
        
        Returns:
            A list of common shapes.
        
        Example:
            >>> obj.list_shapes()
            ['Circle', 'Square', 'Triangle']
        """
        return ['Circle', 'Square', 'Triangle']