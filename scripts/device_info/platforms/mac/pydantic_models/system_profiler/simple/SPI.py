from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPSPIDataType(BaseModelWithDefault):
    name: str | None = Field(alias='Name', default=None)
    a_product_id: str | None = Field(alias='Product ID', default=None)
    b_vendor_id: str | None = Field(alias='Vendor ID', default=None)
    c_stfw_version: str | None = Field(alias='ST Firmware Version', default=None)
    d_serial_num: str | None = Field(alias='Serial Number', default=None)
    f_manufacturer: str | None = Field(alias='Manufacturer', default=None)
    g_location_id: str | None = Field(alias='Location ID', default=None)
    h_mtfw_version: str | None = Field(alias='MT Firmware Version', default=None)
