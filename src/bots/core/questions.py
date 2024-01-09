from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass

from src.bots.exceptions.exceptions import StorageError, AnotherQuestionProcessing


@dataclass(frozen=True)
class DefaultKey:
    bot_id: int
    chat_id: int
    user_id: int


class BasicKeyBuilder(ABC):
    """
    Base class for key builder
    """

    @abstractmethod
    def build(self, key: DefaultKey) -> str:
        """
        This method should be implemented in subclasses
        :return: key to distinguish tg users
        """
        pass


class BasicStorage(ABC):
    """
    Base storage class. Should implement storage container and basic methods
    """

    @abstractmethod
    def in_storage(self, value):
        pass

    @abstractmethod
    def add(self, value):
        pass

    @abstractmethod
    def delete(self, value):
        pass


class QuestionKeyBuilder(BasicKeyBuilder):
    def __init__(self, delimiter: str = ":"):
        self.delimiter = delimiter

    def build(self, key: DefaultKey) -> str:
        key_list = [str(key.bot_id), str(key.chat_id), str(key.user_id)]
        return self.delimiter.join(key_list)


class SetStorage(BasicStorage):
    """Storage based on python set"""

    def __init__(self):
        self.storage = set()

    def in_storage(self, value) -> bool:
        return value in self.storage

    def add(self, value) -> None:
        if value not in self.storage:
            self.storage.add(value)

        else:
            raise StorageError(f"{value} is already in {self.storage}!")

    def delete(self, value) -> None:
        self.storage.remove(value)


class PendingQuestionManager:
    """Base class for pending questions handling"""

    def __init__(self, key_builder: BasicKeyBuilder, storage: BasicStorage):
        self.pending_questions = storage
        self.key_builder = key_builder

    def build_key(self, bot_id: int, chat_id: int, user_id: int) -> str:
        key = DefaultKey(bot_id=bot_id, chat_id=chat_id, user_id=user_id)
        return self.key_builder.build(key)

    def question_pending(self, key: str) -> bool:
        """Check if user already asked something"""
        return self.pending_questions.in_storage(key)

    @contextmanager
    def add_question(self, key: str) -> None:
        """
        Add current question to pending_questions. Question is deleted when answered or error has happened

        """
        try:
            if not self.question_pending(key):
                yield self.pending_questions.add(key)

            else:
                raise AnotherQuestionProcessing("Wait until previous question answered!")

        finally:
            self.remove_question(key)

    def remove_question(self, key: str) -> None:
        if self.pending_questions.in_storage(key):
            self.pending_questions.delete(key)
