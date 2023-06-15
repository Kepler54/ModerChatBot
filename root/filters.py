from aiogram import types
from keyboards import KeyboardRandom
from aiogram.dispatcher.filters import BoundFilter

kr = KeyboardRandom()


class AdminFilter(BoundFilter):
    """Filtering of the admin user"""
    key = 'admin'

    def __init__(self, admin):
        self.admin = admin

    async def check(self, message: types.Message) -> object:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


class ReplyChatFilter(BoundFilter):
    """Filtering bot responses to messages"""

    async def check(self, message: types.Message) -> bool:
        try:
            if message.from_user.id != message.chat.id:
                if message.reply_to_message.from_user.id == message.bot.id:
                    return True
            else:
                if message.from_user.id == message.chat.id:
                    return True
        except AttributeError:
            pass


class IntegerFilter(BoundFilter):
    """Filtering of integers"""

    async def check(self, message: types.Message) -> bool:
        try:
            if int(message.text):
                return True
        except ValueError:
            await message.reply(
                text=f'"{message.text}" — НЕ ЩИТАИТСЯ! НУЖНО ВВЕСТИ ЦЕЛОЕ ЧИСЛО!',
                reply_markup=kr.inline_keyboard
            )
