import platform

from scripts.device_info.platforms.available_platforms import AvailablePlatforms
from scripts.device_info.platforms.mac.Darwin import Darwin
from scripts.device_info.platforms.linux.Linux import Linux
from scripts.device_info.platforms.windows.Windows import Windows

if __name__ == '__main__':
    match platform.system():
        case AvailablePlatforms.WINDOWS.value:
            p = Windows()
        case AvailablePlatforms.DARWIN.value:
            p = Darwin()
        case AvailablePlatforms.LINUX.value:
            p = Linux()
        case _:
            raise RuntimeError("Unsupported platform")

    p.print_basic_format()
    p.print_detailed_format()
