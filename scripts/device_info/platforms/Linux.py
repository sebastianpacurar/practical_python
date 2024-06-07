import os
import subprocess

from scripts.device_info.platforms.GenericPlatform import GenericPlatform


class Linux(GenericPlatform):
    def get_gpu_info(self) -> None:
        def get_gpu_temperature() -> list[int]:
            temps: list[int] = []
            try:
                # attempt to get GPU temperature using nvidia-smi (Linux)
                result: str = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], text=True)
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

    def get_storage_info(self) -> None:
        try:
            info: list[str] = subprocess.check_output(['lsblk', '-o', 'NAME,SIZE,MODEL'], text=True).strip().split('\n')[1:]
            for line in info:
                parts: list[str] = line.strip().split()
                if len(parts) >= 3:
                    device: str = parts[0]
                    size: str = parts[1]
                    model: str = ' '.join(parts[2:])
                    self.set_sys_info_entry_key('Storage', device, {
                        'Size (GB)': size,
                        'Model': model,
                    })
        except Exception as e:
            print(f'error fetching storage information: {e}')

    def battery_information(self) -> None:
        try:
            battery_info: list[str] = subprocess.check_output(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], text=True).strip().split('\n')
            for line in battery_info:
                bat_key, bat_val = line.strip().split(': ', 1)
                self.set_sys_info_entry_key('Battery', bat_key, bat_val)
        except subprocess.CalledProcessError:
            pass

    def is_laptop(self) -> bool:
        return os.path.exists('/sys/class/power_supply/BAT0')
