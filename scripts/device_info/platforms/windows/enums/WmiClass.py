from enum import Enum

from scripts.device_info.platforms.windows.enums.Win32.Win32NetworkProtocol import Win32NetworkProtocol
from scripts.device_info.platforms.windows.enums.Win32.Win32OSRecoveryConfiguration import Win32OSRecoveryConfiguration
from scripts.device_info.platforms.windows.enums.Win32.Win32PnP import Win32PnP
from scripts.device_info.platforms.windows.enums.Win32.Win32PortableBattery import Win32PortableBattery
from scripts.device_info.platforms.windows.enums.Win32.Win32VoltageProbe import Win32VoltageProbe
from scripts.device_info.platforms.windows.enums.Win32.Win32NetworkClient import Win32NetworkClient
from scripts.device_info.platforms.windows.enums.Win32.Win32Volume import Win32Volume
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
    """
    Enum representing various WMI classes used for system information retrieval on Windows.

    Each enum entry consists of:
    - Class Name: The name of the WMI class as per the WMI namespace.
    - Python Class: The corresponding Python class used for handling data from this WMI class.
    - Table Row ID: The specific row used to differentiate multiple entries (acts as an ID of the table, and is the first column).
    """
    BASEBOARD = ('Win32_BaseBoard', Win32BaseBoard, Win32BaseBoard.Caption.name)
    MOTHERBOARD_DEVICE = ('Win32_MotherboardDevice', Win32MotherboardDevice, Win32MotherboardDevice.Caption.name)
    BATTERY = ('Win32_Battery', Win32Battery, Win32Battery.Caption.name)
    PORTABLE_BATTERY = ('Win32_PortableBattery', Win32PortableBattery, Win32PortableBattery.Caption.name)
    BIOS = ('Win32_Bios', Win32Bios, Win32Bios.Caption.name)
    COMPUTER_SYSTEM = ('Win32_ComputerSystem', Win32ComputerSystem, Win32ComputerSystem.Caption.name)
    DESKTOP = ('Win32_Desktop', Win32Desktop, Win32Desktop.Name.name)
    OPERATING_SYSTEM = ('Win32_OperatingSystem', Win32OperatingSystem, Win32OperatingSystem.Caption.name)
    DISK_DRIVE = ('Win32_DiskDrive', Win32DiskDrive, Win32DiskDrive.Caption.name)
    LOGICAL_DISK = ('Win32_LogicalDisk', Win32LogicalDisk, Win32LogicalDisk.Caption.name)
    DISK_PARTITION = ('Win32_DiskPartition', Win32DiskPartition, Win32DiskPartition.Caption.name)
    VOLUME = ('Win32_Volume', Win32Volume, Win32Volume.Caption.name)
    PROCESSOR = ('Win32_Processor', Win32Processor, Win32Processor.Caption.name)
    PHYSICAL_MEMORY = ('Win32_PhysicalMemory', Win32PhysicalMemory, Win32PhysicalMemory.DeviceLocator.name)
    MEMORY_DEVICE = ('Win32_MemoryDevice', Win32MemoryDevice, Win32MemoryDevice.DeviceID.name)
    NETWORK_ADAPTER = ('Win32_NetworkAdapter', Win32NetworkAdapter, Win32NetworkAdapter.Caption.name)
    NETWORK_ADAPTER_CONFIG = ('Win32_NetworkAdapterConfiguration', Win32NetworkAdapterConfiguration, Win32NetworkAdapterConfiguration.Caption.name)
    NETWORK_CLIENT = ('Win32_NetworkClient', Win32NetworkClient, Win32NetworkClient.Caption.name)
    NETWORK_PROTOCOL = ('Win32_NetworkProtocol', Win32NetworkProtocol, Win32NetworkProtocol.Caption.name)
    FAN = ('Win32_Fan', Win32Fan, Win32Fan.Caption.name)
    USB_CONTROLLER = ('Win32_USBController', Win32UsbController, Win32UsbController.Caption.name)
    DISPLAY_CONFIGURATION = ('Win32_DisplayConfiguration', Win32DisplayConfiguration, Win32DisplayConfiguration.DeviceName.name)
    KEYBOARD = ('Win32_Keyboard', Win32Keyboard, Win32Keyboard.DeviceID.name)
    SOUND_DEVICE = ('Win32_SoundDevice', Win32SoundDevice, Win32SoundDevice.Caption.name)
    VOLTAGE_PROBE = ('Win32_VoltageProbe', Win32VoltageProbe, Win32VoltageProbe.Caption.name)
    RECOVERY_CONFIGURATION = ('Win32_OSRecoveryConfiguration', Win32OSRecoveryConfiguration, Win32OSRecoveryConfiguration.Name.name)
    PLUG_AND_PLAY = ('Win32_PnPEntity', Win32PnP, Win32PnP.Caption.name)

# TODO: issues with format
# USB_CONTROLLER_DEVICE = ('Win32_USBControllerDevice', Win32UsbControllerDevice, Win32UsbControllerDevice.NegotiatedSpeed.name)
