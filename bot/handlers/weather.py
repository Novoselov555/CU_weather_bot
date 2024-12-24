from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.states.weather_states import WeatherForm
from bot.utils.convert_from_address_to_coordinates import GetCoords
from bot.keyboards.keyboards import get_confirm_keyboard, choose_days_forecast
import json

router = Router()
coords_api_key = '5cbf1bfd-9264-477c-b05c-2af092e99e54'


def upload_db(path):
    with open(path, 'r') as db:
        data = json.load(db)
    return data


def download_db(path, data):
    with open(path, 'w', encoding='utf-8') as db:
        json.dump(data, db, ensure_ascii=False, indent=4)


# Пользователь использовал команду weather, и мы просим ввести пункт отправления
@router.message(Command('weather'))
async def ask_start_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    with open(f'bot/database/database_{user_id}.json', 'w', encoding='utf-8') as db:
        json.dump({}, db, ensure_ascii=False, indent=4)
    await message.answer('Введите пункт отправления: ')
    await state.set_state(WeatherForm.start_city)


@router.message(WeatherForm.start_city)
async def process_start_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text

    try:
        city_coords = GetCoords(coords_api_key).get_coords_by_address(city)
        db = upload_db(f'bot/database/database_{user_id}.json')
        db['city_0'] = {
            'city_name': city.capitalize(),
            'city_coords': city_coords
        }
        download_db(f'bot/database/database_{user_id}.json', db)

        await message.answer('Введите пункт прибытия: ')
        await state.set_state(WeatherForm.end_city)
    except ValueError as e:
        await message.answer(f'❌ Ашипка: {str(e)}, введите пункт заново')
        return
    except Exception as e:
        await message.answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
        await state.clear()


@router.message(WeatherForm.end_city)
async def process_end_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text

    try:
        city_coords = GetCoords(coords_api_key).get_coords_by_address(city)
        db = upload_db(f'bot/database/database_{user_id}.json')
        db['city_1'] = {
            'city_name': city.capitalize(),
            'city_coords': city_coords
        }
        download_db(f'bot/database/database_{user_id}.json', db)

        await message.answer(
            'Заезжаем еще куда-нибудь?',
            reply_markup=get_confirm_keyboard()
        )
        await state.set_state(WeatherForm.confirm_new_city)
    except ValueError as e:
        await message.answer(f'❌ Ашипка: {str(e)}, введите пункт заново')
        return
    except Exception as e:
        await message.answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
        await state.clear()


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
async def process_new_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text

    try:
        city_coords = GetCoords(coords_api_key).get_coords_by_address(city)
        db = upload_db(f'bot/database/database_{user_id}.json')
        city_id = int(list(db.keys())[-1].split('_')[1]) + 1
        db[f'city_{city_id}'] = {
            'city_name': city.capitalize(),
            'city_coords': city_coords
        }
        download_db(f'bot/database/database_{user_id}.json', db)
        await message.answer(
            'Заезжаем еще куда-нибудь?',
            reply_markup=get_confirm_keyboard()
        )
        await state.set_state(WeatherForm.confirm_new_city)
    except ValueError as e:
        await message.answer(f'❌ Ашипка: {str(e)}, введите пункт заново')
        return
    except Exception as e:
        await message.answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
        await state.clear()


@router.message(WeatherForm.forecast)
async def forecast(message: Message, state: FSMContext):
    ans = message.text
    if ans == 'Прогноз на 1 день':
        pass
    elif ans == 'Прогноз на 3 дня':
        pass
    elif ans == 'Прогноз на 5 дней':
        pass
    else:
        await message.answer('Вы ввели говно, переделывайте')
        return