import requests
from .. import SoftwareForAnalyze, Vulnerability


def check_nvd_vulnerabilities(software: SoftwareForAnalyze) -> [Vulnerability]:
    URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    params = {
        "keywordSearch": f"{software.package} {software.version}",
        "resultsPerPage": 5
    }

    response = requests.get(URL, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    raw_vulnerabilities = data.get("vulnerabilities", [])

    if not raw_vulnerabilities:
        return []

    vulnerabilities = []
    for vuln in raw_vulnerabilities:
        vulnerabilities.append(Vulnerability(
            id=vuln["cve"]["id"],
            description=vuln["cve"]["description"][0]["value"],
            more_info=str([ref["url"] for ref in vuln["cve"].get("references", [])])
        ))

    return vulnerabilities
