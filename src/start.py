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
    The number of applications that were analyzed: {soft_count}\n
    The number of Vulnerable ones: {vuln_count}\n
    The number of improved ones: {up_count}\n
    """)
