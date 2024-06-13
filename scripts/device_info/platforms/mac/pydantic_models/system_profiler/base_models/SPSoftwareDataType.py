from pydantic import BaseModel, Field, ConfigDict


class SPSoftwareDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(alias='Name')
    boot_mode: str = Field(alias='Boot mode')
    boot_volume: str = Field(alias='Boot volume')
    kernel_version: str = Field(alias='Kernel version')
    local_host_name: str = Field(alias='Local host name')
    os_version: str = Field(alias='Operating system version')
    secure_vm: str = Field(alias='Secure virtual machine')
    system_integrity: str = Field(alias='System integrity')
    uptime: str = Field(alias='Uptime')
    user_name: str = Field(alias='User name')
