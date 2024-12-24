# Weather Forecast Telegram Bot

## Описание проекта
Этот проект представляет собой Telegram-бота, который предоставляет прогноз погоды для заданных городов. Пользователь может получить информацию о погоде на 1, 3 или 5 дней. Бот также генерирует графики температуры и вероятности дождя, которые отправляются пользователю в виде изображений.

## Стек технологий
- **Python** — основной язык программирования
- **Aiogram** — библиотека для разработки Telegram-ботов
- **Plotly** — визуализация данных
- **Pandas** — обработка и анализ данных
- **JSON** — хранение данных о погоде

## Функциональность
- Получение прогноза погоды по заданным городам
- Поддержка многодневных прогнозов (1, 3, 5 дней)
- Генерация графиков с температурой и вероятностью дождя
- Логирование ошибок
- Элегантные ответы с использованием эмодзи и форматированного текста

## Установка и запуск
### Установка зависимостей
```bash
pip install -r requirements.txt
```
### Настройка API-ключей
- В файле кода установите свои API-ключи для получения координат и данных о погоде:
```python
coords_api_key = 'YOUR_COORDS_API_KEY'
weather_api_key = 'YOUR_WEATHER_API_KEY'
```

### Запуск бота
```bash
python bot.py
```

## Пример работы
- Пользователь отправляет команду `/weather`
- Бот запрашивает город отправления и город назначения
- Пользователь выбирает количество дней для прогноза (1, 3, 5)
- Бот отправляет текстовый прогноз и графики с температурой и вероятностью дождя

## Примечания
- Для работы с графиками необходимо установить `kaleido`:
```bash
pip install kaleido
```
- Ошибки логируются в файл `bot_errors.log`.

## Контакты
Если у вас есть вопросы или предложения, обращайтесь:
- Telegram: [@your_username](https://t.me/your_username)
- Email: your_email@example.com
