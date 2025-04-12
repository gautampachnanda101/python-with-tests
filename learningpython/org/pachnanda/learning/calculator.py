"""Calculator module providing basic arithmetic operations with logging.

This module implements a Calculator class that performs basic arithmetic
operations (addition, subtraction, multiplication, division) and logs
the operations and their results.
"""

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Calculator:
    """A simple calculator class that performs basic arithmetic operations.

    This class provides methods for addition, subtraction, multiplication,
    and division. Each operation is logged using the logging module.
    """

    def add(self, a, b):
        """Add two numbers and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            The sum of a and b
        """
        result = a + b
        logging.info(f"Adding {a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        """Subtract the second number from the first and return the result.

        Args:
            a: Number to subtract from
            b: Number to subtract

        Returns:
            The difference between a and b
        """
        result = a - b
        logging.info(f"Subtracting {a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        """Multiply two numbers and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            The product of a and b
        """
        result = a * b
        logging.info(f"Multiplying {a} * {b} = {result}")
        return result

    def divide(self, a, b):
        """Divide the first number by the second and return the result.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            The quotient of a divided by b

        Raises:
            ValueError: If b is zero (division by zero)
        """
        if b == 0:
            logging.error("Division by zero error")
            raise ValueError("Cannot divide by zero")
        result = a / b
        logging.info(f"Dividing {a} / {b} = {result}")
        return result
