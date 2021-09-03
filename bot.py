from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from os import environ
import asyncio

from db import (create_table, insert,
                update, delete, get,
                )


loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)


class NewChannel(StatesGroup):
    get_channel_id = State()
    get_pattern = State()


@dp.message_handler(text_contains='https://www.youtube.com/channel/', state=NewChannel.get_channel_id)
async def add_channel(message: Message, state: FSMContext):
    channel_id = message.text.split('https://www.youtube.com/channel/')[1]
    await message.answer('Send me the pattern now')
    await NewChannel.next()


@dp.message_handler(state=NewChannel.get_pattern)
async def add_pattern(message: Message, state: FSMContext):
    pattern = message.text
    # insert()
    await message.answer(
        'Done! You will get a message when video with title corresponding your pattern will be uploaded')
