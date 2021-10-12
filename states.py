from aiogram.dispatcher.filters.state import StatesGroup, State


class NewChannel(StatesGroup):
    get_channel_id = State()
    get_pattern = State()


class UpdateChannel(StatesGroup):
    get_channel = State()
    get_pattern = State()


class DeleteChannel(StatesGroup):
    get_channel = State()
    confirm = State()