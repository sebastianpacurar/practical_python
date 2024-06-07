from enum import Enum


class WmiDiskInfo(Enum):
    BytesPerSector = 'Bytes Per Sector'
    Capabilities = 'Capabilities'
    CapabilityDescriptions = 'Capability Descriptions'
    Caption = 'Caption'
    ConfigManagerErrorCode = 'Config Manager Error Code'
    ConfigManagerUserConfig = 'Config Manager User Config'
    CreationClassName = 'Creation ClassName'
    Description = 'Description'
    DeviceID = 'Device ID'
    FirmwareRevision = 'Firmware Revision'
    Index = 'Index'
    InterfaceType = 'Interface Type'
    Manufacturer = 'Manufacturer'
    MediaLoaded = 'Media Loaded'
    MediaType = 'Media Type'
    Model = 'Model'
    Name = 'Name'
    Partitions = 'Partitions'
    PNPDeviceID = 'PNP Device ID'
    SCSIBus = 'SCSI Bus'
    SCSILogicalUnit = 'SCSI Logical Unit'
    SCSIPort = 'SCSI Port'
    SCSITargetId = 'SCSI Target Id'
    SectorsPerTrack = 'Sectors Per Track'
    SerialNumber = 'Serial Number'
    Size_GB = 'Size (GB)'
    Status = 'Status'
    SystemCreationClassName = 'System Creation ClassName'
    SystemName = 'System Name'
    TotalCylinders = 'Total Cylinders'
    TotalHeads = 'Total Heads'
    TotalSectors = 'Total Sectors'
    TotalTracks = 'Total Tracks'
    TracksPerCylinder = 'Tracks Per Cylinder'

    # may not work for all disks
    Availability = 'Availability'
    CompressionMethod = 'Compression Method'
    DefaultBlockSize = 'Default Block Size'
    ErrorCleared = 'Error Cleared'
    ErrorDescription = 'Error Description'
    ErrorMethodology = 'Error Methodology'
    InstallDate = 'Install Date'
    LastErrorCode = 'Last Error Code'
    MaxBlockSize = 'Max Block Size'
    MaxMediaSize = 'Max Media Size'
    MinBlockSize = 'Min Block Size'
    NeedsCleaning = 'Needs Cleaning'
    NumberOfMediaSupported = 'Number Of Media Supported'
    PowerManagementCapabilities = 'Power Management Capabilities'
    PowerManagementSupported = 'Power Management Supported'
    Signature = 'Signature'
    StatusInfo = 'Status Info'
