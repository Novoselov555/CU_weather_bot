from aiogram.fsm.state import StatesGroup, State

class WeatherForm(StatesGroup):
    start_city = State()
    end_city = State()
    intermediate_cities = State()
