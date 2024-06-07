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

    def get_disk_info(self):
        try:
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines[1:]:
                fs, size, used, avail, percentage, mountpoint = line.split()
                disk_info = {
                    'Mountpoint': mountpoint,
                    'Total': size,
                    'Used': used,
                    'Free': avail,
                    'Percentage': percentage,
                }

                self.set_sys_info_entry_key('Disks', fs, disk_info)
        except Exception as e:
            raise ValueError(f"Error retrieving disk information: {e}")

    def get_network_hardware_info(self):
        result = subprocess.run(['ip', '-c', 'addr'], capture_output=True, text=True)
        output_lines = result.stdout.strip().split('\n\n')

        network_info = {}
        for interface_info in output_lines:
            lines = interface_info.split('\n')
            interface_name = lines[0].split(':')[1].strip()
            mac_address = lines[1].split()[1]
            ipv4_addresses = []
            ipv6_addresses = []

            for line in lines[1:]:
                if 'inet ' in line:
                    ipv4_addresses.append(line.split()[1].split('/')[0])
                elif 'inet6 ' in line:
                    ipv6_addresses.append(line.split()[1].split('/')[0])

            data = {
                'MAC': mac_address,
                'IPv4': '\n'.join(ipv4_addresses) if ipv4_addresses else '-',
                'IPv6': '\n'.join(ipv6_addresses) if ipv6_addresses else '-'
            }

            self.set_sys_info_entry_key('Network', interface_name, data)
        return network_info

    def get_storage_info(self):
        try:
            result = subprocess.run(['lsblk', '-J', '--output', 'NAME,MOUNTPOINT,SIZE,ROTA,FSTYPE,MODEL,SERIAL,VENDOR'], capture_output=True, text=True)
            if result.returncode == 0:
                storage_info = result.stdout.strip()
                # Process storage_info as needed
                return storage_info
            else:
                raise ValueError(f"Error retrieving storage information: {result.stderr}")
        except Exception as e:
            raise ValueError(f"Error retrieving storage information: {e}")

    def battery_information(self) -> None:
        try:
            battery_info: list[str] = subprocess.check_output(
                ['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], text=True).strip().split('\n')
            for line in battery_info:
                bat_key, bat_val = line.strip().split(': ', 1)
                self.set_sys_info_entry_key('Battery', bat_key, bat_val)
        except subprocess.CalledProcessError:
            pass

    def is_laptop(self) -> bool:
        return os.path.exists('/sys/class/power_supply/BAT0')
