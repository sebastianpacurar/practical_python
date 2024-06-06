import subprocess

from scripts.device_info.platforms.generic_platform import GenericPlatform


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
            battery_info: list[str] = subprocess.check_output(['pmset', '-g', 'batt'], text=True).strip().split('\n')
            if len(battery_info) >= 2:
                power_source: str = battery_info[0].strip()
                self.set_sys_info_entry_key('Battery', 'Power Source', power_source)

                battery_status: list[str] = battery_info[1].strip().split(';')
                if len(battery_status) >= 3:
                    self.set_sys_info_entry_key('Battery', 'Status', battery_status[1].strip())
                    self.set_sys_info_entry_key('Battery', 'Charge', battery_status[2].strip())
        except subprocess.CalledProcessError:
            pass

    def is_laptop(self) -> bool:
        try:
            pmset: str = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
            return 'Battery' in pmset
        except subprocess.CalledProcessError:
            return False
