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
        return "/start — начало работы\n" \
               "/help — информация\n" \
               "/random — случайное число\n" \
               "/word — добавить слово в чс\n" \
               "#ban — забанить кого-то\n" \
               "кубик — игральная кость"

    @staticmethod
    def obscene_words_answer() -> tuple:
        answer_list = ("А?", "ШО?", "САМ!", "ИЗВИНИСЬ!", "ТЮ МЛЯ!", "ДА ТЫ ШО!")
        return answer_list

    @staticmethod
    def sticker_reading() -> tuple:
        try:
            with open('stickers.spec') as stickers:
                return literal_eval(f'({stickers.read()})')
        except FileNotFoundError:
            with open('stickers.spec', 'w') as stickers_write:
                stickers_write.write("'CAACAgIAAxkBAAEI941kX3KFR0-D7HglAtk3vuBAqKeQDgACawAD9pS1FCzORHN4WTW_LwQ', ")
        except IndexError:
            pass

    @staticmethod
    def conversation_reading() -> dict:
        try:
            with open('conversation.spec', encoding='utf-8') as conversation:
                return literal_eval('{' + conversation.read() + '}')
        except FileNotFoundError:
            with open('conversation.spec', 'w') as conversation_write:
                conversation_write.write('"хай": "ХАЙ", ')
