"""SGr Python Exceptions.

Custom exceptions to be used in the SGr Library code.
"""

class MyCustomException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()


    def __str__(self):
        """Return string representation."""
        return f"Custom Error: {self.message}"


class XMLValueException(Exception):
    ...

class DataPointException(ValueError):
    ...

class FunctionalProfileException(ValueError):
    ...

class ParsingError(Exception):
    ...