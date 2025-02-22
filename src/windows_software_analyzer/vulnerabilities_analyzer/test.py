from windows_software_analyzer.vulnerabilities_analyzer.structures import SoftwareForAnalyze
from windows_software_analyzer.vulnerabilities_analyzer.vulnerabilities_analyzer import check_software_for_vulnerabilities

soft = SoftwareForAnalyze(package="mruby", version="2.1.2rc")

print(str(check_software_for_vulnerabilities(soft)[0]))