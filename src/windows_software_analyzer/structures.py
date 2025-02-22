from dataclasses import dataclass

from . import software_analyzer, windows_analyzer


@dataclass
class Info:
    windows_info: windows_analyzer.WindowsInfo
    software_info: list[software_analyzer.SoftwareInfo]
