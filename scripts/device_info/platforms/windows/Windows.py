import subprocess
import psutil
import os

from device_info.platforms.windows.enums import WmiDiskInfo
from scripts.device_info.platforms.GenericPlatform import GenericPlatform


class Windows(GenericPlatform):
    def get_gpu_info(self) -> None:
        def get_gpu_temperature() -> list[int]:
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

    def get_storage_info(self) -> None:
        try:
            import wmi
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                entry_value = {}
                for info in WmiDiskInfo:
                    entry_value[info.value] = get_disk_attribute(disk, info)
                self.set_sys_info_entry_key('Storage', disk.DeviceID, entry_value)
        except Exception as e:
            raise ValueError(f"Error retrieving storage information: {e}")

    def battery_information(self) -> None:
        try:
            battery = psutil.sensors_battery()
            if battery:
                if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
                    time_left = "Unlimited"
                elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
                    time_left = "Unknown"
                else:
                    hours, remainder = divmod(battery.secsleft, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_left = f"{hours:02}:{minutes:02}:{seconds:02}"

                self.set_sys_info_entry_key('Battery', 'Percentage', f'{battery.percent}%')
                self.set_sys_info_entry_key('Battery', 'Plugged In', 'Yes' if battery.power_plugged else 'No')
                self.set_sys_info_entry_key('Battery', 'Time Left', time_left)
        except ImportError:
            pass

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False


def get_disk_attribute(disk, attribute: WmiDiskInfo):
    # calculate free space, or get the specific disk info
    if attribute == WmiDiskInfo.Size_GB:
        res = round(int(disk.Size) / (1024 ** 3), 2) if disk.Size else 'Unknown'
    else:
        attr_val = getattr(disk, attribute.name, 'Unknown')
        res = '-' if attr_val is None else attr_val
    return res
