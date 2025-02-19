from dataclasses import dataclass


@dataclass
class WindowsInfo:
    version: str
    release: str
    installed_updates: list[str]
    pending_updates: list[str]
