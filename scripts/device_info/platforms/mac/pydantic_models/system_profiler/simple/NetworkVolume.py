from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPNetworkVolumeDataType(BaseModelWithDefault):
    name: str | None = Field(alias='Name')
    spnetworkvolume_automounted: str | None = Field(alias='Auto Mounted', default=None)
    spnetworkvolume_fsmtnonname: str | None = Field(alias='File System Mount name', default=None)
    spnetworkvolume_fstypename: str | None = Field(alias='File System Type name', default=None)
    spnetworkvolume_mntfromname: str | None = Field(alias='Mount From Name', default=None)
