from random import randint
from keyboards import KeyboardRandom
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from configuration import SystemFiles, UserStatesGroup
from filters import ReplyChatFilter, AdminFilter, IntegerFilter
from aiogram.utils.exceptions import BotBlocked, CantRestrictSelf, \
    MessageToDeleteNotFound, NetworkError, MessageNotModified, RetryAfter

sf = SystemFiles()
kr = KeyboardRandom()
usg = UserStatesGroup()
group_id = sf.group_id_reading()


def handlers_register(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)

    """Beginning"""

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.bot.send_sticker(message.from_user.id, sticker=sf.sticker_reading()[1])
        await message.bot.send_message(message.from_user.id, sf.help_list())
        await message.delete()

    @dp.message_handler(commands=["help"])
    async def help_me(message: types.Message):
        await message.bot.send_message(message.from_user.id, sf.help_list())
        await message.bot.send_message(
            message.from_user.id,
            "P.S. Ответьте хэштегом #ban на сообщение пользователя, которого хотите забанить."
        )
        await message.delete()

    """Random function"""

    @dp.message_handler(commands=["random"])
    async def random_value(message: types.Message):
        await message.reply(text="Выбери диапазон генерации случайного числа от 0 и до ...")
        await usg.range_value.set()

    @dp.message_handler(IntegerFilter(), state=usg.range_value)
    async def save_range_value(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["range_value"] = message.text
            await message.reply(text=f'Случайное число: {randint(0, int(data["range_value"]))}')
        await state.finish()

    """Callback cancel function"""

    @dp.callback_query_handler(text="cancel", state="*")
    async def callback_cancel(callback: types.CallbackQuery, state: FSMContext):
        if state is None:
            return
        await state.finish()
        await callback.message.delete()

    """Ban function"""

    @dp.message_handler(admin=True, commands="ban", commands_prefix="#")
    async def ban(message: types.Message):
        await message.bot.delete_message(group_id, message.message_id)
        try:
            await message.bot.kick_chat_member(chat_id=group_id, user_id=message.reply_to_message.from_user.id)
            await message.reply_to_message.reply("БАН!")
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[0])
        except CantRestrictSelf:
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
            await message.answer("Я НИ МАГУ ЗАБАНИТЬ САМ СИБЯ! ЭТА КАКОЙ ТА БРЭД!")

    """Other functions"""

    @dp.message_handler(ReplyChatFilter(), content_types="sticker")
    async def sticker_from_user(message: types.Message):
        await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])

    @dp.message_handler(ReplyChatFilter(), lambda message: message.text.lower() == "кубик")
    async def dice(message: types.Message):
        await message.answer_dice()

    """Conversation function and obscene words filter"""

    @dp.message_handler(ReplyChatFilter())
    async def conversation(message: types.Message):
        for i in sf.conversation_reading():
            if i in message.text.lower():
                await message.reply(sf.conversation_reading()[i])
        counter = 0
        for i in sf.obscene_words_reading():
            if i in message.text.lower():
                counter += 1
                if counter == 1:
                    await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
                    await message.answer(sf.obscene_words_answer()[randint(0, 5)])
                await message.delete()

        if message.text.lower() == "кто тебя создал?" or message.text.lower() == "кто твой разработчик?" or \
                message.text.lower() == "кто твой создатель?" or message.text.lower() == "кто твой автор?" or \
                message.text.lower() == "кто тебя сделал?" or message.text.lower() == "кто тебя запрограммировал?":
            await message.reply("https://github.com/kepler54")

    """Obscene words filter"""

    @dp.message_handler()
    async def obscene_words_function(message: types.Message):
        counter = 0
        for i in sf.obscene_words_reading():
            if i in message.text.lower():
                counter += 1
                if counter == 1:
                    await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
                    await message.answer(sf.obscene_words_answer()[randint(0, 5)])
                await message.delete()

    """Exceptions"""

    @dp.errors_handler(exception=BotBlocked)
    async def exception_blocked(update: types.update, exception: BotBlocked):
        return True

    @dp.errors_handler(exception=MessageNotModified)
    async def exception_not_modified(update: types.update, exception: MessageNotModified):
        return True

    @dp.errors_handler(exception=RetryAfter)
    async def exception_retry_after(update: types.update, exception: RetryAfter):
        return True

    @dp.errors_handler(exception=MessageToDeleteNotFound)
    async def exception_message_not_found(update: types.update, exception: MessageToDeleteNotFound):
        return True

    @dp.errors_handler(exception=NetworkError)
    async def exception_network_error(update: types.update, exception: NetworkError):
        return True

    @dp.errors_handler(exception=AttributeError)
    async def exception_attribute_error(update: types.update, exception: AttributeError):
        return True
