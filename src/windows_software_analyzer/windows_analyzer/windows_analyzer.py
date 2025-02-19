import platform
import subprocess
import win32com.client

from . import structures as struct


class WindowsAnalyzer:
    def get_windows_info(self) -> struct.WindowsInfo:
        installed_updates = self._get_installed_updates()
        pending_updates = self._get_pending_updates()
        return struct.WindowsInfo(
            version=platform.version(),
            release=platform.release(),
            installed_updates=installed_updates,
            pending_updates=pending_updates,
        )

    @staticmethod
    def _get_installed_updates() -> list[str]:
        cmd = 'powershell "Get-HotFix | Select-Object -ExpandProperty HotFixID"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        updates = result.stdout.strip().split("\n")
        return [update.strip() for update in updates if update.strip()]

    @staticmethod
    def _get_pending_updates() -> list[str]:
        session = win32com.client.Dispatch("Microsoft.Update.Session")
        search_result = session.CreateUpdateSearcher().Search("IsInstalled=0 and Type='Software'")
        
        pending_updates  = []
        for update in search_result.Updates:
            if not update.KBArticleIDs.Count:
                continue
            update_kb = "KB" + update.KBArticleIDs[0]
            pending_updates.append(update_kb)
        return pending_updates