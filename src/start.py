from windows_software_analyzer import Analyzer


if __name__ == "__main__":
    analyzer = Analyzer()
    info = analyzer.analyze()

    print(info)
