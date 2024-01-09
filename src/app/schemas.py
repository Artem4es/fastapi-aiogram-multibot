from enum import Enum

from pydantic import BaseModel, Field


class Status(str, Enum):
    ACTIVATED = "Activated"
    DELETED = "Deleted"
    ERROR = "Error"


class OpenAIEngine(str, Enum):
    GPT_35_TURBO = "gpt-3.5-turbo"


class BaseBotData(BaseModel):
    token: str


class BotData(BaseBotData):
    name: str
    prompt: str = ""
    engine: OpenAIEngine = OpenAIEngine.GPT_35_TURBO
    temperature: float = Field(ge=0, le=1, default=0)


class BotActivateResponse(BaseModel):
    status: Status


class BotDeleteResponse(BaseModel):
    status: Status
