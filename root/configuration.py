from random import randint
from ast import literal_eval


class SystemFiles:

    @staticmethod
    def help_list():
        return "/start — начало работы\n/help — информация\n#ban — забанить кого-то\ndice — кубик"

    @staticmethod
    def answer():
        answer_list = ("А?", "ШО?", "САМ!", "ИЗВИНИСЬ!", "ТЮ БЛЯ!", "ДА ТЫ ШО!")
        return answer_list[randint(0, 5)]

    @staticmethod
    def group_id_reading():
        try:
            with open('group_id.spec', encoding='utf-8') as group_id:
                return literal_eval(group_id.read())
        except FileNotFoundError:
            with open('group_id.spec', 'w') as conversation_write:
                conversation_write.write("''")

    @staticmethod
    def sticker_reading():
        try:
            with open('stickers.spec') as stickers:
                return literal_eval(f'({stickers.read()})')
        except FileNotFoundError:
            with open('stickers.spec', 'w') as stickers_write:
                stickers_write.write("'CAACAgIAAxkBAAEI941kX3KFR0-D7HglAtk3vuBAqKeQDgACawAD9pS1FCzORHN4WTW_LwQ', ")
        except IndexError:
            pass

    @staticmethod
    def conversation_reading():
        try:
            with open('conversation.spec', encoding='utf-8') as conversation:
                return literal_eval('{' + conversation.read() + '}')
        except FileNotFoundError:
            with open('conversation.spec', 'w') as conversation_write:
                conversation_write.write('"хай": "ХАЙ", ')

    @staticmethod
    def obscene_words_reading():
        try:
            with open('obscenewords.spec', encoding='utf-8') as obscene_words:
                return literal_eval(f'({obscene_words.read()})')
        except FileNotFoundError:
            with open('obscenewords.spec', 'w') as obscene_words_write:
                obscene_words_write.write('"хуй", ')
