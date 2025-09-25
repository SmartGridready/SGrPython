from enum import Enum


class DataTypes(Enum):
    """Defines the data point data types supported by the SGr specification."""

    UNDEFINED = "UNDEFINED"
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    ENUM = "ENUM"
    BOOLEAN = "BOOLEAN"
    BITMAP = "BITMAP"
    DATE_TIME = "DATE_TIME"
    JSON = "JSON"
