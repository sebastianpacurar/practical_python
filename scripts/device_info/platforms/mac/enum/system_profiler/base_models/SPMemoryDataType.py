from pydantic import BaseModel, ConfigDict, Field


class SPMemoryDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dimm_manufacturer: str = Field(alias='DIMM Manufacturer')
    dimm_type: str = Field(alias='DIMM Type')
    SPMemoryDataType: str = Field(alias='DIMM Capacity')
