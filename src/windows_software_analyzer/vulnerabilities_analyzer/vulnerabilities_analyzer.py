from . import Vulnerability, SoftwareForAnalyze
from . import osv_analyzer, nvd_analyzer


def check_software_for_vulnerabilities(software: SoftwareForAnalyze) -> list[Vulnerability]:
    vulnerabilities = osv_analyzer(software)
    vulnerabilities.extend(nvd_analyzer(software))

    return vulnerabilities