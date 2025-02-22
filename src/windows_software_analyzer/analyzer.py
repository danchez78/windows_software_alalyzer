from . import structures as struct
from . import software_analyzer, windows_analyzer
from .vulnerabilities_analyzer import check_software_for_vulnerabilities, SoftwareForAnalyze


class Analyzer:
    def __init__(self) -> "Analyzer":
        self._software_analyzer = software_analyzer.SoftwareAnalyzer()
        self._windows_analyzer = windows_analyzer.WindowsAnalyzer()

    def analyze(self) -> struct.Info:
        software_info = self._software_analyzer.get_installed_software()
        windows_info = self._windows_analyzer.get_windows_info()

        for software in software_info:
            vulnerabilities = check_software_for_vulnerabilities(SoftwareForAnalyze(package=software.name, version=software.version))

            if vulnerabilities:
                software.vulnerabilities = vulnerabilities

            print(software)

        return struct.Info(
            windows_info=windows_info,
            software_info=software_info,
        )
