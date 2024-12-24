import plotly.express as px
import pandas as pd
import json

# Добавляем модуль для сохранения графиков в виде изображений
import plotly.io as pio


def generate_graphs(user_id, city_id, days):
    # Загружаем данные о погоде
    with open(f'bot/database/database_{user_id}.json', 'r') as file:
        weather_data = json.load(file)

    df = pd.DataFrame(weather_data[city_id]['weather_data'][:days])
    df['date'] = pd.to_datetime(df['date'])  # Преобразуем дату

    # Построение графика температуры
    fig_temp = px.line(
        df,
        x='date',
        y=['max_temp', 'min_temp'],
        labels={'value': 'Температура (°C)', 'date': 'Дата'},
        title='Температурный прогноз на несколько дней'
    )

    # Построение графика вероятности дождя
    fig_rain = px.bar(
        df,
        x='date',
        y=[df['day_forecast'].apply(lambda x: x['rain_probability']),
           df['night_forecast'].apply(lambda x: x['rain_probability'])],
        labels={'value': 'Вероятность дождя (%)', 'date': 'Дата'},
        title='Вероятность дождя на несколько дней'
    )
    fig_rain.update_layout(barmode='group', xaxis_tickangle=-45)

    # Сохранение графиков в виде изображений
    temp_path = f'bot/graphs/temp_{user_id}_{city_id}.png'
    rain_path = f'bot/graphs/rain_{user_id}_{city_id}.png'

    pio.write_image(fig_temp, temp_path)
    pio.write_image(fig_rain, rain_path)

    return temp_path, rain_path
