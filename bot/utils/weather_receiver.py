import requests
import json


class WeatherReceiver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
        self.forecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'

    # Достаем locationKey, чтобы дальше получить данные о погоде
    def get_location_key(self, lat, lon):
        params = {
            'format': json,
            'apikey': self.api_key,
            'q': f'{lat},{lon}'
        }
        response = requests.get(self.location_url, params=params)
        if response.status_code == 200:
            return response.json()['Key']
        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    # Получаем все данные о погоде в текущий момент
    def get_weather(self, lat, lon):
        params = {
            'apikey': self.api_key,
            'metric': True,
            'details': True
        }
        location_key = self.get_location_key(lat, lon)
        response = requests.get(self.forecast_url + f'{location_key}/', params=params)
        if response.status_code == 200:
            data = response.json()
            with open('weather_forecast.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

# Оставляем лишь ключевые параметры
def weather_key_parameters():
    try:
        with open('weather_forecast.json', 'r') as file:
            data = json.load(file)

        daily_parameters = list()
        for daily_forecast in data['DailyForecasts']:
            # так как мы не знаем, когда поедут люди в путешествие, целесообразно брать прогноз погоды как на день, так и на ночь
            params = {
                'date': daily_forecast['Date'],
                'max_temp': daily_forecast['Temperature']['Maximum']['Value'],
                'min_temp': daily_forecast['Temperature']['Minimum']['Value'],
                'avg_temp': (daily_forecast['Temperature']['Maximum']['Value'] +
                             daily_forecast['Temperature']['Minimum']['Value']) / 2,
                'day_forecast': {
                    'humidity': daily_forecast['Day']['RelativeHumidity']['Average'],
                    'wind_speed': daily_forecast['Day']['Wind']['Speed']['Value'],
                    'rain_probability': daily_forecast['Day']['RainProbability'],
                },
                'night_forecast': {
                    'humidity': daily_forecast['Night']['RelativeHumidity']['Average'],
                    'wind_speed': daily_forecast['Night']['Wind']['Speed']['Value'],
                    'rain_probability': daily_forecast['Night']['RainProbability']
                }
            }
            daily_parameters.append(params)

        with open('weather_key_parameters.json', 'w', encoding='utf-8') as file:
            json.dump(daily_parameters, file, ensure_ascii=False, indent=4)

        return daily_parameters
    except FileNotFoundError:
        print('Файл "weather_forecast" не найден')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


# api_key = 'AGlRoTK491bc73SZrvSPGGx6fisQS586'
# location = WeatherReceiver(api_key)
# # lat, lon = 52.516259, 13.377217
# lat, lon = 66.084712, 76.680559
# location.get_weather(lat, lon)
# weather_key_parameters()
