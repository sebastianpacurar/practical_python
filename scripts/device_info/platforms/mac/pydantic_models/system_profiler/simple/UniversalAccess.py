from pydantic import Field

from scripts.device_info.platforms.mac.pydantic_models.system_profiler.base_model import BaseModelWithDefault


class SPUniversalAccessDataType(BaseModelWithDefault):
    name: str | None = Field(alias='Name', default=None)
    contrast: str | None = Field(alias='Contrast', default=None)
    cursor_mag: str | None = Field(alias='Cursor Mag', default=None)
    display: str | None = Field(alias='Display', default=None)
    flash_screen: str | None = Field(alias='Flash Screen', default=None)
    keyboardZoom: str | None = Field(alias='Keyboard Zoom', default=None)
    mouse_keys: str | None = Field(alias='Mouse Keys', default=None)
    scrollZoom: str | None = Field(alias='Scroll Zoom', default=None)
    slow_keys: str | None = Field(alias='Slow Keys', default=None)
    sticky_keys: str | None = Field(alias='Sticky Keys', default=None)
    voiceover: str | None = Field(alias='Voiceover', default=None)
    zoomMode: str | None = Field(alias='Zoom Mode', default=None)
