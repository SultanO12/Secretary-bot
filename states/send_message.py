from aiogram.dispatcher.filters.state import StatesGroup, State

class SendMessage(StatesGroup):
    text = State()