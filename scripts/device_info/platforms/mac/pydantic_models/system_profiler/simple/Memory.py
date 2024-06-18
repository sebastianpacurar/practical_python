from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPMemoryDataType(BaseModelWithDefault):
    dimm_manufacturer: str | None = Field(alias='DIMM Manufacturer', default=None)
    dimm_type: str | None = Field(alias='DIMM Type', default=None)
    SPMemoryDataType: str | None = Field(alias='DIMM Capacity', default=None)
