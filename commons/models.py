from typing import Optional
import dataclasses
import pydantic


class Command(pydantic.BaseModel):
    command: Optional[str] = None
    key: Optional[str] = None
    val: Optional[str] = None
    force: Optional[bool] = False

    @pydantic.field_validator("command")
    def cannot_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("command can not be empty")
        return v


@dataclasses.dataclass
class Config:
    host: Optional[str] = None
    port: Optional[int] = None
    db: Optional[int] = None
    password: Optional[str] = None
    addr: Optional[str] = None
