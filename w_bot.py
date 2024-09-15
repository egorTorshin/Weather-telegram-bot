from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import requests

BOT_TOKEN = '{TELEGRAM_BOT_TOKEN}'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_cmd(message: types.Message):
    await message.answer('Введи название города')


@dp.message(F.text)
async def get_weather(message: types.Message):
    city_name = message.text
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'
        weather_data = requests.get(url).json()

        temp = round(weather_data['main']['temp'], 1)
        feels_like = round(weather_data['main']['feels_like'], 1)
        wind = round(weather_data['wind']['speed'], 1)
        clouds = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

        await message.answer(f'Погода в городе {city_name}:\n'
                             f' Температура воздуха:  {temp}°C\n'
                             f' Ощущается как:  {feels_like}°C\n'
                             f' Ветер:  {wind} м/с\n'
                             f' Погода в целом:  {clouds}\n'
                             f' Туманность:  {humidity}%'
                             )
    except KeyError:
        await message.answer(f'Не удалось определить город: {city_name}')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
