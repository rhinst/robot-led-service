from dataclasses import dataclass

@dataclass
class LED:
    name: str
    pin: int
    state: bool