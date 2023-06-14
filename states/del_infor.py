from aiogram.dispatcher.filters.state import StatesGroup, State

class Delinfo(StatesGroup):
    data = State()
    check = State()

class DelSignin(StatesGroup):
    check = State()