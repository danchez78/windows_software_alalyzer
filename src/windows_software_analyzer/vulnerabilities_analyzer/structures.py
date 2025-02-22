from dataclasses import dataclass

@dataclass
class Vulnerability:
    id: str
    description: str
    more_info: str

    def __str__(self) -> str:
        return """
VULNERABILITY:
    vulnerability_code: {id}
    vulnerability_description: {description}
    more_info: {more_info}
        """.format(id=self.id, description=self.description, more_info=self.more_info)


@dataclass
class SoftwareForAnalyze:
    package: str
    version: str
