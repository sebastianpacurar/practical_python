import warnings
from pydantic import Field, BaseModel, ConfigDict

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault

# needed to suppress default values for int types
warnings.filterwarnings('ignore', module='pydantic')


class CoreAudioDevice(BaseModelWithDefault):
    name: str = Field(alias='Name', default='-')
    coreaudio_device_input: int | str = Field(alias='Device Input', default='-')
    coreaudio_device_manufacturer: str = Field(alias='Device Manufacturer', default='-')
    coreaudio_device_output: int | str = Field(alias='Device Output', default='-')
    coreaudio_device_srate: int | str = Field(alias='Device Sound Rate', default='-')
    coreaudio_device_transport: str = Field(alias='Device Transport', default='-')
    coreaudio_input_source: str = Field(alias='Device Input Source', default='-')
    coreaudio_output_source: str = Field(alias='Device Output Source', default='-')
    coreaudio_default_audio_input_device: str = Field(alias='Device Default Audio Input', default='-')
    coreaudio_default_audio_output_device: str = Field(alias='Device Default Audio Output', default='-')
    coreaudio_default_audio_system_device: str = Field(alias='System Device', default='-')
    properties: str = Field(alias='Properties', default='-')


class CoreAudioDevices(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    items: list[CoreAudioDevice] = Field(alias='items', default=list())


class SPAudioDataType(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    audio_items: list[CoreAudioDevice] = Field(alias='audio_items', default=list())
