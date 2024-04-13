from typing import Optional, Union
import dataclasses
import pydantic


class Command(pydantic.BaseModel):
    command: str
    limit: Optional[Union[str, int]] = 10

    @pydantic.field_validator("command")
    def cannot_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("command can not be empty")
        return v


@dataclasses.dataclass
class Config:
    host: str
    port: int
    db: int
    password: str
