from enum import Enum


class BotPhrases(str, Enum):
    TRY_AGAIN = "Что-то пошло не так, попробуйте спросить ещё разок или подождите некоторое время, мы уже чиним!"
    REFRESH_CHAT = "Новый чат активирован, начните диалог"
    START_FIRST = "Нечего чистить. Сперва начните диалог с ботом"
    CONTEXT_CLEANED = "История чата успешно очищена - можно пользоваться дальше"
    CLOSE_TO_CONTEXT_LIMIT = "Скоро лимит истории чата закончится! Очистите историю чата командой /refresh_history \n\n"
    CONTEXT_LIMIT_EXCEEDED = "Вы превысили лимит чата, обновите историю командой /refresh_history"
    WAIT_PREVIOUS_QUESTION = "Пожалуйста дождитесь ответа на предыдущий вопрос!"

    @staticmethod
    def hello(user_name: str) -> str:
        """Hello phrase after changing assistant"""
        return f"Привет, {user_name}! Чем могу помочь?"
