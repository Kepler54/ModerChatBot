from ast import literal_eval
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStatesGroup(StatesGroup):
    """User state machine"""
    range_value = State()
    add_word = State()


class SystemFiles:
    """Different support functions"""

    @staticmethod
    def help_list() -> str:
        return "Функции пользователя и чата:\n" \
               "\n/start — начало работы\n" \
               "/help — информация\n" \
               "/random — случайное число\n" \
               "/post — активация постов\n" \
               "кубик — игральная кость\n" \
               "\nФункции чата:\n" \
               "\n/word — добавить слово в чс\n" \
               "#ban — забанить кого-то\n"

    @staticmethod
    def obscene_words_answer() -> tuple:
        answer_list = ("А?", "ШО?", "САМ!", "ИЗВИНИСЬ!", "ТЮ МЛЯ!", "ДА ТЫ ШО!")
        return answer_list

    @staticmethod
    def sticker_reading() -> tuple:
        try:
            with open('stickers.spec') as stickers:
                return literal_eval(f'({stickers.read()})')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def sticker_for_post() -> tuple:
        try:
            with open('sticker_for_post.spec') as sticker_for_post:
                return literal_eval(f'({sticker_for_post.read()})')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def conversation_reading() -> dict:
        try:
            with open('conversation.spec', encoding='utf-8') as conversation:
                return literal_eval('{' + conversation.read() + '}')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def conversation_for_post() -> tuple:
        try:
            with open('conversation_for_post.spec', encoding='utf-8') as conversation_for_post:
                return literal_eval(f'({conversation_for_post.read()})')
        except (FileNotFoundError, IndexError):
            pass

    @staticmethod
    def img_format(image) -> str:
        """Format of image delete function"""
        if str(image).endswith("jpeg"):
            return str(image[7:-5])
        return str(image[7:-4])
