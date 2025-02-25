from dataclasses import dataclass, field
from windows_software_analyzer.vulnerability_analyzer import Vulnerability

@dataclass
class SoftwareInfo:
    name: str
    vendor: str
    version: str
    available_version: str
    install_location: str
    install_date: str
    vulnerabilities: list[Vulnerability] = field(default_factory=list)

    def __eq__(self, value: "SoftwareInfo") -> bool:
        return self.name == value.name
    
    def __str__(self) -> str:
        vulnerabilities = "\n".join([str(v) for v in self.vulnerabilities]) if len(self.vulnerabilities) else "-"
        return f"""
    {self.name}:
        vendor - {self.vendor}
        version - {self.version}
        available version - {self.available_version}
        install location - {self.install_location}
        install date - {self.install_date}
        vulnerabilities:
        {vulnerabilities}
    """
