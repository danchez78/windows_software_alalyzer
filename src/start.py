from windows_software_analyzer import Analyzer


if __name__ == "__main__":
    analyzer = Analyzer()
    info = analyzer.analyze()

    soft_count = len(info.software_info)

    up_count = 0
    vuln_count = 0
    for soft in info.software_info:
        if soft.vulnerabilities:
            vuln_count += 1

        if soft.available_version:
            up_count += 1

    print(f"""
    Analyzed programs: {soft_count}\n
    Vulnerable programs: {vuln_count}\n
    Programs to update: {up_count}\n
    """)
