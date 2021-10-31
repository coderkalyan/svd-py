from dataclasses import dataclass
from enum import Enum, auto


class Endian(Enum):
    LITTLE = auto()
    BIG = auto()
    SELECTABLE = auto()
    OTHER = auto()
    

@dataclass
class CPU:
    """Represents a device's CPU"""

    # these are required (and sanitized in the parser) but given default values anyway
    name: str = ""
    revision: str = ""
    endian: Endian = Endian.LITTLE
    mpu: bool = False
    fpu: bool = False
    nvic_priority_bits: int = 32
    vendor_systick: bool = False

    # these are optional
    fpu_double_precision: bool = False
    dsp: bool = False
    icache: bool = False
    dcache: bool = False
    itcm: bool = False
    dtcm: bool = False
    vtor: bool = True
    num_interrupts: int = 0

    # TODO: sau regions
