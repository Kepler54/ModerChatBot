from ast import literal_eval
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStatesGroup(StatesGroup):
    """User state machine"""
    range_value = State()
    add_word = State()
    user_name = State()
    user_message = State()


class SystemFiles:
    """Different support functions"""

    @staticmethod
    def help_list() -> str:
        return "Функции пользователя и чата:\n" \
               "\n/start — начало работы\n" \
               "/help — информация\n" \
               "/random — случайное число\n" \
               "/post — активация постов\n" \
               "/feedback — обратная связь\n" \
               "\nФункции чата:\n" \
               "\n/word — добавить слово в чс\n" \
               "#ban — забанить кого-то\n"

    @staticmethod
    def obscene_words_answer() -> tuple:
        """Bot random answer function"""
        answer_list = ("А?", "Шо?", "Ну ну!", "Извинись!", "Тю мля!", "Да ты шо!", "Тю!", "Парируй!")
        return answer_list

    @staticmethod
    def sticker_reading() -> tuple:
        """Bot answer with sticker in the post"""
        try:
            with open('stickers.spec') as stickers:
                return literal_eval(f'({stickers.read()})')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def sticker_for_post() -> tuple:
        """Bot stickers in the post"""
        try:
            with open('sticker_for_post.spec') as sticker_for_post:
                return literal_eval(f'({sticker_for_post.read()})')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def conversation_reading() -> dict:
        """Bot answer function"""
        try:
            with open('conversation.spec', encoding='utf-8') as conversation:
                return literal_eval('{' + conversation.read() + '}')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def conversation_for_post() -> tuple:
        """Bot conversation in the post"""
        try:
            with open('conversation_for_post.spec', encoding='utf-8') as conversation_for_post:
                return literal_eval(f'({conversation_for_post.read()})')
        except (FileNotFoundError, IndexError):
            pass
