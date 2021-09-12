from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
import asyncio

from db import (insert, update, delete,
                get,)
from main import logger, get_last_videos


loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())


def create_keyboard(subs):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for sub in subs:  # TODO
        button = InlineKeyboardButton(f'')


class NewChannel(StatesGroup):
    get_channel_id = State()
    get_pattern = State()


class UpdateChannel(StatesGroup):
    get_channel = State()
    get_pattern = State()


class DeleteChannel(StatesGroup):
    get_channel = State()
    confirm = State()


@dp.message_handler(Text(contains='youtube.com/channel/'))
async def add_channel(message: Message, state: FSMContext):
    logger.info(f'user {message.from_user.username} sent link')
    channel_id = message.text.split('/channel/')[1]
    async with state.proxy() as data:
        data['channel'] = channel_id
    await message.answer('Send me the pattern now')
    await NewChannel.get_pattern.set()


@dp.message_handler(state=NewChannel.get_pattern)
async def add_pattern(message: Message, state: FSMContext):
    logger.info(f'{message.from_user.username} is adding pattern')
    pattern = message.text
    async with state.proxy() as data:
        insert(channel=data['channel'], pattern=pattern, table=message.from_user.username)
    await message.answer(
        'Done! You will get a message when video with title corresponding your pattern will be uploaded')
    await state.finish()


@dp.message_handler(Command('UpdateSubscription'))
async def update_subscription(message: Message, state: FSMContext):
    subs = get(message.from_user.username)

    await message.answer(subs)


@dp.message_handler(Command('ShowAllSubscriptions'))
async def show_subscriptions(message: Message):
    subs = get(message.from_user.username)
    await message.answer(subs)


@dp.message_handler(Command('CallMain'))  # TODO For dev purposes, delete after
async def main(message: Message):
    logger.info(get_last_videos('UCyzelLPcSrGUdLhN79eA4mg'))
    await message.answer('done')


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)


async def send_notification(link: str, user: str):
    await bot.send_message(chat_id=user, text=link)


async def background_on_start():
    """Background task which is created when bot starts"""

    while True:
        await asyncio.sleep(86400)  # Every day
        channels = get('')
        for channel in channels:
            videos = get_last_videos(channel, number=5)
            videos_in_db = get(channel)

            for video in videos:  # TODO
                if video not in videos_in_db:
                    asyncio.create_task(send_notification())


# --------- In case this will be needed ---------
async def background_on_action():
    """Background task which is created when user asked"""

    while True:
        logger.info('Background task in progress')
        await asyncio.sleep(10)


@dp.message_handler(Command('start'))
async def background_task_creator(message: Message):
    """Creates background tasks"""

    asyncio.create_task(background_on_action())
    await message.reply("Background task create")
# --------- In case this will be needed ---------


async def on_bot_start_up(dispatcher: Dispatcher):
    """List of actions which should be done before bot start"""

    asyncio.create_task(background_on_start())  # creates background task


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_bot_start_up)
