from pydantic import BaseModel, Field, ConfigDict

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class HardwareInfo(BaseModelWithDefault):
    name: str = Field(alias='Name', default='-')
    activation_lock_status: str = Field(alias='Activation Lock Status', default='-')
    boot_rom_version: str = Field(alias='Boot ROM', default='-')
    chip_type: str = Field(alias='Chip Type', default='-')
    machine_model: str = Field(alias='Machine Model', default='-')
    machine_name: str = Field(alias='Machine Name', default='-')
    model_number: str = Field(alias='Model Number', default='-')
    number_processors: str = Field(alias='Processors', default='-')
    os_loader_version: str = Field(alias='OS Loader Version', default='-')
    physical_memory: str = Field(alias='Physical Memory', default='-')
    platform_UUID: str = Field(alias='Platform UUID', default='-')
    provisioning_UDID: str = Field(alias='Provisioning UDID', default='-')
    serial_number: str = Field(alias='Serial Number', default='-')


class SPHardwareDataType(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    hardware_items: list[HardwareInfo] = Field(default=list())
