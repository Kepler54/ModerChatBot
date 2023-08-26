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
        return "<b>Функции чата и пользователя:</b>\n" \
               "\n<em>/start — начало работы</em>\n" \
               "<em>/help — информация</em>\n" \
               "<em>/random — случайное число</em>\n" \
               "\n<em>кубик — игральная кость</em>\n" \
               "<em>аудио — случайное аудио</em>\n" \
               "\n<b>Функции админа или создателя чата:</b>\n" \
               "\n<em>/word — добавить слово в чс</em>\n" \
               "<em>/post — активация постов</em>\n" \
               "<em>/stop — деактивация постов</em>\n" \
               "<em>/ban — забанить кого-то</em>\n" \
               "\nОтветь командой /ban на сообщение пользователя, которого хочешь забанить\n" \
               "\n<b>Функции пользователя:</b>\n" \
               "\n<em>/feedback — обратная связь</em>\n" \
               "\n<b>Поддержать автора в Bitcoin:</b>\n" \
               "\nbc1qewfgtrrg2gqgtvzl5d2pr9pte685pp5n3g6scy"

    @staticmethod
    def obscene_words_answer() -> tuple:
        """Bot random answer function"""
        answer_list = ("А?", "Шо?", "Каво?!", "Извинись!", "Тю мля!", "Да ты шо!", "Тю!", "Парируй!")
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
