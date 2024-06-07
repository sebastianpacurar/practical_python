import subprocess
from socket import AddressFamily

import psutil

from scripts.device_info.platforms.GenericPlatform import GenericPlatform
from scripts.device_info.platforms.mac.enums import BatteryInfo


class Darwin(GenericPlatform):
    def get_gpu_info(self) -> None:
        def get_gpu_temperature() -> list[int]:
            temps: list[int] = []
            try:
                # attempt to get GPU temperature using iStats (macOS)
                result: str = subprocess.check_output(['istats', 'extra'], text=True)
                temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
            except (subprocess.CalledProcessError, FileNotFoundError):
                # if iStats didn't work, try using smcFanControl (macOS)
                try:
                    result = subprocess.check_output(['smcFanControl', '-g', 'tsdi'], text=True)
                    temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

            return temps

        gpu_temps: list[int] = get_gpu_temperature()
        if gpu_temps:
            for i, temp in enumerate(gpu_temps, 1):
                self.set_sys_info_entry_key('GPU', f'GPU {i}', {
                    'Temperature (°C)': temp,
                })
        else:
            self.set_sys_info_entry_key('GPU', 'No GPU', {
                'Temperature (°C)': 'N/A',
            })

    def __get_disk_info(self):
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            info = {
                'Mount Point': partition.mountpoint,
                'Total (GB)': round(usage.total / (1024 ** 3), 2),
                'Used (GB)': round(usage.used / (1024 ** 3), 2),
                'Free (GB)': round(usage.free / (1024 ** 3), 2),
                'File System': partition.fstype,
            }

            self.set_sys_info_entry_key('Disks', partition.device, info)

    def get_network_hardware_info(self):
        net_info = psutil.net_if_addrs()
        for interf, addresses in net_info.items():
            info = {
                'MAC': [addr.address for addr in addresses if addr.family.name == AddressFamily.AF_LINK.name],
                'IPv4': [addr.address for addr in addresses if addr.family.name == AddressFamily.AF_INET.name],
                'IPv6': [addr.address for addr in addresses if addr.family.name == AddressFamily.AF_INET6.name]
            }

            for k, v in info.items():
                if isinstance(v, list) and len(v) == 1:
                    info[k] = v[0]
                elif len(v) > 1:
                    info[k] = '\n'.join(v)
                else:
                    info[k] = '-'

            self.set_sys_info_entry_key('Network', interf, info)

    def get_storage_info(self) -> None:
        try:
            info = subprocess.check_output(['diskutil', 'list'], text=True)
            disks = info.strip().split('\n\n')
            for disk in disks:
                lines = disk.strip().split(' ')
                disk_name = lines[0]
                detail_info = subprocess.check_output(['diskutil', 'info', disk_name], text=True)
                details = detail_info.strip().split('\n')
                disk_data = {}
                for detail in details:
                    key_value = detail.split(':')
                    if len(key_value) == 2:
                        key, value = key_value
                        disk_data[key.strip()] = value.strip()

                self.set_sys_info_entry_key('Storage', disk_name, disk_data)

        except Exception as e:
            print(f'Error fetching storage information: {e}')

    def battery_information(self) -> None:
        try:
            # basic info
            battery_info = subprocess.check_output(['pmset', '-g', 'batt'], text=True).strip().split('\n')
            if len(battery_info) >= 2:
                power_source = battery_info[0].strip()
                self.set_sys_info_entry_key('Battery', 'Current Status', power_source)

                battery_status = [status.strip() for status in battery_info[1].strip().split(';')]
                charging_status = battery_status[1]
                time_left = ' '.join(battery_status[2].split(' ')[:1])

                try:
                    int(time_left[0])
                except ValueError:
                    time_left = 'No Estimate'

                self.set_sys_info_entry_key('Battery', 'Charging Status', charging_status)
                self.set_sys_info_entry_key('Battery', 'Time Left', time_left)

            # detailed info
            ioreg_output = subprocess.check_output(["ioreg", "-r", "-c", "AppleSmartBattery"], text=True)
            battery_data = {}
            for line in ioreg_output.split("\n"):
                parts = [part.strip() for part in line.split('=')]
                if len(parts) == 2:
                    key, value = parts
                    battery_data[key.strip('"')] = value.strip()

            if battery_data:
                for i in BatteryInfo:
                    self.set_sys_info_entry_key('Battery', i.name, battery_data.get(i.value, 'Unknown'))
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def is_laptop(self) -> bool:
        try:
            pmset: str = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
            return 'Battery' in pmset
        except subprocess.CalledProcessError:
            return False
