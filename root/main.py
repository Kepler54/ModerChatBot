import os
import asyncio
import logging
from dotenv import load_dotenv
from bot import handlers_register
from aiogram import Bot, Dispatcher


def register(dp: Dispatcher):
    handlers_register(dp)


async def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv('.env')
    token = os.getenv('token')
    bot = Bot(token)
    dp = Dispatcher(bot)
    register(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
