import subprocess

import psutil
import os

from scripts.device_info.platforms.windows.enums.Win32Bios import Win32Bios
from scripts.device_info.platforms.windows.enums.Win32ComputerSystem import Win32ComputerSystem
from scripts.device_info.platforms.windows.enums.Win32NetworkAdapter import Win32NetworkAdapter
from scripts.device_info.platforms.windows.enums.Win32NetworkAdapterConfiguration import Win32NetworkAdapterConfiguration
from scripts.device_info.platforms.windows.enums.Win32OperatingSystem import Win32OperatingSystem
from scripts.device_info.platforms.windows.enums.Win32DiskDrive import Win32DiskDrive
from scripts.device_info.platforms.windows.enums.Win32Battery import Win32Battery
from scripts.device_info.platforms.windows.enums.Win32PhysicalMemory import Win32PhysicalMemory
from scripts.device_info.platforms.windows.enums.Win32Processor import Win32Processor
from scripts.device_info.platforms.GenericPlatform import GenericPlatform


class Windows(GenericPlatform):
    _wmi = None

    def set_gpu_info(self) -> None:
        def set_gpu_temperature() -> list[int]:
            temps: list[int] = []
            try:
                res: str = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], text=True)
                temps = [int(t.strip()) for t in res.splitlines()]
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    if os.path.exists('ADL.exe'):
                        res = subprocess.check_output(['ADL.exe', 'temperature', 'get', '0'], text=True)
                        temps += [int(t.split('=')[1]) for t in res.splitlines()]
                    else:
                        print("ADL.exe does not exist. please install ADL to use this")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass
            return temps

        gpu_temps: list[int] = set_gpu_temperature()
        if gpu_temps:
            for i, temp in enumerate(gpu_temps, 1):
                self.set_sys_info_entry_key('GPU', f'GPU {i}', {
                    'Temperature (°C)': temp,
                })
        else:
            self.set_sys_info_entry_key('GPU', 'No GPU', {
                'Temperature (°C)': 'N/A',
            })

    def set_platform_sys_data(self):
        if self._wmi is None:
            import wmi
            self._wmi = wmi.WMI()
        self.set_os_sys_info()
        self.set_computer_system_data()
        self.set_disk_drive_info()
        self.set_network_info()
        self.set_network_adapter_config_data()
        self.set_bios_info()
        self.set_processor_data()
        self.set_physical_memory_data()

    def set_processor_data(self):
        try:
            self.add_sys_info_key('Processor Data')
            for win32_processor in self._wmi.Win32_Processor():
                info = {}
                for entry in Win32Processor:
                    info[entry.value] = set_data_attribute(win32_processor, entry)
                self.set_sys_info_entry_key('Processor Data', win32_processor.Name, info)
        except Exception as ex:
            print(ex)

    def set_computer_system_data(self):
        try:
            self.add_sys_info_key('Computer System Data')
            for win32_cs in self._wmi.Win32_ComputerSystem():
                info = {}
                for entry in Win32ComputerSystem:
                    info[entry.value] = set_data_attribute(win32_cs, entry)
                self.set_sys_info_entry_key('Computer System Data', win32_cs.UserName, info)
        except Exception as ex:
            raise ValueError(f'Issue with computer system setting on windows, exception: {ex}')

    def set_physical_memory_data(self):
        try:
            self.add_sys_info_key('Physical Memory Data')
            for win32_processor in self._wmi.Win32_PhysicalMemory():
                info = {}
                for entry in Win32PhysicalMemory:
                    info[entry.value] = set_data_attribute(win32_processor, entry)
                self.set_sys_info_entry_key('Physical Memory Data', win32_processor.Tag, info)
        except Exception as ex:
            print(ex)

    def set_bios_info(self):
        try:
            self.add_sys_info_key('Bios Data')
            for win32_bios in self._wmi.Win32_BIOS():
                info = {}
                for entry in Win32Bios:
                    info[entry.value] = set_data_attribute(win32_bios, entry)
                self.set_sys_info_entry_key('Bios Data', win32_bios.Name, info)
        except Exception as ex:
            print(ex)

    def set_network_info(self):
        try:
            self.add_sys_info_key('Network Adapter')
            for win32_net in self._wmi.Win32_NetworkAdapter():
                info = {}
                for entry in Win32NetworkAdapter:
                    info[entry.value] = set_data_attribute(win32_net, entry)
                self.set_sys_info_entry_key('Network Adapter', win32_net.Name, info)
        except Exception as ex:
            print(ex)

    def set_network_adapter_config_data(self):
        try:
            self.add_sys_info_key('Network Adapter Configuration')
            for win32_net in self._wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                info = {}
                for entry in Win32NetworkAdapterConfiguration:
                    info[entry.value] = set_data_attribute(win32_net, entry)
                self.set_sys_info_entry_key('Network Adapter Configuration', win32_net.Description, info)
        except Exception as ex:
            print(f"Error retrieving network data: {ex}")

    def set_os_sys_info(self):
        try:
            self.add_sys_info_key('Operating System')
            for win32_os in self._wmi.Win32_OperatingSystem():
                info = {}
                for entry in Win32OperatingSystem:
                    info[entry.value] = set_data_attribute(win32_os, entry)

                valid = {k: v for k, v in info.items() if v != '-'}
                self.set_sys_info_entry_key('Operating System', win32_os.CSName, valid)
        except Exception as ex:
            print(ex)

    def set_disk_drive_info(self):
        try:
            self.add_sys_info_key('Disk Drive')
            for win32_disk in self._wmi.Win32_DiskDrive():
                info = {}
                for entry in Win32DiskDrive:
                    info[entry.value] = set_data_attribute(win32_disk, entry)
            self.set_sys_info_entry_key('Disk Drive', win32_disk.Name, info)
        except Exception as ex:
            print(ex)

    def battery_information(self) -> None:
        try:
            self.add_sys_info_key('Battery')
            for win32_battery in self._wmi.Win32_Battery():
                info = {}
                for entry in Win32Battery:
                    info[entry.value] = set_data_attribute(win32_battery, entry)
                self.set_sys_info_entry_key('Disk Drive', win32_battery.DeviceID, info)
        except Exception as ex:
            print(ex)

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False


def set_data_attribute(wmi_entity, attribute):
    if attribute == Win32DiskDrive.Size:
        res = f'{round(int(wmi_entity.Size) / (1024 ** 3), 2)} GB'
    elif attribute == Win32PhysicalMemory.Capacity:
        res = f'{round(int(wmi_entity.Capacity) / (1024 ** 3), 2)} GB'
    else:
        attr_val = getattr(wmi_entity, attribute.name, 'Unknown')
        res = '-' if attr_val is None else attr_val
    return res
