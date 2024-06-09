from enum import Enum


class Win32LogicalDisk(Enum):
    Access = 'Access'
    Availability = 'Availability'
    BlockSize = 'Block Size'
    Caption = 'Caption'
    Compressed = 'Compressed'
    ConfigManagerErrorCode = 'Config Manager Error Code'
    ConfigManagerUserConfig = 'Config Manager User Config'
    CreationClassName = 'Creation Class Name'
    Description = 'Description'
    DeviceID = 'Device ID'
    DriveType = 'Drive Type'
    ErrorCleared = 'Error Cleared'
    ErrorDescription = 'Error Description'
    ErrorMethodology = 'Error Methodology'
    FileSystem = 'File System'
    FreeSpace = 'Free Space'
    InstallDate = 'Install Date'
    LastErrorCode = 'Last Error Code'
    MaximumComponentLength = 'Maximum Component Length'
    MediaType = 'Media Type'
    Name = 'Name'
    NumberOfBlocks = 'Number Of Blocks'
    PNPDeviceID = 'PNP Device ID'
    PowerManagementCapabilities = 'Power Management Capabilities'
    PowerManagementSupported = 'Power Management Supported'
    ProviderName = 'Provider Name'
    Purpose = 'Purpose'
    QuotasDisabled = 'Quotas Disabled'
    QuotasIncomplete = 'Quotas Incomplete'
    QuotasRebuilding = 'Quotas Rebuilding'
    Size = 'Size'
    Status = 'Status'
    StatusInfo = 'Status Info'
    SupportsDiskQuotas = 'Supports Disk Quotas'
    SupportsFileBasedCompression = 'Supports File Based Compression'
    SystemCreationClassName = 'System Creation Class Name'
    SystemName = 'System Name'
    VolumeDirty = 'Volume Dirty'
    VolumeName = 'Volume Name'
    VolumeSerialNumber = 'Volume Serial Number'