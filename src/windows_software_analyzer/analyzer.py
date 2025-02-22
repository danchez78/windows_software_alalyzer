from . import structures as struct
from . import software_analyzer, windows_analyzer, vulnerability_analyzer


class Analyzer:
    def __init__(self) -> "Analyzer":
        self._software_analyzer = software_analyzer.SoftwareAnalyzer()
        self._windows_analyzer = windows_analyzer.WindowsAnalyzer()
        self._vulnerability_analyzer = vulnerability_analyzer.VulnerabilityAnalyzer()

    def analyze(self) -> struct.Info:
        software_info = self._software_analyzer.get_installed_software()
        windows_info = self._windows_analyzer.get_windows_info()

        print(windows_info)

        for software in software_info:
            vulnerabilities = self._vulnerability_analyzer.analyze(
                vulnerability_analyzer.SoftwareForAnalyze(package=software.name, version=software.version)
                )

            if vulnerabilities:
                software.vulnerabilities = vulnerabilities

            print(software)

        return struct.Info(
            windows_info=windows_info,
            software_info=software_info,
        )
