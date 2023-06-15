from aiogram.dispatcher.filters.state import StatesGroup, State

class AddMalumot(StatesGroup):
    text = State()
    img = State()
    video = State()