from dataclasses import dataclass


@dataclass
class SoftwareInfo:
    name: str
    vendor: str
    version: str
    available_version: str
    install_location: str
    install_date: str

    def __eq__(self, value: "SoftwareInfo") -> bool:
        return self.name == value.name
    
    def __str__(self) -> str:
        return f"""
    {self.name}:
        vendor - {self.vendor}
        version - {self.version}
        available version - {self.available_version}
        install location - {self.install_location}
        install date - {self.install_date}
    """
