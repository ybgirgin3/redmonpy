from typing import Optional, Union
import dataclasses
import pydantic


class Command(pydantic.BaseModel):
    command: str = None
    key: Optional[str] = None
    val: Optional[str] = None

    @pydantic.field_validator("command")
    def cannot_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("command can not be empty")
        return v


@dataclasses.dataclass
class Config:
    host: str = None
    port: int = None
    db: int = None
    password: str = None
    addr: str = None
