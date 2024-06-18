from pydantic import BaseModel, ConfigDict, field_validator


class BaseModelWithDefault(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    @field_validator('*', mode='before', check_fields=False)
    def set_default(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return '-'
        else:
            return v
