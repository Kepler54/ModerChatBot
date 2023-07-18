from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class KeyboardClose:
    """Close keyboard"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    cancel_button = InlineKeyboardButton(text="Закрыть", callback_data="close")
    inline_keyboard.add(cancel_button)
