from pydantic import BaseModel, Field, ConfigDict


class SPCameraDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(alias='Name')
    spcamera_model_id: str = Field(alias='Model ID')
    spcamera_unique_id: str = Field(alias='Unique ID')
