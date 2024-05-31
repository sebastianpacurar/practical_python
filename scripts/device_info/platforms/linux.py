import os
import subprocess

from device_info.platforms.generic_platform import GenericPlatform


class Linux(GenericPlatform):
    def get_gpu_info(self):
        def get_gpu_temperature():
            temps = []
            try:
                # Attempt to get GPU temperature using nvidia-smi (Linux)
                result = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], text=True)
                temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
            except (subprocess.CalledProcessError, FileNotFoundError):
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
            info = subprocess.check_output(['lsblk', '-o', 'NAME,SIZE,MODEL'], text=True).strip().split('\n')[1:]
            for line in info:
                parts = line.strip().split()
                if len(parts) >= 3:
                    device = parts[0]
                    size = parts[1]
                    model = ' '.join(parts[2:])
                    self.sys_info['Storage'][device] = {
                        'Size (GB)': size,
                        'Model': model,
                    }
        except Exception as e:
            print(f'error fetching storage information: {e}')

    def battery_information(self):
        try:
            battery_info = subprocess.check_output(
                ['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], text=True)
            battery_info = battery_info.strip().split('\n')
            for line in battery_info:
                bat_key, bat_val = line.strip().split(': ', 1)
                self.sys_info['Battery'][bat_key] = bat_val
        except subprocess.CalledProcessError:
            pass

    def is_laptop(self):
        return os.path.exists('/sys/class/power_supply/BAT0')
