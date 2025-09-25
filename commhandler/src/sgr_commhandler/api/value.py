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

    def __str__(self) -> str:
        return self.value.__str__()

    def __repr__(self) -> str:
        return f'<DataPointValue value={self.value.__repr__()} type={self.data_type}>'

    def __eq__(self, other):
        if not isinstance(other, DataPointValue):
            return False
        return self.data_type == other.data_type and self.value == other.value


class EnumRecord(object):
    """
    Implements an SGr enum record.
    """

    def __init__(self, literal: Optional[str] = None, ordinal: Optional[int] = None, description: Optional[str] = None):
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
        return EnumRecord()

    @staticmethod
    def from_ordinal(ordinal: int, spec: EnumMapProduct) -> 'EnumRecord':
        if spec and spec.enum_entry:
            for entry in spec.enum_entry:
                if ordinal == entry.ordinal:
                    return EnumRecord(entry.literal, entry.ordinal, entry.description)
        return EnumRecord()

    def __str__(self) -> str:
        return self.literal if self.literal is not None else ''

    def __repr__(self) -> str:
        return f'<EnumRecord literal={self.literal} ordinal={self.ordinal}>'

    def __eq__(self, other):
        if not isinstance(other, EnumRecord):
            return False
        return self.literal == other.literal and self.ordinal == other.ordinal

    def __hash__(self):
        return hash((self.literal, self.ordinal))
