from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def anon_share(url) -> InlineKeyboardMarkup:
    text = "Поделиться ссылкой"
    buttons = [
        [
            InlineKeyboardButton(text=text, url=url)
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


async def answer_button(user_id) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="Ответить", callback_data=f"answer_{user_id}")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
