from random import randint
from configuration import SystemFiles
from aiogram import Dispatcher, types
from filters import ReplyChatFilter, AdminFilter
from aiogram.utils.exceptions import BotBlocked, CantRestrictSelf, MessageToDeleteNotFound, NetworkError

sf = SystemFiles()
group_id = sf.group_id_reading()


def handlers_register(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        try:
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[1])
            await message.delete()
        except BotBlocked:
            pass

    @dp.message_handler(commands=['help'])
    async def help_me(message: types.Message):
        await message.answer(sf.help_list())
        await message.delete()

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
