from enum import Enum, auto
from dataclasses import dataclass, field
from .protection import Protection

class SAURegionAccess(Enum):
    NON_SECURE = auto()
    SECURE = auto()

@dataclass
class SAURegion:
    base_address: int = 0
    limit_address: int = 0
    access: SAURegionAccess = SAURegionAccess.SECURE

    # optional
    name: str = ""
    enabled: bool = True
    
@dataclass
class SAURegionConfig:
    enabled: bool = False
    protection: Protection = Protection.SECURE
    sau_regions: [SAURegion] = field(default_factory=list)

