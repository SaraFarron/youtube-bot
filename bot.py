from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import environ
import asyncio

from db import *
from states import NewChannel, UpdateChannel, DeleteChannel
from main import logger, get_last_videos
from keyboards import create_inline_keyboard


loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())


@dp.message_handler(Text(contains='youtube.com/c'))
async def add_channel(message: Message, state: FSMContext):

    logger.info(f'user {message.from_user.username} sent link')
    try:
        channel_id = message.text.split('/channel/')[1]
    except IndexError:  # TODO bug with short links eg http://youtube.com/c/TrashTaste CRITICAL bot becomes unusable
        channel_id = message.text.split('/c/')[1]

    async with state.proxy() as data:
        data['channel_id'] = channel_id

    await message.answer('Send me the pattern now')
    await NewChannel.get_pattern.set()


@dp.message_handler(state=NewChannel.get_pattern)
async def add_pattern(message: Message, state: FSMContext):

    logger.info(f'{message.from_user.username} is adding pattern')
    pattern = message.text

    async with state.proxy() as data:
        channel_data = get_last_videos(data['channel_id'])
        logger.info(channel_data)

    channel_id, channel_name = channel_data['channel_id'], channel_data['channel_title']
    videos = [video for video in channel_data['videos']]
    response = new_user_subscription(channel_id, channel_name, pattern, message.from_user.username)

    if not response:
        add_channel_to_db(channel_id, videos)
        await message.answer(
            "Done! You will get a message when video with title you're interested will be uploaded")
    else:
        await message.answer('Something went wrong')

    await state.finish()


@dp.message_handler(Command('UpdateSubscription'))
async def update_subscription(message: Message, state: FSMContext):

    subs = get_value(message.from_user.username)
    if subs == 'Error':
        await message.answer("You don't have any subscriptions")
    else:
        logger.info(subs)
        subs = {f'{sub[1]}:\n{sub[3]}': sub[0] for sub in subs}
        keyboard = create_inline_keyboard(subs, max_rows=1)

        await message.answer('Choose a subscription you want to change', reply_markup=keyboard)
        await UpdateChannel.get_channel.set()


@dp.message_handler(state=UpdateChannel.get_pattern)
async def get_pattern(message: Message, state: FSMContext, callback_data):
    pass


@dp.message_handler(Command('ShowAllSubscriptions'))
async def show_subscriptions(message: Message):

    subs = get_value(message.from_user.username)
    if not subs:
        await message.answer("You don't have any subscriptions yet")
    response = ''

    for sub in subs:
        response += f'{sub[1]} - {sub[3]}\n'

    await message.answer(response)


@dp.message_handler(Command('CallMain'))  # TODO For dev purposes, delete after
async def main(message: Message):

    logger.info(get_last_videos('UCyzelLPcSrGUdLhN79eA4mg'))
    await message.answer('done')


@dp.message_handler()
async def echo(message: Message):
    buttons = {'name': 1, 'another': 2}
    logger.info('echoing')
    await message.answer(message.text, reply_markup=create_inline_keyboard(buttons))


async def send_notification(link: str, user: str):
    await bot.send_message(chat_id=user, text=link)


async def background_on_start():
    """Background task which is created when bot starts"""

    while True:
        await asyncio.sleep(86400)  # Every day
        channels = get_value('channels')
        for channel in channels:
            videos = get_last_videos(channel, number=5)
            videos_in_db = get_value(channel)

            for video in videos['videos']:  # TODO
                if video not in get_value('channels', 'channel_id'):
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
