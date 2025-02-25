from dataclasses import dataclass


@dataclass
class WindowsInfo:
    version: str
    release: str
    installed_updates: list[str]
    pending_updates: list[str]

    def __str__(self):
        installed_updates = "\n\t".join(self.installed_updates) if len(self.installed_updates) else "-"
        pending_updates = "\n\t".join(self.pending_updates) if len(self.pending_updates) else "-"
        return """
Windows info:
    version - {version}
    release - {release}
    installed updates:
        {installed_updates}
    pending updates:
        {pending_updates}
            """.format(
                version=self.version,
                release=self.release,
                installed_updates=installed_updates,
                pending_updates=pending_updates,
            )
