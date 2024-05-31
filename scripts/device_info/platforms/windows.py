import subprocess

import psutil
import os
import wmi

from device_info.platforms.generic_platform import GenericPlatform


class Windows(GenericPlatform):
    def get_gpu_info(self):
        def get_gpu_temperature():
            temps = []
            try:
                # Get NVIDIA GPU temperature using NVIDIA-SMI
                res = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], text=True)
                temps = [int(t.strip()) for t in res.splitlines()]
            except (subprocess.CalledProcessError, FileNotFoundError):
                # NVIDIA-SMI not found or no NVIDIA GPU
                try:
                    # Get AMD GPU temperature using ADL (AMD Display Library)
                    if os.path.exists('ADL.exe'):  # Check if ADL.exe exists
                        res = subprocess.check_output(['ADL.exe', 'temperature', 'get', '0'], text=True)
                        temps += [int(t.split('=')[1]) for t in res.splitlines()]
                    else:
                        # Handle the case when ADL.exe is not found
                        print("ADL.exe does not exist. please install ADL to use this")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # ADL not found or no AMD GPU
                    pass

            return temps

        gpu_temps = get_gpu_temperature()
        if gpu_temps:
            for i, temp in enumerate(gpu_temps, 1):
                self.sys_info['GPU'][f'GPU {i}'] = {
                    'Temperature (°C)': temp,
                }
        else:
            self.sys_info['GPU']['No GPU'] = {
                'Temperature (°C)': 'N/A',
            }

    def get_storage_info(self):
        try:
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                self.sys_info['Storage'][disk.DeviceID] = {
                    'Model': disk.Model,
                    'Size (GB)': round(int(disk.Size) / (1024 ** 3), 2),
                }
        except Exception as e:
            print(f'error fetching storage information: {e}')

    def battery_information(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                self.sys_info['Battery']['Percentage'] = f'{battery.percent}%'
                self.sys_info['Battery']['Plugged In'] = 'Yes' if battery.power_plugged else 'No'
        except ImportError:
            pass

    def is_laptop(self):
        try:
            return psutil.sensors_battery()
        except AttributeError:
            return False
