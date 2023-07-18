from aiogram import types
from keyboards import KeyboardClose
from aiogram.dispatcher.filters import BoundFilter

kr = KeyboardClose()


class CreatorAdminFilter(BoundFilter):
    """Filtering of the creator or admin user"""

    key = 'creator'

    def __init__(self, creator):
        self.creator = creator

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


class PrivateMessageFilter(BoundFilter):
    """The message should be only private"""

    async def check(self, message: types.Message) -> bool:
        if message.from_user.id == message.chat.id:
            return True
