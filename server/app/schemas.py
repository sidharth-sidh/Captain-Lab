from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Status = Literal["online", "offline"]


class ComputerRegister(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    hostname: str = Field(min_length=1, max_length=255)
    ip_address: str | None = Field(default=None, max_length=45)
    operating_system: str = Field(min_length=1, max_length=100)
    os_version: str = Field(min_length=1, max_length=100)
    username: str | None = Field(default=None, max_length=255)
    agent_version: str | None = Field(default=None, max_length=50)


class ComputerHeartbeat(BaseModel):
    ip_address: str | None = Field(default=None, max_length=45)
    username: str | None = Field(default=None, max_length=255)
    agent_version: str | None = Field(default=None, max_length=50)


class ComputerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    hostname: str
    ip_address: str | None
    operating_system: str
    os_version: str
    status: Status
    username: str | None
    last_seen: datetime | None
    agent_version: str | None
    created_at: datetime
    updated_at: datetime
