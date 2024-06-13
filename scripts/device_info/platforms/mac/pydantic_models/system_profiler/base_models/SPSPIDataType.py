from pydantic import BaseModel, Field, ConfigDict


class SPSPIDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(alias='Name')
    a_product_id: str = Field(alias='Product ID')
    b_vendor_id: str = Field(alias='Vendor ID')
    c_stfw_version: str = Field(alias='ST Firmware Version')
    d_serial_num: str = Field(alias='Serial Number')
    f_manufacturer: str = Field(alias='Manufacturer')
    g_location_id: str = Field(alias='Location ID')
    h_mtfw_version: str = Field(alias='MT Firmware Version')
