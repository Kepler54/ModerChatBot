from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class KeyboardRandom:
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    random_button = InlineKeyboardButton(text="Random Value", callback_data="random")
    close_button = InlineKeyboardButton(text="Close", callback_data="close")
    inline_keyboard.add(random_button).add(close_button)
