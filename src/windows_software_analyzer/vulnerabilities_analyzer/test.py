from windows_software_analyzer.vulnerabilities_analyzer.structures import Software
from windows_software_analyzer.vulnerabilities_analyzer.vulnerabilities_analyzer import check_software_for_vulnerabilities

soft = Software(package="mruby", version="2.1.2rc")

print(check_software_for_vulnerabilities(soft))