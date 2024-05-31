import platform

from device_info.platforms.available_platforms import AvailablePlatforms
from device_info.platforms.darwin import Darwin
from device_info.platforms.linux import Linux
from device_info.platforms.windows import Windows

if __name__ == '__main__':
    match platform.system():
        case AvailablePlatforms.WINDOWS.value:
            hardware = Windows()
        case AvailablePlatforms.DARWIN.value:
            hardware = Darwin()
        case AvailablePlatforms.LINUX.value:
            hardware = Linux()
        case _:
            raise RuntimeError("Unsupported platform")

    # retrieve hardware information
    hardware.get_disk_info()
    hardware.get_gpu_info()
    hardware.get_storage_info()
    hardware.get_network_hardware_info()
    hardware.get_network_bandwidth_info()

    if hardware.is_laptop():
        hardware.battery_information()

    # display the sys_info data
    for k, v in hardware.sys_info.items():
        if isinstance(v, dict):
            print(f'\n{k}')
            for key, value in v.items():
                print(f'{key}: {value}')
        else:
            print(f'{k}: {v}')
