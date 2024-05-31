import re
import subprocess

from device_info.platforms.generic_platform import GenericPlatform


class Darwin(GenericPlatform):
    def get_gpu_info(self):
        def get_gpu_temperature():
            temps = []
            try:
                # attempt to get GPU temperature using iStats (macOS)
                result = subprocess.check_output(['istats', 'extra'], text=True)
                temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
            except (subprocess.CalledProcessError, FileNotFoundError):
                # if iStats didn't work, try using smcFanControl (macOS)
                try:
                    result = subprocess.check_output(['smcFanControl', '-g', 'tsdi'], text=True)
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
            info = subprocess.check_output(['diskutil', 'list'], text=True)
            disks = info.strip().split('\n\n') # separate devices
            for disk in disks:
                lines = disk.strip().split('\n')
                disk_name = lines[0].split(':')[0]
                parsed_data = []

                # iterate through subtypes
                for line in lines[2:]:
                    subtype = {}

                    # replace any single whitespaces to underscores, to merge words together, then split
                    line = re.sub(r'(?<=\S) (?=\S)', '_', line).split()

                    if len(line) >= 2:
                        # grab the last 2 elements
                        subtype['Identifier'] = line[-1]
                        subtype['Size'] = line[-2]
                        parsed_data.append(subtype)

                self.sys_info['Storage'][disk_name] = parsed_data
        except Exception as e:
            print(f'Error fetching storage information: {e}')

    def battery_information(self):
        try:
            battery_info = subprocess.check_output(['pmset', '-g', 'batt'], text=True).strip().split('\n')
            if len(battery_info) >= 2:
                power_source = battery_info[0].strip()
                self.sys_info['Battery']['Power Source'] = power_source

                battery_status = battery_info[1].strip().split(';')
                if len(battery_status) >= 3:
                    self.sys_info['Battery']['Status'] = battery_status[1].strip()
                    self.sys_info['Battery']['Charge'] = battery_status[2].strip()

        except subprocess.CalledProcessError:
            pass

    def is_laptop(self):
        try:
            pmset = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
            return 'Battery' in pmset
        except subprocess.CalledProcessError:
            return False
