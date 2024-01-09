from enum import Enum

import openai


class ProcessQuestionError(Exception):
    """Error during ALF GPT request"""


class AnotherQuestionProcessing(Exception):
    """Another question from user is already processing"""


class StorageError(Exception):
    """Value is already in storage"""


class OpenAITextError(str, Enum):
    """OpenAI error phrases"""

    TOKEN_LIMIT_EXCEEDED = "context_length_exceeded"


class OpenAIErrorResolver:
    """Recognize error reason"""

    @classmethod
    def token_limit_exceeded(cls, error: openai.BadRequestError):
        return error.body["code"] == OpenAITextError.TOKEN_LIMIT_EXCEEDED
