from dataclasses import dataclass

@dataclass
class Vulnerability:
    id: str
    description: str
    more_info: str


@dataclass
class Software:
    package: str
    version: str
