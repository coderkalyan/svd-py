from enum import Enum, auto


class Protection(Enum):
    """Register protection"""
    SECURE = auto()
    NON_SECURE = auto()
    PRIVILEGED = auto()
