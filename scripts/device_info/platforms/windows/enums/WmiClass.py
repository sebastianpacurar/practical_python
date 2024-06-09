from enum import Enum

from scripts.device_info.platforms.windows.enums.Win32.Win32DiskPartition import Win32DiskPartition
from scripts.device_info.platforms.windows.enums.Win32.Win32MemoryDevice import Win32MemoryDevice
from scripts.device_info.platforms.windows.enums.Win32.Win32DisplayConfiguration import Win32DisplayConfiguration
from scripts.device_info.platforms.windows.enums.Win32.Win32Keyboard import Win32Keyboard
from scripts.device_info.platforms.windows.enums.Win32.Win32SoundDevice import Win32SoundDevice
from scripts.device_info.platforms.windows.enums.Win32.Win32Desktop import Win32Desktop
from scripts.device_info.platforms.windows.enums.Win32.Win32UsbController import Win32UsbController
from scripts.device_info.platforms.windows.enums.Win32.Win32LogicalDisk import Win32LogicalDisk
from scripts.device_info.platforms.windows.enums.Win32.Win32Fan import Win32Fan
from scripts.device_info.platforms.windows.enums.Win32.Win32MotherboardDevice import Win32MotherboardDevice
from scripts.device_info.platforms.windows.enums.Win32.Win32BaseBoard import Win32BaseBoard
from scripts.device_info.platforms.windows.enums.Win32.Win32Battery import Win32Battery
from scripts.device_info.platforms.windows.enums.Win32.Win32Bios import Win32Bios
from scripts.device_info.platforms.windows.enums.Win32.Win32ComputerSystem import Win32ComputerSystem
from scripts.device_info.platforms.windows.enums.Win32.Win32DiskDrive import Win32DiskDrive
from scripts.device_info.platforms.windows.enums.Win32.Win32NetworkAdapter import Win32NetworkAdapter
from scripts.device_info.platforms.windows.enums.Win32.Win32NetworkAdapterConfiguration import Win32NetworkAdapterConfiguration
from scripts.device_info.platforms.windows.enums.Win32.Win32OperatingSystem import Win32OperatingSystem
from scripts.device_info.platforms.windows.enums.Win32.Win32PhysicalMemory import Win32PhysicalMemory
from scripts.device_info.platforms.windows.enums.Win32.Win32Processor import Win32Processor


class WmiClass(Enum):
    BASEBOARD = ('Win32_BaseBoard', Win32BaseBoard, Win32BaseBoard.Caption.name)
    MOTHERBOARD_DEVICE = ('Win32_MotherboardDevice', Win32MotherboardDevice, Win32MotherboardDevice.Caption.name)
    BATTERY = ('Win32_Battery', Win32Battery, Win32Battery.Caption.name)
    BIOS = ('Win32_Bios', Win32Bios, Win32Bios.Caption.name)
    COMPUTER_SYSTEM = ('Win32_ComputerSystem', Win32ComputerSystem, Win32ComputerSystem.Caption.name)
    DESKTOP = ('Win32_Desktop', Win32Desktop, Win32Desktop.Name.name)
    OPERATING_SYSTEM = ('Win32_OperatingSystem', Win32OperatingSystem, Win32OperatingSystem.Caption.name)
    DISK_DRIVE = ('Win32_DiskDrive', Win32DiskDrive, Win32DiskDrive.Caption.name)
    LOGICAL_DISK = ('Win32_LogicalDisk', Win32LogicalDisk, Win32LogicalDisk.Caption.name)
    DISK_PARTITION = ('Win32_DiskPartition', Win32DiskPartition, Win32DiskPartition.Caption.name)
    PROCESSOR = ('Win32_Processor', Win32Processor, Win32Processor.Caption.name)
    PHYSICAL_MEMORY = ('Win32_PhysicalMemory', Win32PhysicalMemory, Win32PhysicalMemory.DeviceLocator.name)
    MEMORY_DEVICE = ('Win32_MemoryDevice', Win32MemoryDevice, Win32MemoryDevice.DeviceID.name)
    NETWORK_ADAPTER = ('Win32_NetworkAdapter', Win32NetworkAdapter, Win32NetworkAdapter.Caption.name)
    NETWORK_ADAPTER_CONFIG = ('Win32_NetworkAdapterConfiguration', Win32NetworkAdapterConfiguration, Win32NetworkAdapterConfiguration.Caption.name)
    FAN = ('Win32_Fan', Win32Fan, Win32Fan.Caption.name)
    USB_CONTROLLER = ('Win32_USBController', Win32UsbController, Win32UsbController.Caption.name)
    DISPLAY_CONFIGURATION = ('Win32_DisplayConfiguration', Win32DisplayConfiguration, Win32DisplayConfiguration.DeviceName.name)
    KEYBOARD = ('Win32_Keyboard', Win32Keyboard, Win32Keyboard.DeviceID.name)
    SOUND_DEVICE = ('Win32_SoundDevice', Win32SoundDevice, Win32SoundDevice.Caption.name)

    # TODO: issues with format
    # USB_CONTROLLER_DEVICE = ('Win32_USBControllerDevice', Win32UsbControllerDevice, Win32UsbControllerDevice.NegotiatedSpeed.name)