from typing import Any, Optional

from sgr_commhandler.api.data_types import DataTypes
from sgr_specification.v0.generic import EnumMapProduct


class DataPointValue(object):
    """
    Implements a data point value container.
    """

    def __init__(self, value: Any, data_type: DataTypes):
        """
        Constructs a data point value container.

        Parameters
        ----------
        value : Any
            An arbitrary value
        data_type : DataTypes
            An appropriate SGr data type
        """  
        self.value = value
        self.data_type = data_type


class EnumRecord(object):
    """
    Implements an SGr enum record.
    """

    def __init__(self, literal: Optional[str], ordinal: Optional[int], description: Optional[str]):
        """
        Constructs an enum record.

        Parameters
        ----------
        literal : Optional[str]
            A text literal value
        ordinal : Optional[int]
            A numeric ordinal value
        description : Optional[str]
            A text description
        """ 
        self.literal = literal
        self.ordinal = ordinal
        self.description = description

    @staticmethod
    def from_literal(literal: str, spec: EnumMapProduct) -> 'EnumRecord':
        if spec and spec.enum_entry:
            for entry in spec.enum_entry:
                if literal == entry.literal:
                    return EnumRecord(entry.literal, entry.ordinal, entry.description)
        return EnumRecord(None, None, None)

    @staticmethod
    def from_ordinal(ordinal: int, spec: EnumMapProduct) -> 'EnumRecord':
        if spec and spec.enum_entry:
            for entry in spec.enum_entry:
                if ordinal == entry.ordinal:
                    return EnumRecord(entry.literal, entry.ordinal, entry.description)
        return EnumRecord(None, None, None)
