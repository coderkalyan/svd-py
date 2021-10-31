from dataclasses import dataclass, field
from enum import Enum, auto
from .access import Access
from .protection import Protection


class DataType(Enum):
    UINT8 = auto()
    UINT16 = auto()
    UINT32 = auto()
    UINT64 = auto()
    INT8 = auto()
    INT16 = auto()
    INT32 = auto()
    INT64 = auto()
    UINT8_PTR = auto()
    UINT16_PTR = auto()
    UINT32_PTR = auto()
    UINT64_PTR = auto()
    INT8_PTR = auto()
    INT16_PTR = auto()
    INT32_PTR = auto()
    INT64_PTR = auto()


class WriteOperation(Enum):
    MODIFY = auto()
    CLEAR = auto()
    SET = auto()
    ONE_TO_CLEAR = auto()
    ONE_TO_SET = auto()
    ONE_TO_TOGGLE = auto()
    ZERO_TO_CLEAR = auto()
    ZERO_TO_SET = auto()
    ZERO_TO_TOGGLE = auto()


class ReadOperation(Enum):
    NONE = auto()
    CLEAR = auto()
    SET = auto()
    MODIFY = auto()
    MODIFY_EXTERNAL = auto()


@dataclass
class Field:
    """Represents a field inside a register"""

    # these are required (and sanitized in the parser) but given default values anyway
    name: str = ""
    bit_range: tuple = tuple() # msb, lsb

    # these are optional
    description: str = ""
    access: Access = Access.READ_WRITE
    write_operation: WriteOperation = WriteOperation.MODIFY
    read_operation: ReadOperation = ReadOperation.NONE
    

@dataclass
class Register:
    """Represents a memory-mapped register"""

    # these are required (and sanitized in the parser) but given default values anyway
    name: str = ""
    address_offset: int = 0

    # these are optional
    display_name: str = ""
    description: str = ""
    size: int = 0
    access: Access = Access.READ_WRITE
    protection: Protection = Protection.SECURE
    reset_value: int = 0
    reset_mask: int = 0xFFFF
    data_type: DataType = DataType.UINT32
    write_operation: WriteOperation = WriteOperation.MODIFY
    read_operation: ReadOperation = ReadOperation.NONE

    fields: [Field] = field(default_factory=list)
