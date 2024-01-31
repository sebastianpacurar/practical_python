import psutil
import os
import platform
import subprocess
import re

# init sys_info and populate basic platform information
sys_info = {
    'System': platform.system(),
    'Node Name': platform.node(),
    'Release': platform.release(),
    'Version': platform.version(),
    'Machine': platform.machine(),
    'Processor': platform.processor(),
}


# Function to add disk information
def get_disk_info():
    sys_info['Disks'] = {}
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        sys_info['Disks'][partition.device] = {
            'Mount Point': partition.mountpoint,
            'Total (GB)': round(usage.total / (1024 ** 3), 2),
            'Used (GB)': round(usage.used / (1024 ** 3), 2),
            'Free (GB)': round(usage.free / (1024 ** 3), 2),
            'File System': partition.fstype,
        }


def get_gpu_info():
    """ get gpu information """
    sys_info['GPU'] = {}

    def get_gpu_temperature():
        temps = []

        if platform.system() == 'Windows':
            res = None
            try:
                # Get NVIDIA GPU temperature using NVIDIA-SMI
                res = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], text=True)
                temps = [int(t.strip()) for t in res.splitlines()]
            except (subprocess.CalledProcessError, FileNotFoundError):
                # NVIDIA-SMI not found or no NVIDIA GPU
                pass

            if res is None:
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

        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            try:
                # Attempt to get GPU temperature using iStats (macOS) or nvidia-smi (Linux)
                result = subprocess.check_output(['istats', 'extra'], text=True) if platform.system() == 'Darwin' else \
                    subprocess.check_output(
                        ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                        text=True)
                temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

            if not temps and platform.system() == 'Darwin':
                try:
                    # If iStats didn't work, try using smcFanControl (macOS)
                    result = subprocess.check_output(['smcFanControl', '-g', 'tsdi'], text=True)
                    temps = [int(t.split(':')[1].strip()) for t in result.splitlines() if 'GPU' in t]
                except (subprocess.CalledProcessError, FileNotFoundError):
                    pass

        return temps

    gpu_temps = get_gpu_temperature()
    if gpu_temps:
        for i, temp in enumerate(gpu_temps, 1):
            sys_info['GPU'][f'GPU {i}'] = {
                'Temperature (°C)': temp,
            }
    else:
        sys_info['GPU']['No GPU'] = {
            'Temperature (°C)': 'N/A',
        }


def get_storage_info():
    """ Get Storage Info"""
    sys_info['Storage'] = {}

    # Mac
    if platform.system() == 'Darwin':
        try:
            info = subprocess.check_output(['diskutil', 'list'], text=True)
            # Split by empty lines to separate devices
            disks = info.strip().split('\n\n')
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

                sys_info['Storage'][disk_name] = parsed_data
        except Exception as e:
            print(f'Error fetching storage information: {e}')

    # Windows
    elif platform.system() == 'Windows':
        try:
            import wmi
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                sys_info['Storage'][disk.DeviceID] = {
                    'Model': disk.Model,
                    'Size (GB)': round(int(disk.Size) / (1024 ** 3), 2),
                }
        except Exception as e:
            print(f'error fetching storage information: {e}')

    # Linux
    elif platform.system() == 'Linux':
        try:
            info = subprocess.check_output(['lsblk', '-o', 'NAME,SIZE,MODEL'], text=True).strip().split('\n')[1:]
            for line in info:
                parts = line.strip().split()
                if len(parts) >= 3:
                    device = parts[0]
                    size = parts[1]
                    model = ' '.join(parts[2:])
                    sys_info['Storage'][device] = {
                        'Size (GB)': size,
                        'Model': model,
                    }
        except Exception as e:
            print(f'error fetching storage information: {e}')


# Function to add network information
def get_network_hardware_info():
    """get network hardware info"""
    sys_info['Network'] = {}
    net_info = psutil.net_if_addrs()
    for interface, addresses in net_info.items():
        sys_info['Network'][interface] = {
            'Addresses': [addr.address for addr in addresses],
        }


def get_network_bandwidth_info():
    """ get network bandwidth data """
    sys_info['Network Bandwidth'] = {}
    network_interfaces = psutil.net_io_counters(pernic=True)
    for interface, stats in network_interfaces.items():
        sys_info['Network Bandwidth'][interface] = {
            'Bytes Sent': stats.bytes_sent,
            'Bytes Received': stats.bytes_recv,
            'Packets Sent': stats.packets_sent,
            'Packets Received': stats.packets_recv,
        }


def battery_information():
    """ get battery info """
    sys_info['Battery'] = {}

    # get battery info for Windows
    if platform.system() == 'Windows':
        try:
            battery = psutil.sensors_battery()
            if battery:
                sys_info['Battery']['Percentage'] = f'{battery.percent}%'
                sys_info['Battery']['Plugged In'] = 'Yes' if battery.power_plugged else 'No'
        except ImportError:
            pass

    # get battery info for Linux
    elif platform.system() == 'Linux':
        try:
            battery_info = subprocess.check_output(
                ['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], text=True)
            battery_info = battery_info.strip().split('\n')
            for line in battery_info:
                bat_key, bat_val = line.strip().split(': ', 1)
                sys_info['Battery'][bat_key] = bat_val
        except subprocess.CalledProcessError:
            pass

    # get battery info for Mac
    elif platform.system() == 'Darwin':
        try:
            battery_info = subprocess.check_output(['pmset', '-g', 'batt'], text=True).strip().split('\n')
            if len(battery_info) >= 2:
                power_source = battery_info[0].strip()
                sys_info['Battery']['Power Source'] = power_source

                battery_status = battery_info[1].strip().split(';')
                if len(battery_status) >= 3:
                    sys_info['Battery']['Status'] = battery_status[1].strip()
                    sys_info['Battery']['Charge'] = battery_status[2].strip()

        except subprocess.CalledProcessError:
            pass


# used to verify battery status
def is_laptop():
    """ check if device is laptop """
    system = platform.system()

    if system == 'Windows':
        try:
            return psutil.sensors_battery()
        except AttributeError:
            return False

    elif system == 'Linux':
        return os.path.exists('/sys/class/power_supply/BAT0')

    elif system == 'Darwin':
        try:
            pmset = subprocess.check_output(['pmset', '-g', 'batt'], text=True)
            return 'Battery' in pmset
        except subprocess.CalledProcessError:
            return False

    return False


if __name__ == '__main__':
    get_disk_info()
    get_gpu_info()
    get_storage_info()
    get_network_hardware_info()
    get_network_bandwidth_info()

    if is_laptop():
        battery_information()

    for k, v in sys_info.items():
        if isinstance(v, dict):
            print(f'\n{k}')
            for key, value in v.items():
                print(f'{key}: {value}')
        else:
            print(f'{k}: {v}')
