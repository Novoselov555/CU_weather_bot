from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.states.weather_states import WeatherForm
from bot.utils.convert_from_address_to_coordinates import GetCoords

router = Router()
api_key = '5cbf1bfd-9264-477c-b05c-2af092e99e54'


@router.message(Command('weather'))
async def ask_start_city(message: Message, state: FSMContext):
    await message.answer('Введите пункт отправления: ')
    await state.set_state(WeatherForm.start_city)


@router.message(WeatherForm.start_city)
async def process_start_city(message: Message, state: FSMContext):
    start_city = message.text

    try:
        city_coords = GetCoords(api_key).get_coords_by_address(start_city)
        await state.update_data(start_city=start_city, start_city_coords=city_coords)
        await message.answer('Введите пункт прибытия: ')
        await state.set_state(WeatherForm.end_city)
        return
    except ValueError as e:
        await message.answer(f'❌ Ашипка: {str(e)}, введите пункт заново')
        return
    except Exception as e:
        await message.answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
        await state.clear()


@router.message(WeatherForm.end_city)
async def process_end_city(message: Message, state: FSMContext):
    end_city = message.text

    try:
        city_coords = GetCoords(api_key).get_coords_by_address(end_city)
        await state.update_data(end_city=end_city, end_city_coords=city_coords)
        await message.answer('Будем заезжать куда еще?')
        await state.set_state(WeatherForm.intermediate_cities)
        return
    except ValueError as e:
        await message.answer(f'❌ Ашипка: {str(e)}, введите пункт заново')
        return
    except Exception as e:
        await message.answer(f'⚠️ Произошла непредвиденная ошибка. {str(e)}')
        await state.clear()
