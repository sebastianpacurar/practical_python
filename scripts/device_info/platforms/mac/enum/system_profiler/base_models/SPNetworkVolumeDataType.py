from pydantic import BaseModel, Field, ConfigDict


class SPNetworkVolumeDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(alias='Name')
    spnetworkvolume_automounted: str = Field(alias='Auto Mounted')
    spnetworkvolume_fsmtnonname: str = Field(alias='File System Mount name')
    spnetworkvolume_fstypename: str = Field(alias='File System Type name')
    spnetworkvolume_mntfromname: str = Field(alias='Mount From Name')
