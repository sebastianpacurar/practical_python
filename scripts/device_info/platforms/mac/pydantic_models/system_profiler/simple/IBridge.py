from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPiBridgeDataType(BaseModelWithDefault):
    ibridge_boot_uuid: str | None = Field(alias='Boot UUID', default=None)
    ibridge_build: str | None = Field(alias='Build Version', default=None)
    ibridge_extra_boot_policies: str | None = Field(alias='Extra Boot Policies', default=None)
    ibridge_model_identifier_top: str | None = Field(alias='Model Identifier', default=None)
    ibridge_sb_boot_args: str | None = Field(alias='Secure Boot Arguments', default=None)
    ibridge_sb_ctrr: str | None = Field(alias='CTRr Value', default=None)
    ibridge_sb_device_mdm: str | None = Field(alias='Device MDM', default=None)
    ibridge_sb_manual_mdm: str | None = Field(alias='Manual MDM', default=None)
    ibridge_sb_other_kext: str | None = Field(alias='Other Kernel Extensions', default=None)
    ibridge_sb_sip: str | None = Field(alias='System Integrity Protection', default=None)
    ibridge_sb_ssv: str | None = Field(alias='Signed System Volume', default=None)
    ibridge_secure_boot: str | None = Field(alias='Secure Boot', default=None)
