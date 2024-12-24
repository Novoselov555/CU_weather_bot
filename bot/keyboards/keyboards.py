from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes")],
            [InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")]
        ]
    )

def choose_days_forecast():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Прогноз на 1 день')],
            [KeyboardButton(text='Прогноз на 3 дня')],
            [KeyboardButton(text='Прогноз на 5 дней')]
        ],
        resize_keyboard=True
    )