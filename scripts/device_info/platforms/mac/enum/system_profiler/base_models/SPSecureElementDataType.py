from pydantic import BaseModel, Field, ConfigDict

class SPSecureElementDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ctl_fw: str = Field(alias='Controller Firmware')
    ctl_hw: str = Field(alias='Controller Hardware')
    ctl_info: str = Field(alias='Controller Information')
    ctl_mw: str = Field(alias='Controller Middleware')
    se_device: str = Field(alias='Security Device')
    se_fw: str = Field(alias='Security Firmware')
    se_hw: str = Field(alias='Security Hardware')
    se_id: str = Field(alias='Security Id')
    se_in_restricted_mode: str = Field(alias='Security In Restricted Mode')
    se_info: str = Field(alias='Security Information')
    se_os_version: str = Field(alias='Security Operating System Version')
    se_plt: str = Field(alias='Security Platform')
