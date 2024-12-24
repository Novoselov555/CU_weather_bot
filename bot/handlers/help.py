from aiogram.filters import Command
from aiogram import Router, types

router = Router()


# Обработка команды /help
@router.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer('/start — краткое приветствие.\n'
                         '/help — список доступных команд с подсказками.\n'
                         '/weather — запрос прогноза погоды с возможностью указать:\n'
                         '      - Начальную и конечную точки маршрута.\n'
                         '      - Временной интервал прогноза (1, 3 или 5 дней).\n'
                         '      - Промежуточные остановки для получения детальной информации.')
