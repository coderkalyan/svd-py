from enum import Enum, auto


class Access(Enum):
    """Access rights for a register"""
    READ_ONLY = auto()
    WRITE_ONLY = auto()
    READ_WRITE = auto()
    WRITE_ONCE = auto()
    READ_WRITE_ONCE = auto()
