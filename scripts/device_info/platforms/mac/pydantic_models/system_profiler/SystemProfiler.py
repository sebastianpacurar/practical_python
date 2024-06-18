from enum import Enum

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.SPI import SPSPIDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.Camera import SPCameraDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.Memory import SPMemoryDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.NetworkVolume import SPNetworkVolumeDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.SecureElement import SPSecureElementDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.SoftwareData import SPSoftwareDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.UniversalAccess import SPUniversalAccessDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.simple.IBridge import SPiBridgeDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.nested.Audio import SPAudioDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.nested.Hardware import SPHardwareDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.nested.Storage import SPStorageDataType


class SystemProfiler(Enum):
    # dictionary, more like no nested properties
    SPCameraDataType = SPCameraDataType
    SPiBridgeDataType = SPiBridgeDataType
    SPMemoryDataType = SPMemoryDataType
    SPNetworkVolumeDataType = SPNetworkVolumeDataType
    SPSecureElementDataType = SPSecureElementDataType
    SPSoftwareDataType = SPSoftwareDataType
    SPSPIDataType = SPSPIDataType
    SPUniversalAccessDataType = SPUniversalAccessDataType

    # nested 1 level
    SPAudioDataType = SPAudioDataType
    SPHardwareDataType = SPHardwareDataType
    SPStorageDataType = SPStorageDataType


simple = ['SPUniversalAccessDataType', 'SPSecureElementDataType', 'SPCameraDataType', 'SPiBridgeDataType', 'SPMemoryDataType', 'SPSPIDataType', 'SPSoftwareDataType', 'SPNetworkVolumeDataType']
nested_active = ['SPAudioDataType', 'SPHardwareDataType', 'SPStorageDataType']

# TODO: the below are used for debugging
# base model inherited by other Profiles (all the BaseModels which appear as values in SystemProfiler, above)
long_ones = ['SPApplicationsDataType', 'SPInstallHistoryDataType', 'SPRawCameraDataType']

no_values = ['SPParallelATADataType', 'SPDeveloperToolsDataType', "SPDiagnosticsDataType", "SPDisabledSoftwareDataType",
             "SPDiscBurningDataType", "SPEthernetDataType", "SPFibreChannelDataType", "SPFireWireDataType",
             "SPLegacySoftwareDataType", "SPNetworkLocationDataType", 'SPPCIDataType', 'SPParallelSCSIDataType', 'SPPrefPaneDataType',
             'SPStartupItemDataType', 'SPWWANDataType']

might_not_use = ['SPAirPortDataType', 'SPExtensionsDataType', 'SPFrameworksDataType', 'SPLogsDataType', 'SPPrintersSoftwareDataType',
                 'SPPrintersDataType', 'SPConfigurationProfileDataType', "SPSASDataType", "SPSerialATADataType",
                 'SPSmartCardsDataType', 'SPSyncServicesDataType', 'SPThunderboltDataType']

# simple = ['SPUniversalAccessDataType', 'SPSecureElementDataType', 'SPCameraDataType', 'SPiBridgeDataType',
#           'SPMemoryDataType', 'SPSPIDataType', 'SPSoftwareDataType', 'SPNetworkVolumeDataType']

nested_1 = ['SPAudioDataType', 'SPHardwareDataType', 'SPFirewallDataType', 'SPFontsDataType', 'SPDisplaysDataType',
            'SPManagedClientDataType', 'SPStorageDataType', 'SPUSBDataType']

nested_with_info = ['SPBluetoothDataType', 'SPCardReaderDataType']

# complex = ['SPInternationalDataType', 'SPNVMeDataType', 'SPNetworkDataType', 'SPPowerDataType']
