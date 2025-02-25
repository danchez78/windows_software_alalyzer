import winreg
import subprocess
import re

from . import structures as struct

class SoftwareAnalyzer:
    __REGISTRY_PATHS = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    def get_installed_software(self) -> list[struct.SoftwareInfo]:
        installed_software: list[struct.SoftwareInfo] = self._get_list_of_programs()

        software_info: list[struct.SoftwareInfo] = []
        for path in self.__REGISTRY_PATHS:
            software_info.extend(self._get_software_by_key_and_path(winreg.HKEY_LOCAL_MACHINE, path))
        for path in self._get_hkey_users_paths():
            software_info.extend(self._get_software_by_key_and_path(winreg.HKEY_USERS, path))
        for software in software_info:
            if software not in installed_software:
                installed_software.append(software)
            else:
                self._update_software_info(installed_software, software)
        return installed_software
    
    def _get_software_by_key_and_path(self, key_type, path) -> list[struct.SoftwareInfo]:
        software_list = []
        try:
            key = winreg.OpenKey(key_type, path)
        except EnvironmentError:
            return software_list

        for i in range(0, winreg.QueryInfoKey(key)[0]):
            try:
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                   software = self._get_software_from_subkey(subkey)
                   if software.name:
                    software_list.append(software)
            except EnvironmentError:
                continue
            except WindowsError:
                continue
        return software_list

    def _get_software_from_subkey(self, subkey: winreg.HKEYType) -> struct.SoftwareInfo:
        keys = ["DisplayName", "DisplayVersion", "InstallLocation", "InstallDate", "Publisher"]
        
        results = {}
        for key in keys:
            try:
                res = winreg.QueryValueEx(subkey, key)[0]
                results[key] = res
            except EnvironmentError:
                results[key] = ""

        return struct.SoftwareInfo(
            name=results["DisplayName"], 
            vendor=results["Publisher"],
            version=results["DisplayVersion"],
            available_version="",
            install_location=results["InstallLocation"],
            install_date=results["InstallDate"],
        )

    @staticmethod
    def _get_list_of_programs() -> list[struct.SoftwareInfo]:
        cmd = 'winget list'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding="utf-8")

        if not result.stdout:
            return ""
        
        pattern = r"(.+?)\s{2,}([\w\.-]+)\s{2,}([\d\.]+)(?:\s{2,}([\d\.]+))?\s+(winget)$"
        
        software_info: list[struct.SoftwareInfo] = []
        for line in result.stdout.strip().split("\n"):
            match = re.match(pattern, line)
            if match:
                name = match.group(1).strip()
                version_current = match.group(3).strip()
                version_latest = match.group(4).strip() if match.group(4) else "N/A"
            else:
                continue

            if "ARP\\" in name:
                name = " ".join(name.split(" ")[:-1]).strip()

            software_info.append(struct.SoftwareInfo(
                name=name,
                vendor="",
                version=version_current.strip(),
                available_version=version_latest,
                install_location="",
                install_date="",
            ))

        return software_info
    
    @staticmethod
    def _update_software_info(software_info: list[struct.SoftwareInfo], software: struct.SoftwareInfo) -> list[struct.SoftwareInfo]:
        updated_software = next((s for s in software_info if s.name == software.name), None)
        if updated_software:
            if not updated_software.vendor:
                updated_software.vendor = software.vendor
            if not updated_software.install_location: 
                updated_software.install_location = software.install_location
            if not updated_software.install_date: 
                updated_software.install_date = software.install_date

    def _get_hkey_users_paths(self) -> list[str]:
        paths: list[str] = []
        with winreg.OpenKey(winreg.HKEY_USERS, "") as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                sid = winreg.EnumKey(key, i)
                for path in self.__REGISTRY_PATHS:
                    hkey_path = sid + "\\" + path
                    paths.append(hkey_path)

        return paths
