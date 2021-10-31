from dataclasses import dataclass, field
from .access import Access
from .cpu import CPU
from .protection import Protection
from .peripheral import Peripheral


@dataclass
class Device:
    """Represents an SVD device definition"""

    # these are required (and sanitized in the parser) but given default values anyway
    name: str = ""
    svd_version: str = ""
    width: int = 32
    address_unit_bits: int = 8

    # this is optional
    cpu: CPU = None

    # this is required
    peripherals: [Peripheral] = field(default_factory=list)

    # these are optional
    vendor: str = ""
    vendor_id: str = ""
    series: str = ""
    description: str = ""
    license_text: str = ""
    size: int = 32

    # these are optional
    default_access: Access = Access.READ_WRITE
    default_protection: Protection = Protection.SECURE
    default_reset_value: int = 0
    default_reset_mask: int = 0xFFFF
