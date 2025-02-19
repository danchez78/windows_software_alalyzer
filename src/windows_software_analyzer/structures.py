from dataclasses import dataclass

from . import software_analyzer, windows_analyzer


@dataclass
class Info:
    windows_info: windows_analyzer.WindowsInfo
    software_info: list[software_analyzer.SoftwareInfo]

    def __str__(self):
        installed_updates = "\n\t".join(self.windows_info.installed_updates) if len(self.windows_info.installed_updates) else "-"
        pending_updates = "\n\t".join(self.windows_info.pending_updates) if len(self.windows_info.pending_updates) else "-"
        software_info = "\n".join([str(s) for s in self.software_info]) if len(self.software_info) else "-"
        return """
Windows info:
    version - {version}
    release - {release}
    installed updates:
        {installed_updates}
    pending updates:
        {pending_updates}
Software info:
{software_info}
            """.format(
                version=self.windows_info.version,
                release=self.windows_info.version,
                installed_updates=installed_updates,
                pending_updates=pending_updates,
                software_info=software_info,
            )