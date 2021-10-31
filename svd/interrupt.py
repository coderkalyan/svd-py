from dataclasses import dataclass


@dataclass
class Interrupt:
    """Interrupt name and value definition for peripheral interrupts"""

    # these are required (and sanitized in the parser) but given default values anyway
    name: str = ""
    value: int = 0

    # these are optional
    description: str = ""
