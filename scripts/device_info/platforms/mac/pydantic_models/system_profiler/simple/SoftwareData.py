from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPSoftwareDataType(BaseModelWithDefault):
    name: str | None = Field(alias='Name', default=None)
    boot_mode: str | None = Field(alias='Boot mode', default=None)
    boot_volume: str | None = Field(alias='Boot volume', default=None)
    kernel_version: str | None = Field(alias='Kernel version', default=None)
    local_host_name: str | None = Field(alias='Local host name', default=None)
    os_version: str | None = Field(alias='Operating system version', default=None)
    secure_vm: str | None = Field(alias='Secure virtual machine', default=None)
    system_integrity: str | None = Field(alias='System integrity', default=None)
    uptime: str | None = Field(alias='Uptime', default=None)
    user_name: str | None = Field(alias='User name', default=None)
