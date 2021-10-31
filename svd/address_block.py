from dataclasses import dataclass
from enum import Enum, auto
from .protection import Protection


class AddressBlockUsage(Enum):
    REGISTERS = auto()
    BUFFER = auto()
    RESERVED = auto()


@dataclass
class AddressBlock:
    # these are required (and sanitized in the parser) but given default values anyway
    offset: int = 0
    size: int = 0
    usage: AddressBlockUsage = AddressBlockUsage.REGISTERS

    # these are optional
    protection: Protection = Protection.SECURE
