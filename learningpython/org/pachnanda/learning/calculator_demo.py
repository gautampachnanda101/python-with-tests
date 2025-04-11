#!/usr/bin/env python3
# learningpython/org/pachnanda/learning/calculator_demo.py

"""Demo script for demonstrating the Calculator class."""

from org.pachnanda.learning.calculator import Calculator


def main():
    """Demonstrate the functionality of the Calculator class."""
    print("Calculator Demo")
    print("--------------")

    # Create a calculator instance
    calc = Calculator()

    # Demonstrate addition
    print("\nAddition:")
    print(f"5 + 3 = {calc.add(5, 3)}")

    # Demonstrate subtraction
    print("\nSubtraction:")
    print(f"10 - 4 = {calc.subtract(10, 4)}")

    # Demonstrate multiplication
    print("\nMultiplication:")
    print(f"6 * 7 = {calc.multiply(6, 7)}")

    # Demonstrate division
    print("\nDivision:")
    print(f"20 / 5 = {calc.divide(20, 5)}")

    # Demonstrate error handling
    print("\nError handling:")
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"Error caught: {e}")


if __name__ == "__main__":
    main()
