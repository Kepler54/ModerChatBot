from random import randint
from ast import literal_eval
from aiohttp import ClientOSError
from keyboards import KeyboardRandom
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from configuration import SystemFiles, UserStatesGroup
from filters import ReplyChatFilter, AdminFilter, IntegerFilter
from aiogram.utils.exceptions import BotBlocked, CantRestrictSelf, \
    MessageToDeleteNotFound, NetworkError, MessageNotModified, RetryAfter, \
    MessageCantBeDeleted, BadRequest, Unauthorized, ChatAdminRequired

sf = SystemFiles()
kr = KeyboardRandom()
usg = UserStatesGroup()


def handlers_register(dp: Dispatcher) -> None:
    """Register handlers"""
    dp.filters_factory.bind(AdminFilter)

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message) -> None:
        """Start"""
        await message.bot.send_sticker(message.from_user.id, sticker=sf.sticker_reading()[1])
        await message.bot.send_message(message.from_user.id, sf.help_list())
        await message.delete()

    @dp.message_handler(commands=["help"])
    async def help_me(message: types.Message) -> None:
        """Help"""
        await message.reply(sf.help_list())
        await message.reply("Ответьте хэштегом #ban на сообщение пользователя, которого хотите забанить.")

    @dp.message_handler(commands=["random"])
    async def random_value(message: types.Message) -> None:
        """Random function"""
        await message.reply(
            text="Выбери диапазон генерации случайного числа от 0 и до ...",
            reply_markup=kr.inline_keyboard)
        await usg.range_value.set()
        await message.delete()

    @dp.message_handler(IntegerFilter(), state=usg.range_value)
    async def save_range_value(message: types.Message, state: FSMContext) -> None:
        """Random function"""
        async with state.proxy() as data:
            data["range_value"] = message.text
            await message.reply(text=f'Случайное число: {randint(0, int(data["range_value"]))}')
        await state.finish()

    @dp.message_handler(admin=True, commands=["word"])
    async def word_input(message: types.Message) -> None:
        """Obscene word input function"""
        await message.reply("Введи нежелательное слово...", reply_markup=kr.inline_keyboard)
        await usg.add_word.set()
        await message.delete()

    @dp.message_handler(state=usg.add_word)
    async def word_write(message: types.Message, state: FSMContext) -> None:
        """Obscene word write function"""
        async with state.proxy() as data:
            data["range_value"] = message.text.lower()
            with open(f'chats/{message.chat.id}.spec', 'a') as obscene_words_write:
                obscene_words_write.write(f' "{data["range_value"]}",')
            await message.reply(text="Слово добавлено в чёрный список!")
        await state.finish()
        await message.delete()

    @dp.callback_query_handler(text="close", state="*")
    async def callback_cancel(callback: types.CallbackQuery, state: FSMContext) -> None:
        """Callback cancel function"""
        if state is None:
            return
        await state.finish()
        await callback.message.delete()

    @dp.message_handler(admin=True, commands="ban", commands_prefix="#")
    async def ban(message: types.Message) -> None:
        """Ban function"""
        await message.bot.delete_message(message.chat.id, message.message_id)
        try:
            await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
            await message.reply_to_message.reply("БАН!")
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[0])
        except (CantRestrictSelf, ChatAdminRequired):
            await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
            await message.answer("Я НИ МАГУ ЗАБАНИТЬ САМ СИБЯ! ЭТА КАКОЙ ТА БРЭД!")

    @dp.message_handler(ReplyChatFilter(), content_types="sticker")
    async def sticker_from_user(message: types.Message) -> None:
        """Sticker function"""
        await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])

    @dp.message_handler(ReplyChatFilter(), lambda message: message.text.lower() == "кубик")
    async def dice(message: types.Message) -> None:
        """Dice function"""
        await message.answer_dice()

    @dp.message_handler(ReplyChatFilter())
    async def conversation(message: types.Message) -> None:
        """Conversation function and obscene words filter"""
        for i in sf.conversation_reading():
            if i in message.text.lower():
                await message.reply(sf.conversation_reading()[i])
        counter = 0

        try:
            with open(f'chats/{message.chat.id}.spec', encoding='utf-8') as obscene_words:
                words = literal_eval(f'({obscene_words.read()})')

            for i in words:
                if i in message.text.lower():
                    counter += 1
                    if counter == 1:
                        await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
                        await message.answer(sf.obscene_words_answer()[randint(0, 5)])
                    await message.delete()

        except FileNotFoundError:
            with open(f'chats/{message.chat.id}.spec', 'w') as obscene_words_write:
                obscene_words_write.write('')

        if message.text.lower() == "кто тебя создал?" or message.text.lower() == "кто твой разработчик?" or \
                message.text.lower() == "кто твой создатель?" or message.text.lower() == "кто твой автор?" or \
                message.text.lower() == "кто тебя сделал?" or message.text.lower() == "кто тебя запрограммировал?":
            await message.reply("https://github.com/kepler54")

    @dp.message_handler()
    async def obscene_words_function(message: types.Message) -> None:
        """Obscene words filter"""
        counter = 0

        try:
            with open(f'chats/{message.chat.id}.spec', encoding='utf-8') as obscene_words:
                words = literal_eval(f'({obscene_words.read()})')

            for i in words:
                if i in message.text.lower():
                    counter += 1
                    if counter == 1:
                        await message.bot.send_sticker(message.chat.id, sticker=sf.sticker_reading()[randint(2, 11)])
                        await message.answer(sf.obscene_words_answer()[randint(0, 5)])
                    await message.delete()

        except FileNotFoundError:
            with open(f'chats/{message.chat.id}.spec', 'w') as obscene_words_write:
                obscene_words_write.write('')

    @dp.errors_handler(exception=BotBlocked)
    async def exception_blocked(update: types.update, exception: BotBlocked) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=MessageNotModified)
    async def exception_not_modified(update: types.update, exception: MessageNotModified) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=RetryAfter)
    async def exception_retry_after(update: types.update, exception: RetryAfter) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=MessageToDeleteNotFound)
    async def exception_message_not_found(update: types.update, exception: MessageToDeleteNotFound) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=NetworkError)
    async def exception_network_error(update: types.update, exception: NetworkError) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=AttributeError)
    async def exception_attribute_error(update: types.update, exception: AttributeError) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=ClientOSError)
    async def exception_client_os_error(update: types.update, exception: ClientOSError) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=MessageCantBeDeleted)
    async def message_cant_be_deleted(update: types.update, exception: MessageCantBeDeleted) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=BadRequest)
    async def bad_request(update: types.update, exception: BadRequest) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=Unauthorized)
    async def unauthorized(update: types.update, exception: Unauthorized) -> bool:
        """Exception"""
        return True
