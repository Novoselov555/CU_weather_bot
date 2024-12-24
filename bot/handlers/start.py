from aiogram.filters import CommandStart
from aiogram import Router, types

router = Router()


# Обработка команды /start
@router.message(CommandStart())
async def handle_welcome(message: types.Message):
    user_info = message.from_user
    first_name = user_info.first_name if user_info.first_name is not None else ''
    last_name = user_info.last_name if user_info.last_name is not None else ''
    user_name = first_name + ' ' + last_name
    await message.answer(f'Привет, {user_name}!\n'
                         'Бот дает возможность отслеживать погоду на проложенном вами маршруте.')
