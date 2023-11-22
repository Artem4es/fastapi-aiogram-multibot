from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    ACTIVATED = "Activated"
    ERROR = "Error"


class BotData(BaseModel):
    token: str
    assistant_id: int


class BotActivateResponse(BaseModel):
    assistant_id: int
    status: Status
