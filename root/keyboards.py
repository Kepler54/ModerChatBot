from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class KeyboardRandom:
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    random_button = InlineKeyboardButton(text="Нажать", callback_data="random")
    close_button = InlineKeyboardButton(text="Закрыть", callback_data="close")
    inline_keyboard.add(random_button).add(close_button)


class KeyboardRockPaperScissors:
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    rock_button = InlineKeyboardButton(text="Камень", callback_data='rock')
    paper_button = InlineKeyboardButton(text="Бумага", callback_data='paper')
    scissors_button = InlineKeyboardButton(text="Ножницы", callback_data='scissors')
    close_button = InlineKeyboardButton(text="Закрыть", callback_data='close')
    inline_keyboard.add(rock_button, paper_button, scissors_button).add(close_button)
