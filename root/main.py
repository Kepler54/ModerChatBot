from os import getenv
from asyncio import run
from dotenv import load_dotenv
from bot import handlers_register
from sqlite import DataBaseFeedback
from aiogram import Bot, Dispatcher
from logging import basicConfig, INFO
from aiogram.contrib.fsm_storage.memory import MemoryStorage

dbf = DataBaseFeedback()


def register(dp: Dispatcher) -> None:
    handlers_register(dp)


async def main() -> None:
    """Entry point"""
    basicConfig(level=INFO)
    load_dotenv('.env')
    token = getenv('token')
    bot = Bot(token)  # , proxy='http://proxy.server:3128'
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    register(dp)

    await dbf.db_start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()


if __name__ == '__main__':
    run(main())
