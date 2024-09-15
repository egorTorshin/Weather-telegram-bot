from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import requests

BOT_TOKEN = '7239236509:AAFvIRtSIF34SIIEVe6ABXLI_e2N_sOD0QM'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_cmd(message: types.Message):
    await message.answer('Введи название города')


@dp.message(F.text)
async def get_weather(message: types.Message):
    city = message.text
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=dcbc9c3857e22b64862636d8d596a986'
        weather_data = requests.get(url).json()

        temp = round(weather_data['main']['temp'], 1)
        feels_like = round(weather_data['main']['feels_like'], 1)
        wind = round(weather_data['wind']['speed'], 1)
        clouds = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

        await message.answer(f'Погода в городе {city}:\n'
                             f' Температура воздуха:  {temp}°C\n'
                             f' Ощущается как:  {feels_like}°C\n'
                             f' Ветер:  {wind} м/с\n'
                             f' Погода в целом:  {clouds}\n'
                             f' Туманность:  {humidity}%'
                             )
    except KeyError:
        await message.answer(f'Не удалось определить город: {city}')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
