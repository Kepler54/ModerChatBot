from random import randint
from configuration import SystemFiles
from aiogram import Dispatcher, types
from filters import ReplyChatFilter, AdminFilter
from keyboards import KeyboardRandom
from aiogram.utils.exceptions import BotBlocked, CantRestrictSelf, \
    MessageToDeleteNotFound, NetworkError, MessageNotModified, RetryAfter

sf = SystemFiles()
kr = KeyboardRandom()
group_id = sf.group_id_reading()


def handlers_register(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        try:
            await message.bot.send_sticker(message.from_user.id, sticker=sf.sticker_reading()[1])
            await message.bot.send_message(message.from_user.id, sf.help_list())
            await message.delete()
        except BotBlocked:
            pass

    @dp.message_handler(commands=['help'])
    async def help_me(message: types.Message):
        try:
            await message.bot.send_message(message.from_user.id, sf.help_list())
            await message.bot.send_message(
                message.from_user.id,
                "P.S. Ответьте хэштегом #ban на сообщение пользователя, которого хотите забанить."
            )
            await message.delete()
        except BotBlocked:
            pass

    @dp.message_handler(commands=['random'])
    async def random_value(message: types.Message):
        await message.bot.send_message(
            chat_id=message.chat.id, text=f'Случайное число: {randint(0, 100)}', reply_markup=kr.inline_keyboard
        )
        await message.delete()

    @dp.callback_query_handler(text='random')
    async def callback_function(callback: types.CallbackQuery):
        try:
            await callback.message.edit_text(f'Случайное число: {randint(0, 100)}', reply_markup=kr.inline_keyboard)
        except MessageNotModified:
            pass
        except RetryAfter:
            pass

    @dp.callback_query_handler(text='close')
    async def callback_close(callback: types.CallbackQuery):
        await callback.message.delete()

    @dp.message_handler(admin=True, commands='ban', commands_prefix='#')
    async def ban(message: types.Message):
        await message.bot.delete_message(group_id, message.message_id)
        try:
            await message.bot.kick_chat_member(chat_id=group_id, user_id=message.reply_to_message.from_user.id)
            await message.reply_to_message.reply("БАН!")
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[0])
        except CantRestrictSelf:
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
            await message.answer('Я НИ МАГУ ЗАБАНИТЬ САМ СИБЯ! ЭТА КАКОЙ ТА БРЭД!')

    @dp.message_handler(ReplyChatFilter(), content_types='sticker')
    async def sticker_from_user(message: types.Message):
        await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])

    @dp.message_handler(ReplyChatFilter(), lambda message: message.text.lower() == "кубик")
    async def dice(message: types.Message):
        await message.answer_dice()

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
                    await message.answer(sf.answer())
                try:
                    await message.delete()
                except MessageToDeleteNotFound:
                    pass
                except NetworkError:
                    pass

        if message.text.lower() == "кто тебя создал?" or message.text.lower() == "кто твой разработчик?" or \
                message.text.lower() == "кто твой создатель?" or message.text.lower() == "кто твой автор?" or \
                message.text.lower() == "кто тебя сделал?" or message.text.lower() == "кто тебя запрограммировал?":
            await message.reply("https://github.com/kepler54")

    @dp.message_handler()
    async def obscene_words_function(message: types.Message):
        counter = 0
        for i in sf.obscene_words_reading():
            if i in message.text.lower():
                counter += 1
                if counter == 1:
                    await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
                    await message.answer(sf.answer())
                try:
                    await message.delete()
                except MessageToDeleteNotFound:
                    pass
                except NetworkError:
                    pass
