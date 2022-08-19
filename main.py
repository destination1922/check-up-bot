import logging
import requests
from config import *
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(text=START_TEXT)

@dp.callback_query_handler()
async def app_function(query: types.CallbackQuery):
    telegram_id = query.from_user.id
    app_id = query.data

    r = requests.get(f"{BASIC_API}by_app?param={app_id}")
    r_data = r.json()
    data = r_data['data'][0]
    await bot.send_message(chat_id=telegram_id, text=notify(data), parse_mode='HTML')

@dp.message_handler()
async def catch_message(message: types.Message):
    msg = message.text

    if check_message(msg) != 'error':
        r = requests.get(f"{BASIC_API}by_{check_message(msg)}?param={msg}")
        r_data = r.json()
        data = r_data['data']

        if len(data) == 1:
            for child in data: await message.answer(text=notify(child), parse_mode='HTML')

        elif len(data) > 1:
            app_array = []
            for child in data[1:]:
                ar_i = []
                id = child['app_id']
                text = f"Aриза рақами: {id}  {get_date(child['app_date'])}"
                ar_i.append(text)
                ar_i.append(str(id))
                app_array.append(ar_i)

            inline_app_markup = types.InlineKeyboardMarkup(row_width=1)
            btns_app = (types.InlineKeyboardButton(text, callback_data=data) for text, data in app_array)
            inline_app_markup.add(*btns_app)

            data0 = data[0]
            await message.answer(text=last_notify(data0), parse_mode='HTML', reply_markup=inline_app_markup)
        else:
            await message.answer("Ҳеч қандай ариза топилмади!")
    else:
        await message.answer(text="Илтимос ноўрин хабар юборманг!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

