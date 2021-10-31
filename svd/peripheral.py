from dataclasses import dataclass, field
from .access import Access
from .protection import Protection
from .address_block import AddressBlock
from .interrupt import Interrupt
from .register import Register


@dataclass
class Peripheral:
    """Represents a device peripheral and its associated registers"""

    # these are required (and sanitized in the parser) but given default values anyway
    name: str = ""
    base_address: int = 0

    # these are optional
    svd_version: str = ""
    description: str = ""
    alternate: str = ""
    group_name: str = ""
    register_prefix: str = ""
    register_suffix: str = ""
    struct_name: str = ""
    disable_condition: str = ""

    # these are optional
    size: int = 0
    default_access: Access = Access.READ_WRITE
    default_protection: Protection = Protection.SECURE
    default_reset_value: int = 0
    reset_mask: int = 0xFFFF
    address_block: AddressBlock = AddressBlock()
    interrupts: [Interrupt] = field(default_factory=list)
    registers: [Register] = field(default_factory=list)
