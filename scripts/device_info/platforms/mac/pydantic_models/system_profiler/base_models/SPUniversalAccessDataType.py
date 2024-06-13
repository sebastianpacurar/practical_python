from pydantic import BaseModel, Field, ConfigDict


class SPUniversalAccessDataType(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(alias='Name')
    contrast: int = Field(alias='Contrast')
    cursor_mag: str = Field(alias='Cursor Mag')
    display: str = Field(alias='Display')
    flash_screen: str = Field(alias='Flash Screen')
    keyboardZoom: str = Field(alias='Keyboard Zoom')
    mouse_keys: str = Field(alias='Mouse Keys')
    scrollZoom: str = Field(alias='Scroll Zoom')
    slow_keys: str = Field(alias='Slow Keys')
    sticky_keys: str = Field(alias='Sticky Keys')
    voiceover: str = Field(alias='Voiceover')
    zoomMode: str = Field(alias='Zoom Mode')
