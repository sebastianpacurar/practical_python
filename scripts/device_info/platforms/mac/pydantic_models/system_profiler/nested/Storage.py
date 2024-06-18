import warnings

from pydantic import BaseModel, Field, ConfigDict, field_validator

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault

# needed to suppress default values for int types
warnings.filterwarnings('ignore', module='pydantic')


class PhysicalDrive(BaseModelWithDefault):
    device_name: str = Field(alias='Device Name', default='-')
    is_internal_disk: str = Field(alias='Is Internal Disk', default='-')
    media_name: str = Field(alias='Media Name', default='-')
    medium_type: str = Field(alias='Medium Type', default='-')
    partition_map_type: str = Field(alias='Partition Map Type', default='-')
    protocol: str = Field(alias='Protocol', default='-')
    smart_status: str = Field(alias='SMART Status', default='-')


class VolumeInfo(BaseModelWithDefault):
    name: str = Field(alias='Name', default='-')
    bsd_name: str = Field(alias='BSD Name', default='-')
    file_system: str = Field(alias='File System', default='-')
    free_space_in_bytes: int | float | str = Field(alias='Free Space in Bytes', default='-')
    ignore_ownership: str = Field(alias='Ignore Ownership', default='-')
    mount_point: str = Field(alias='Mount Point', default='-')
    physical_drive: PhysicalDrive = Field(alias='Physical Drive', default='-')
    size_in_bytes: int | float | str = Field(alias='Size in Bytes', default='-')
    volume_uuid: str = Field(alias='Volume UUID', default='-')
    writable: str = Field(alias='Writable', default='-')

    @field_validator('size_in_bytes', 'free_space_in_bytes', mode='before', check_fields=False)
    def convert_to_gb(cls, value):
        if isinstance(value, int):
            return f'{round(value / (1024 ** 3), 2)} GB'
        return value


class SPStorageDataType(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    volume_items: list[VolumeInfo] = Field(default=list())
