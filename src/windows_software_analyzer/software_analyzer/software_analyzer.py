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
        for path in self.__REGISTRY_PATHS:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        software = self._get_software_from_subkey(subkey)
                        if software not in installed_software:
                            installed_software.append(software)
                        else:
                            self._update_software_info(installed_software, software)
                except EnvironmentError:
                    continue
                except WindowsError:
                    continue

        return installed_software
    
    def _get_software_from_subkey(self, subkey: winreg.HKEYType) -> struct.SoftwareInfo:
        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
        display_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
        install_date = winreg.QueryValueEx(subkey, "InstallDate")[0]
        publisher = winreg.QueryValueEx(subkey, "Publisher")[0]

        if not install_location:
            install_location = winreg.QueryValueEx(subkey, "InstallSource")[0]

        return struct.SoftwareInfo(
            name=display_name, 
            vendor=publisher,
            version=display_version,
            available_version="",
            install_location=install_location,
            install_date=install_date,
        )

    @staticmethod
    def _get_list_of_programs() -> list[struct.SoftwareInfo]:
        cmd = 'winget list'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding="utf-8")

        if not result.stdout:
            return ""
        
        software_info: list[struct.SoftwareInfo] = []
        for line in result.stdout.strip().split("\n"):
        # Парсим строки вида: "Google Chrome  Google.Chrome  121.0.6167.184  122.0.6228.0"
            match = re.match(r"(.+?)\s+([\w\.-]+)\s+([\d\.]+)\s+([\d\.]+)?", line)
            if match:
                name, _, installed_version, available_version = match.groups()
                software_info.append(struct.SoftwareInfo(
                    name=name.strip(),
                    vendor="",
                    version=installed_version.strip(),
                    available_version=available_version.strip() if available_version else "",
                    install_location="",
                    install_date="",
                ))

        return software_info
    
    @staticmethod
    def _update_software_info(software_info: list[struct.SoftwareInfo], software: struct.SoftwareInfo) -> list[struct.SoftwareInfo]:
        updated_software = next((s for s in software_info if s.name == software.name), None)
        if updated_software:
            updated_software.vendor = software.vendor
            updated_software.install_location = software.install_location
            updated_software.install_date = software.install_date
