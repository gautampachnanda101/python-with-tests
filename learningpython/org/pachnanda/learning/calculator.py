import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Calculator:
    def add(self, a, b):
        result = a + b
        logging.info(f"Adding {a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        logging.info(f"Subtracting {a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        logging.info(f"Multiplying {a} * {b} = {result}")
        return result

    def divide(self, a, b):
        if b == 0:
            logging.error("Division by zero error")
            raise ValueError("Cannot divide by zero")
        result = a / b
        logging.info(f"Dividing {a} / {b} = {result}")
        return result
