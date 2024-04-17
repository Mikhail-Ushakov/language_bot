from config_reader import config

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
from enum import Enum
from gandonsky import generate

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()
# dp['my_way'] = 'myyyy'


class PromptCallbackFactory(CallbackData, prefix=""):
    # prompt: Enum[str]
    prompt: str



# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f'Перевод текста с англ на рус')
    # a += 1
    # await message.answer_photo('https://w.forfun.com/fetch/03/03f8cd3f6796daaacc1fe43ffb7704b7.jpeg')


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



@dp.message(F.text)
async def translate(message: types.Message):
    text = message.text
    response = r.get(f'https://ftapi.pythonanywhere.com/translate?sl=en&dl=ru&text={text}')
    js = json.loads(response.text)
    answer = js['destination-text']
    # print(js)


    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Создать {text}",
        # callback_data=f"create_{answer.replace(' ', '')}")  
        # callback_data=PromptCallbackFactory(prompt=Enum('word', answer))
        callback_data=PromptCallbackFactory(prompt=answer)
        )
    
    await message.answer(
        f"{answer}\n\nНажми на кнопку, чтобы сгенерировать изображение(максимум 34 символа =) )",
        reply_markup=builder.as_markup()
    )
    # await messege.answer(answer)




@dp.callback_query(PromptCallbackFactory.filter())
async def send_random_value(callback: types.CallbackQuery, callback_data: PromptCallbackFactory):
    # prompt = callback.data.split('_')[1]
    # prompt = ' '.join(callback_data.prompt)
    prompt = callback_data.prompt
    image = generate(prompt)
    await callback.message.answer_photo(
            BufferedInputFile(
                base64.b64decode(image),
                filename=f"{prompt}.jpg"
            ),
            caption=f"Изображениe {prompt}"
        )
    # await callback.message.answer('a')
    await callback.answer()
    


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())