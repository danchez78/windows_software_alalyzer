from . import Vulnerability, Software
from . import osv_analyzer


def check_software_for_vulnerabilities(software: Software) -> list[Vulnerability]:
    vulnerabilities = osv_analyzer(software)

    return vulnerabilities