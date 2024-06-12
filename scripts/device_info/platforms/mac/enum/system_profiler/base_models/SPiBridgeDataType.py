from pydantic import BaseModel, ConfigDict, Field


class SPiBridgeDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ibridge_boot_uuid: str = Field(alias='Boot UUID')
    ibridge_build: str = Field(alias='Build Version')
    ibridge_extra_boot_policies: str = Field(alias='Extra Boot Policies')
    ibridge_model_identifier_top: str = Field(alias='Model Identifier')
    ibridge_sb_boot_args: str = Field(alias='Secure Boot Arguments')
    ibridge_sb_ctrr: str = Field(alias='CTRr Value')
    ibridge_sb_device_mdm: str = Field(alias='Device MDM')
    ibridge_sb_manual_mdm: str = Field(alias='Manual MDM')
    ibridge_sb_other_kext: str = Field(alias='Other Kernel Extensions')
    ibridge_sb_sip: str = Field(alias='System Integrity Protection')
    ibridge_sb_ssv: str = Field(alias='Signed System Volume')
    ibridge_secure_boot: str = Field(alias='Secure Boot')
