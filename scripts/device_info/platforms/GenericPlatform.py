import psutil
import platform

from abc import ABC, abstractmethod
from socket import AddressFamily

from scripts.utils_global.console_table.ConsoleTable import ConsoleTable


class GenericPlatform(ABC):
    def __init__(self):
        self.__sys_info: dict[str, str | dict] = {
            'System': platform.system(),
            'Node Name': platform.node(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'Disks': {},
            'Storage': {},
            'Battery': {},
            'Network': {},
            'Network Bandwidth': {},
            'GPU': {},
        }
        self.__init_data()

    def set_sys_info_entry_key(self, key: str, entry_key: str, entry_value: str | dict) -> None:
        self.__sys_info.get(key)[entry_key] = entry_value

    def print_basic_format(self):
        for k, v in self.__sys_info.items():
            if isinstance(v, dict):
                print(f'\n{k}')
                for key, val in v.items():
                    print(f'{key}: {val}')
            else:
                print(f'{k}: {v}')

    def print_detailed_format(self) -> None:
        headers = ['System', 'Node Name', 'Release', 'Version', 'Machine', 'Processor']
        basic_data = [[self.__sys_info[header] for header in headers]]
        nested_data = {key: value for key, value in self.__sys_info.items() if key not in headers}
        ConsoleTable(basic_data, title="Basic System Info:", headers=headers).display()

        for k, v in nested_data.items():
            data = []
            if isinstance(v, dict):
                if k in ['Network', 'Network Bandwidth', 'Disks']:
                    for name, description in v.items():
                        headers = ['Interface'] + list(description.keys())
                        data_row = list(description.values())
                        data.append([name] + data_row)
                    ConsoleTable(data, title=f'{k} Info:', headers=headers).display()
                    continue
                if k in ['GPU', 'Storage']:
                    for name, description in v.items():
                        headers = list(description.keys())
                        data_row = [i[0] if isinstance(i, list) else i for i in list(description.values())]
                        data.append([name] + data_row)
                    ConsoleTable(data, title=f'{k} Info:', headers=[k] + headers).display()
                    continue
                if k == 'Battery':
                    headers = [i for i in v.keys()]
                    data = [[i for i in v.values()]]
                    ConsoleTable(data, title=f'{k} Info:', headers=headers).display()
                    continue

    def __init_data(self) -> None:
        self.__get_disk_info()
        self.__get_network_hardware_info()
        self.__get_network_bandwidth_info()
        self.get_gpu_info(),
        self.get_storage_info(),
        if self.is_laptop():
            self.battery_information()

    def __get_disk_info(self):
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            self.__sys_info['Disks'][partition.device] = {
                'Mount Point': partition.mountpoint,
                'Total (GB)': round(usage.total / (1024 ** 3), 2),
                'Used (GB)': round(usage.used / (1024 ** 3), 2),
                'Free (GB)': round(usage.free / (1024 ** 3), 2),
                'File System': partition.fstype,
            }

    def __get_network_hardware_info(self):
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

    def __get_network_bandwidth_info(self):
        network_interfaces = psutil.net_io_counters(pernic=True)
        for interface, stats in network_interfaces.items():
            self.__sys_info['Network Bandwidth'][interface] = {
                'Bytes Sent': stats.bytes_sent,
                'Bytes Received': stats.bytes_recv,
                'Packets Sent': stats.packets_sent,
                'Packets Received': stats.packets_recv,
            }

    @abstractmethod
    def get_gpu_info(self) -> None:
        ...

    @abstractmethod
    def get_storage_info(self) -> None:
        ...

    @abstractmethod
    def battery_information(self) -> None:
        ...

    @abstractmethod
    def is_laptop(self) -> bool:
        ...
