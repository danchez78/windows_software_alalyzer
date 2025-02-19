import requests

from .. import Software, Vulnerability


def check_osv_vulnerabilities(software: Software) -> [Vulnerability]:
    URL = "https://api.osv.dev/v1/query"
    PAYLOAD = {
        "package": {
            "name": software.package
        },
        "version": software.version
    }
    VULNERABILITY_KEY = "vulns"

    response = requests.post(URL, json=PAYLOAD)

    if response.status_code != 200:
        pass
        # ERROR

    data = response.json()

    if VULNERABILITY_KEY in data:
        vulnerabilities = []

        for vuln in data[VULNERABILITY_KEY]:
            vulnerabilities += [Vulnerability(
                id=vuln['id'],
                description=vuln.get('summary', 'No'),
                more_info=str(vuln.get('references', 'NO'))
            )]

        return vulnerabilities

    return []