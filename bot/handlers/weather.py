from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.states.weather_states import WeatherForm
from bot.utils.convert_from_address_to_coordinates import GetCoords
from bot.utils.weather_receiver import WeatherReceiver
from bot.utils.create_graph import generate_graphs
from bot.keyboards.keyboards import get_confirm_keyboard, choose_days_forecast
import json
import logging
import traceback
from functools import wraps

router = Router()
coords_api_key = '5cbf1bfd-9264-477c-b05c-2af092e99e54'
weather_api_key = 'Rg2Bp0Mxu9Lpz4uabYzfOZuEbrt1pKP9'

logging.basicConfig(level=logging.ERROR, filename='bot_errors.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')
def upload_db(path):
    with open(path, 'r') as db:
        data = json.load(db)
    return data


def download_db(path, data):
    with open(path, 'w', encoding='utf-8') as db:
        json.dump(data, db, ensure_ascii=False, indent=4)



def catch_exceptions(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            return await handler(*args, **kwargs)
        except ValueError as e:
            if isinstance(args[0], Message):
                await args[0].answer(f'❌ Ошибка: {str(e)}, попробуйте снова.')
            elif isinstance(args[0], CallbackQuery):
                await args[0].message.answer(f'❌ Ошибка: {str(e)}')
            logging.error(f'ValueError in {handler.__name__}: {str(e)}')
            logging.error(traceback.format_exc())
        except Exception as e:
            if isinstance(args[0], Message):
                await args[0].answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
            elif isinstance(args[0], CallbackQuery):
                await args[0].message.answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
            logging.critical(f'Unhandled Exception in {handler.__name__}: {str(e)}')
            logging.critical(traceback.format_exc())
            if 'state' in kwargs:
                await kwargs['state'].clear()
    return wrapper


# Пользователь использовал команду weather, и мы просим ввести пункт отправления
@router.message(Command('weather'))
async def ask_start_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    with open(f'bot/database/database_{user_id}.json', 'w', encoding='utf-8') as db:
        json.dump({}, db, ensure_ascii=False, indent=4)
    await message.answer('🌆 Введите пункт отправления: ')
    await state.set_state(WeatherForm.start_city)


@router.message(WeatherForm.start_city)
@catch_exceptions
async def process_start_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text
    city_coords = GetCoords(coords_api_key).get_coords_by_address(city)
    db = upload_db(f'bot/database/database_{user_id}.json')
    weather_data = WeatherReceiver(weather_api_key).get_weather(city_coords[0], city_coords[1])
    db['city_0'] = {
        'city_name': city.capitalize(),
        'city_coords': city_coords,
        'weather_data': weather_data
    }
    download_db(f'bot/database/database_{user_id}.json', db)

    await message.answer('🚄 Введите пункт прибытия: ')
    await state.set_state(WeatherForm.end_city)


@router.message(WeatherForm.end_city)
@catch_exceptions
async def process_end_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text
    city_coords = GetCoords(coords_api_key).get_coords_by_address(city)
    weather_data = WeatherReceiver(weather_api_key).get_weather(city_coords[0], city_coords[1])
    db = upload_db(f'bot/database/database_{user_id}.json')
    db['city_1'] = {
        'city_name': city.capitalize(),
        'city_coords': city_coords,
        'weather_data': weather_data
    }
    download_db(f'bot/database/database_{user_id}.json', db)

    await message.answer(
        'Заезжаем еще куда-нибудь?',
        reply_markup=get_confirm_keyboard()
    )
    await state.set_state(WeatherForm.confirm_new_city)



@router.callback_query(WeatherForm.confirm_new_city)
async def confirm_new_city(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'confirm_yes':
        await callback.message.edit_text(
            'Введите промежуточный пункт: '
        )
        await state.set_state(WeatherForm.process_new_city)

    elif callback.data == 'confirm_no':
        await callback.message.delete()
        await callback.message.answer('Выберите количество дней для прогнозирования: ', reply_markup=choose_days_forecast())
        await state.set_state(WeatherForm.forecast)


@router.message(WeatherForm.process_new_city)
@catch_exceptions
async def process_new_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text

    city_coords = GetCoords(coords_api_key).get_coords_by_address(city)
    db = upload_db(f'bot/database/database_{user_id}.json')
    weather_data = WeatherReceiver(weather_api_key).get_weather(city_coords[0], city_coords[1])
    city_id = int(list(db.keys())[-1].split('_')[1]) + 1
    db[f'city_{city_id}'] = {
        'city_name': city.capitalize(),
        'city_coords': city_coords,
        'weather_data': weather_data
    }
    download_db(f'bot/database/database_{user_id}.json', db)
    await message.answer(
        '🗺️ Заезжаем еще куда-нибудь?',
        reply_markup=get_confirm_keyboard()
    )
    await state.set_state(WeatherForm.confirm_new_city)


@router.message(WeatherForm.forecast)
@catch_exceptions
async def forecast(message: Message, state: FSMContext):
    user_id = message.from_user.id
    ans = message.text
    db = upload_db(f'bot/database/database_{user_id}.json')

    forecast_days = {
        'Прогноз на 1 день': 1,
        'Прогноз на 3 дня': 3,
        'Прогноз на 5 дней': 5
    }

    if ans in forecast_days:
        days = forecast_days[ans]
        for city, city_data in db.items():
            await message.answer(f"📍 Прогноз погоды для города: {city_data['city_name']}")
            weather_data = city_data['weather_data']
            for i in range(days):
                await send_forecast(message, weather_data[i])
            temp_path, rain_path = generate_graphs(user_id, city, days)
            await message.answer_photo(FSInputFile(temp_path))
            await message.answer_photo(FSInputFile(rain_path))
    else:
        await message.answer('❌ Некорректный ввод, попробуйте еще раз.')
        return


async def send_forecast(message: Message, weather_data: dict):
    date = weather_data['date']
    max_temp = weather_data['max_temp']
    min_temp = weather_data['min_temp']

    day_forecast = weather_data['day_forecast']
    night_forecast = weather_data['night_forecast']

    await message.answer(f"🌞 <b>День {date}:</b>", parse_mode='HTML')
    await message.answer(f"🌡️ Температура: {max_temp}°C\n"
                         f"💧 Влажность: {day_forecast['humidity']}%\n"
                         f"💨 Скорость ветра: {day_forecast['wind_speed']} м/с\n"
                         f"☔ Вероятность дождя: {day_forecast['rain_probability']}%")

    await message.answer(f"🌙 <b>Ночь:</b>", parse_mode='HTML')
    await message.answer(f"🌡️ Температура: {min_temp}°C\n"
                         f"💧 Влажность: {night_forecast['humidity']}%\n"
                         f"💨 Скорость ветра: {night_forecast['wind_speed']} м/с\n"
                         f"☔ Вероятность дождя: {night_forecast['rain_probability']}%")