from abc import ABC, abstractmethod
import platform
import psutil

from utils_global.console_table.ConsoleTable import ConsoleTable


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

    def prev_print(self):
        for k, v in self.__sys_info.items():
            if isinstance(v, dict):
                print(f'\n{k}')
                for key, val in v.items():
                    print(f'{key}: {val}')
            else:
                print(f'{k}: {v}')

    def print_platform_info(self) -> None:
        headers = ['System', 'Node Name', 'Release', 'Version', 'Machine', 'Processor']
        basic_data = [[self.__sys_info[header] for header in headers]]
        nested_data = {key: value for key, value in self.__sys_info.items() if key not in headers}
        ConsoleTable(basic_data, title="Basic System Info:", headers=headers).display()

        for k, v in nested_data.items():
            if isinstance(v, dict):
                if k == 'Battery':
                    headers = [i for i in v.keys()]
                    data = [[i for i in v.values()]]
                    ConsoleTable(data, title='Battery Info:', headers=headers).display()

                if k == 'Network':
                    data = []
                    for key_item, interface_data in v.items():
                        headers = list(interface_data.keys())
                        interface_row = [key_item] + list(interface_data.values())
                        data.append(interface_row)
                    ConsoleTable(data, title='Network - Interfaces:', headers=['Interface'] + headers).display()

                # TODO: continue from here!!
                if k == 'Network Bandwidth':
                    print('here!')
                    pass

                # for key, val in v.items():
                #     print(f'\n{key}')
                #     if isinstance(val, dict):
                #         for entry_k, entry_v in val.items():
                #             if entry_k == 'Addresses':
                #                 pass
                #             if isinstance(entry_v, list):
                #                 headers.append(entry_k)
                #                 batch.append([str(i) if i is not str else i for i in entry_v])
                #                 ConsoleTable(batch, title=entry_k, headers=headers, layout=Layout.FANCY_OUTLINE).display()
                #                 batch = []
                #                 data = []
                #             else:
                #                 headers.append(entry_k)
                #                 batch.append(str(entry_v))
                #     elif isinstance(val, list):
                #         headers.append(key)
                #         batch.append([str(i) if i is not str else i for i in val])
                #
                #     data.append(batch)
                # ConsoleTable(data, headers=headers, layout=Layout.FANCY_OUTLINE).display()
            else:
                print(f'{k} :=> {v}')

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

        for interface, addresses in net_info.items():
            mac_address = addresses[0].address if len(addresses) > 0 else None
            ipv4_address = addresses[1].address if len(addresses) > 1 else None
            ipv6_address = addresses[2].address if len(addresses) > 2 else None
            self.__sys_info['Network'][interface] = {
                'MAC': mac_address,
                'IPv4': ipv4_address,
                'IPv6': ipv6_address
            }

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
