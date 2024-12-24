from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Dispatcher

dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def handle_welcome(message: Message):
    user_info = message.from_user
    first_name = user_info.first_name if user_info.first_name is not None else ''
    last_name = user_info.last_name if user_info.last_name is not None else ''
    user_name = first_name + ' ' + last_name
    await message.answer(f'Привет, {user_name}!\n'
                         'Бот дает возможность отслеживать погоду на проложенном вами маршруте.')

# Обработка команды /help
@dp.message(Command('help'))
async def handle_help(message: Message):
    await message.answer('/start — краткое приветствие и описание функционала.\n'
                         '/help — список доступных команд с подсказками.\n'
                         '/weather — запрос прогноза погоды с возможностью указать:\n'
                         '      - Начальную и конечную точки маршрута.\n'
                         '      - Временной интервал прогноза (1, 3 или 5 дней).\n'
                         '      - Промежуточные остановки для получения детальной информации.')

# Обработка команды /weather
@dp.message(Command('weather'))
async def fsm_start():
    # На этом этапе будет вызываться fsm
    pass
