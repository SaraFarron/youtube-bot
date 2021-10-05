from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)


def create_inline_keyboard(buttons: dict[str: str], max_rows=2):
    """Return inline keyboard with buttons added"""

    keyboard = InlineKeyboardMarkup(max_rows=max_rows)

    for button_name, button_callback in buttons.items():
        keyboard.add(InlineKeyboardButton(button_name, callback_data=button_callback))

    return keyboard
