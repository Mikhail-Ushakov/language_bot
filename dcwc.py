from config_reader import config
from gandonsky import generate

import asyncio
import logging
import json
import base64
import requests as r
from aiogram import F, Bot, Dispatcher, types, html
from aiogram.filters.command import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import BufferedInputFile


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


class PromptCallbackFactory(CallbackData, prefix=""):
    prompt: str



def get_kb_for_image(text):
    builder = InlineKeyboardBuilder()
    builder.button(
            text=f"Создать {text}",
            callback_data=PromptCallbackFactory(prompt=text)
        )
    return builder.as_markup()




@dp.message(Command('words'))
async def get_list_words(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    response = r.get('http://127.0.0.1:8000/api/', headers={'id': str(user_id)})
    words = json.loads(response.text)
    print(words)
    res = f'{words}'
    await message.answer(res)




# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f'Перевод текста с англ на рус')
   

@dp.message(Command('test'))
async def test(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(
            text='йоу', 
            request_poll=types.KeyboardButtonPollType()
        )
    )
    await message.answer(text='change action', reply_markup=builder.as_markup())


@dp.message(Command('language'))
async def test(message: types.Message):
    # builder = ReplyKeyboardBuilder()
    # builder.add(
    #     types.KeyboardButton(
    #         text='йоу', 
    #         request_poll=types.KeyboardButtonPollType()
    #     )
    # )
    await message.answer(text='change action')


@dp.message(F.text)
async def translate(message: types.Message):
    text = message.text
    response = r.get(f'https://ftapi.pythonanywhere.com/translate?sl=en&dl=ru&text={text}')
    js = json.loads(response.text)
    answer = js['destination-text']

    await message.answer(answer.capitalize())
    # await message.answer(
    #     f"{answer.capitalize()}\n\nНажми на кнопку, чтобы сгенерировать изображение(максимум 34 символа =) )",
    #     reply_markup=get_kb_for_image(answer) if len(answer.encode()) <= 64 else None
    # )




@dp.callback_query(PromptCallbackFactory.filter())
async def send_random_value(callback: types.CallbackQuery, callback_data: PromptCallbackFactory):
    prompt = callback_data.prompt
    print(prompt)
    image = generate.delay((prompt))
    await callback.message.answer_photo(
            BufferedInputFile(
                base64.b64decode(image),
                filename=f"{prompt}.jpg"
            ),
            caption=f"Изображениe {prompt}"
        )
    await callback.message.answer('Идет загрузка фото')
    await callback.answer()
    

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())