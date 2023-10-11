from os import listdir
from pathlib import Path
from asyncio import sleep
from ast import literal_eval
from aiohttp import ClientOSError
from random import randint, choice
from sqlite import DataBaseFeedback
from keyboards import KeyboardClose
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from asyncio.exceptions import TimeoutError
from configuration import SystemFiles, UserStatesGroup
from filters import ReplyChatFilter, CreatorAdminFilter, \
    IntegerFilter, PrivateMessageFilter, ChatMessageFilter, MemberFilter
from aiogram.utils.exceptions import BotBlocked, CantRestrictSelf, MessageToDeleteNotFound, NetworkError, \
    MessageNotModified, RetryAfter, MessageCantBeDeleted, BadRequest, Unauthorized, ChatAdminRequired, TelegramAPIError

sf = SystemFiles()
kr = KeyboardClose()
usg = UserStatesGroup()
dbf = DataBaseFeedback()

switch = True
sticker_list = []
image_list = []
conversation_list = []
audio_list = []


def handlers_register(dp: Dispatcher) -> None:
    """Register handlers"""
    dp.filters_factory.bind(CreatorAdminFilter)
    dp.filters_factory.bind(MemberFilter)

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message) -> None:
        """Start"""
        try:
            await message.bot.send_sticker(message.from_user.id, sticker=sf.sticker_reading()[1])
        except IndexError:
            pass
        await message.bot.send_message(
            message.from_user.id,
            sf.help_list(),
            parse_mode="HTML",
            disable_notification=True
        )
        await message.delete()

    @dp.message_handler(commands=["help"])
    async def help_me(message: types.Message) -> None:
        """Help"""
        await message.bot.send_message(
            message.chat.id,
            sf.help_list(),
            parse_mode="HTML",
            disable_notification=True
        )
        await message.delete()

    @dp.message_handler(commands=["random"])
    async def random_value(message: types.Message) -> None:
        """Random function"""
        await message.bot.send_message(
            message.chat.id,
            text="Выбери диапазон генерации случайного числа от 0 и до ...",
            disable_notification=True,
            reply_markup=kr.inline_keyboard)
        await usg.range_value.set()
        await message.delete()

    @dp.message_handler(IntegerFilter(), state=usg.range_value)
    async def save_range_value(message: types.Message, state: FSMContext) -> None:
        """Random function"""
        async with state.proxy() as data:
            data["range_value"] = message.text
            await message.reply(
                text=f'Случайное число: {randint(0, int(data["range_value"]))}',
                disable_notification=True
            )
        await state.finish()

    @dp.message_handler(member=True, commands=["word", "post", "stop", "ban"], commands_prefix="/")
    async def not_creator_exception(message: types.Message) -> None:
        """Obscene word exception function"""
        await message.bot.send_message(
            message.chat.id,
            text="Команда доступна только в групповом чате для админа или создателя!",
            disable_notification=True
        )
        await message.delete()

    @dp.message_handler(creator=True, commands=["word"])
    async def word_input(message: types.Message) -> None:
        """Obscene word input function"""
        await message.reply(
            "Введи нежелательное слово...",
            disable_notification=True,
            reply_markup=kr.inline_keyboard
        )
        await usg.add_word.set()
        await message.delete()

    @dp.message_handler(state=usg.add_word)
    async def word_write(message: types.Message, state: FSMContext) -> None:
        """Obscene word write function"""
        async with state.proxy() as data:
            data["add_word"] = message.text.lower()
            with open(f'chats/{message.chat.id}.spec', 'a') as obscene_words_write:
                obscene_words_write.write(f' "{data["add_word"]}",')
            await message.reply(
                text="Слово добавлено в чёрный список!",
                disable_notification=True
            )
        await state.finish()
        await message.delete()

    @dp.message_handler(ChatMessageFilter(), commands=["feedback"])
    async def get_feedback_exception(message: types.Message) -> None:
        """Feedback exception function"""
        await message.bot.send_message(
            message.chat.id,
            text="Обратная связь работает только через личные сообщения!",
            disable_notification=True
        )
        await message.delete()

    @dp.message_handler(PrivateMessageFilter(), commands=["feedback"])
    async def get_feedback(message: types.Message) -> None:
        """Call feedback function"""
        await dbf.create_feedback(user_id=message.from_user.id)
        await message.bot.send_message(
            message.from_user.id,
            text="Введи свой email:",
            disable_notification=True,
            reply_markup=kr.inline_keyboard
        )
        await usg.user_name.set()
        await message.delete()

    @dp.message_handler(state=usg.user_name)
    async def get_user_email(message: types.Message, state: FSMContext) -> None:
        """Create user email function"""
        async with state.proxy() as data:
            data['email'] = message.text
            await message.bot.send_message(
                message.from_user.id, text="Введи своё сообщение:",
                disable_notification=True,
                reply_markup=kr.inline_keyboard
            )
            await UserStatesGroup.next()

    @dp.message_handler(state=usg.user_message)
    async def create_user_message(message: types.Message, state: FSMContext) -> None:
        """Create user message function"""
        async with state.proxy() as data:
            data['message'] = message.text
        await dbf.edit_feedback(state, user_id=message.from_user.id)
        await message.bot.send_message(
            message.from_user.id,
            "Спасибо за обращение! Постараюсь ответить в ближайшее время!",
            disable_notification=True
        )
        await state.finish()

    @dp.callback_query_handler(text="close", state="*")
    async def callback_cancel(callback: types.CallbackQuery, state: FSMContext) -> None:
        """Callback cancel function"""
        if state is None:
            return
        await state.finish()
        await callback.message.delete()

    @dp.message_handler(creator=True, commands="ban", commands_prefix="/")
    async def ban(message: types.Message) -> None:
        """Ban function"""
        await message.bot.delete_message(message.chat.id, message.message_id)
        try:
            await message.bot.kick_chat_member(
                chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id
            )
            await message.reply_to_message.reply("БАН!", disable_notification=True)
            await message.bot.send_sticker(
                chat_id=message.chat.id,
                sticker=sf.sticker_reading()[0],
                disable_notification=True
            )
        except (CantRestrictSelf, ChatAdminRequired, IndexError):
            pass

    @dp.message_handler(creator=True, commands=["stop"])
    async def switch_function(message: types.Message) -> None:
        """Switch function"""
        global switch
        switch = False

        sticker_list.clear()
        image_list.clear()
        conversation_list.clear()
        audio_list.clear()

        await message.bot.send_message(
            message.chat.id,
            text="Команда /post остановлена!",
            disable_notification=True
        )
        await message.delete()

    @dp.message_handler(creator=True, commands=["post"])
    async def get_post(message: types.Message) -> None:
        """A new post function"""
        global switch
        switch = True
        await message.delete()

        seconds_list = [17634, 21138, 24895, 28325, 32178, 35728]

        while switch:

            try:
                st = choice(sf.sticker_for_post())
                await sleep(1)
                if st not in sticker_list:
                    sticker_list.append(st)
                    await message.bot.send_sticker(
                        chat_id=message.chat.id,
                        disable_notification=True,
                        sticker=st
                    )
                    if len(sticker_list) == len(sf.sticker_for_post()):
                        sticker_list.clear()
                else:
                    continue
            except ValueError:
                pass

            try:
                img = Path(f"images/{choice(listdir('images/'))}")
                await sleep(choice(seconds_list))
                if img.stem not in image_list:
                    image_list.append(img.stem)
                    await message.bot.send_photo(
                        chat_id=message.chat.id,
                        disable_notification=True,
                        photo=open(img, "rb"),
                        caption=img.stem
                    )
                    if len(image_list) == len(listdir('images/')):
                        image_list.clear()
                else:
                    continue
            except IndexError:
                pass

            try:
                con = choice(sf.conversation_for_post())
                await sleep(choice(seconds_list))
                if con not in conversation_list:
                    conversation_list.append(con)
                    await message.bot.send_message(
                        chat_id=message.chat.id,
                        disable_notification=True,
                        text=con
                    )
                    if conversation_list == len(sf.conversation_for_post()):
                        conversation_list.clear()
                else:
                    continue
            except ValueError:
                pass

            try:
                audio = Path(f"audio/{choice(listdir('audio/'))}")
                await sleep(choice(seconds_list))
                if audio.stem not in audio_list:
                    audio_list.append(audio.stem)
                    await message.bot.send_audio(
                        chat_id=message.chat.id,
                        audio=open(audio, "rb"),
                        disable_notification=True)
                    if len(audio_list) == len(listdir('audio/')):
                        audio_list.clear()
                else:
                    continue
            except IndexError:
                pass

            await sleep(choice(seconds_list))

    @dp.message_handler(ReplyChatFilter(), content_types="sticker")
    async def sticker_from_user(message: types.Message) -> None:
        """Sticker function"""
        try:
            await message.bot.send_sticker(
                chat_id=message.chat.id,
                sticker=sf.sticker_reading()[randint(2, len(sf.sticker_reading()) - 1)],
                disable_notification=True
            )
        except ValueError:
            pass

    @dp.message_handler(ReplyChatFilter(), lambda message: message.text.lower() == "кубик")
    async def dice(message: types.Message) -> None:
        """Dice function"""
        await message.answer_dice(disable_notification=True)

    @dp.message_handler(ReplyChatFilter(), lambda message: message.text.lower() == "аудио")
    async def voice_function(message: types.Message) -> None:
        """Voice function"""
        try:
            audio = Path(f"audio/{choice(listdir('audio/'))}")
            await message.bot.send_audio(
                chat_id=message.chat.id,
                audio=open(audio, "rb"),
                disable_notification=True)
        except IndexError:
            pass

    @dp.message_handler(ReplyChatFilter())
    async def conversation(message: types.Message) -> None:
        """Conversation function and obscene words filter"""
        for i in sf.conversation_reading():
            if i in message.text.lower():
                await message.reply(sf.conversation_reading()[i], disable_notification=True)
        counter = 0

        try:
            with open(f'chats/{message.chat.id}.spec', encoding='utf-8') as obscene_words:
                words = literal_eval(f'({obscene_words.read()})')

            for i in words:
                if i in message.text.lower():
                    counter += 1
                    if counter == 1:
                        try:
                            await message.bot.send_sticker(
                                chat_id=message.chat.id,
                                sticker=sf.sticker_reading()[randint(2, len(sf.sticker_reading()) - 1)],
                                disable_notification=True
                            )
                        except ValueError:
                            pass
                        await message.answer(
                            sf.obscene_words_answer()[randint(0, len(sf.obscene_words_answer()) - 1)],
                            disable_notification=True
                        )
                    await message.delete()

        except FileNotFoundError:
            with open(f'chats/{message.chat.id}.spec', 'w') as obscene_words_write:
                obscene_words_write.write('')

        if message.text.lower() == "кто тебя создал?" or message.text.lower() == "кто твой разработчик?" or \
                message.text.lower() == "кто твой создатель?" or message.text.lower() == "кто твой автор?" or \
                message.text.lower() == "кто тебя сделал?" or message.text.lower() == "кто тебя запрограммировал?" or \
                message.text.lower() == "кто тебя создал" or message.text.lower() == "кто твой разработчик" or \
                message.text.lower() == "кто твой создатель" or message.text.lower() == "кто твой автор" or \
                message.text.lower() == "кто тебя сделал" or message.text.lower() == "кто тебя запрограммировал":
            await message.reply("https://github.com/kepler54", disable_notification=True)

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
                        try:
                            await message.bot.send_sticker(
                                chat_id=message.chat.id,
                                sticker=sf.sticker_reading()[randint(2, len(sf.sticker_reading()) - 1)],
                                disable_notification=True
                            )
                        except ValueError:
                            pass
                        await message.answer(
                            sf.obscene_words_answer()[randint(0, len(sf.obscene_words_answer()) - 1)],
                            disable_notification=True
                        )
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

    @dp.errors_handler(exception=TimeoutError)
    async def exception_timeout_error(update: types.update, exception: TimeoutError) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=TelegramAPIError)
    async def exception_telegram_api_error(update: types.update, exception: TelegramAPIError) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=AttributeError)
    async def exception_attribute_error(update: types.update, exception: AttributeError) -> bool:
        """Exception"""
        return True

    @dp.errors_handler(exception=TypeError)
    async def type_error(update: types.update, exception: TypeError) -> bool:
        """Exception"""
        return True
