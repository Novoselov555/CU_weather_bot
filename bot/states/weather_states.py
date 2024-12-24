from aiogram.fsm.state import StatesGroup, State

class WeatherForm(StatesGroup):
    start_city = State()
    end_city = State()

    # Здесь будем добавлять в json файл информацию по городам
    ask_new_city = State()
    confirm_new_city = State()
    process_new_city = State()

    forecast = State()
