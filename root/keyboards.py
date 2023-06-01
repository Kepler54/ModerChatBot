from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class KeyboardRandom:
    """Keyboard random"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
    inline_keyboard.add(cancel_button)
