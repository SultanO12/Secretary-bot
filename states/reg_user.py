from aiogram.dispatcher.filters.state import StatesGroup, State

class RegUser(StatesGroup):
  phone_number = State()
  password = State()
  check = State()