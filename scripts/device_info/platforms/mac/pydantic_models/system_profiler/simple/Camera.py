from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPCameraDataType(BaseModelWithDefault):
    name: str | None = Field(alias='Name', default=None)
    spcamera_model_id: str | None = Field(alias='Model ID', default=None)
    spcamera_unique_id: str | None = Field(alias='Unique ID', default=None)
