from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPSecureElementDataType(BaseModelWithDefault):
    ctl_fw: str | None = Field(alias='Controller Firmware', default=None)
    ctl_hw: str | None = Field(alias='Controller Hardware', default=None)
    ctl_info: str | None = Field(alias='Controller Information', default=None)
    ctl_mw: str | None = Field(alias='Controller Middleware', default=None)
    se_device: str | None = Field(alias='Security Device', default=None)
    se_fw: str | None = Field(alias='Security Firmware', default=None)
    se_hw: str | None = Field(alias='Security Hardware', default=None)
    se_id: str | None = Field(alias='Security Id', default=None)
    se_in_restricted_mode: str | None = Field(alias='Security In Restricted Mode', default=None)
    se_info: str | None = Field(alias='Security Information', default=None)
    se_os_version: str | None = Field(alias='Security Operating System Version', default=None)
    se_plt: str | None = Field(alias='Security Platform', default=None)
