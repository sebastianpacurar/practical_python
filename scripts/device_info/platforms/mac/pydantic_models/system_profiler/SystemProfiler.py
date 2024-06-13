from enum import Enum

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPSPIDataType import SPSPIDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPCameraDataType import SPCameraDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPMemoryDataType import SPMemoryDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPNetworkVolumeDataType import SPNetworkVolumeDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPSecureElementDataType import SPSecureElementDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPSoftwareDataType import SPSoftwareDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPUniversalAccessDataType import SPUniversalAccessDataType
from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_models.SPiBridgeDataType import SPiBridgeDataType


class SystemProfiler(Enum):
    SPCameraDataType = SPCameraDataType
    SPiBridgeDataType = SPiBridgeDataType
    SPMemoryDataType = SPMemoryDataType
    SPNetworkVolumeDataType = SPNetworkVolumeDataType
    SPSecureElementDataType = SPSecureElementDataType
    SPSoftwareDataType = SPSoftwareDataType
    SPSPIDataType = SPSPIDataType
    SPUniversalAccessDataType = SPUniversalAccessDataType
