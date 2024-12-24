from aiogram import Bot, Dispatcher, types, F
import logging
import asyncio
import os
from dotenv import load_dotenv
from bot.handlers import start, help, weather

load_dotenv()

# Настройки логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('API_TOKEN')

# Создаем бота для диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_routers(
    start.router,
    help.router,
    weather.router
)

# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')
