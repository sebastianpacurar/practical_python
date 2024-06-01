import subprocess
import psutil
import os
import wmi

from device_info.platforms.generic_platform import GenericPlatform


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
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                self.set_sys_info_entry_key('Storage', disk.DeviceID, {
                    'Model': disk.Model,
                    'Size (GB)': round(int(disk.Size) / (1024 ** 3), 2),
                })
        except Exception as e:
            print(f'error fetching storage information: {e}')

    def battery_information(self) -> None:
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.set_sys_info_entry_key('Battery', 'Percentage', f'{battery.percent}%')
                self.set_sys_info_entry_key('Battery', 'Plugged In', 'Yes' if battery.power_plugged else 'No')
        except ImportError:
            pass

    def is_laptop(self) -> bool:
        try:
            return psutil.sensors_battery() is not None
        except AttributeError:
            return False
