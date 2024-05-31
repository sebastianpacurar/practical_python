from abc import ABC, abstractmethod
import platform

import psutil


class GenericPlatform(ABC):
    def __init__(self):
        self.sys_info = {
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

    def get_disk_info(self):
        self.sys_info['Disks'] = {}
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            self.sys_info['Disks'][partition.device] = {
                'Mount Point': partition.mountpoint,
                'Total (GB)': round(usage.total / (1024 ** 3), 2),
                'Used (GB)': round(usage.used / (1024 ** 3), 2),
                'Free (GB)': round(usage.free / (1024 ** 3), 2),
                'File System': partition.fstype,
            }

    def get_network_hardware_info(self):
        self.sys_info['Network'] = {}
        net_info = psutil.net_if_addrs()
        for interface, addresses in net_info.items():
            self.sys_info['Network'][interface] = {
                'Addresses': [addr.address for addr in addresses],
            }

    def get_network_bandwidth_info(self):
        self.sys_info['Network Bandwidth'] = {}
        network_interfaces = psutil.net_io_counters(pernic=True)
        for interface, stats in network_interfaces.items():
            self.sys_info['Network Bandwidth'][interface] = {
                'Bytes Sent': stats.bytes_sent,
                'Bytes Received': stats.bytes_recv,
                'Packets Sent': stats.packets_sent,
                'Packets Received': stats.packets_recv,
            }

    @abstractmethod
    def get_gpu_info(self):
        ...

    @abstractmethod
    def get_storage_info(self):
        ...

    @abstractmethod
    def battery_information(self):
        ...

    @abstractmethod
    def is_laptop(self):
        ...
