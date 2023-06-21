from aiogram.dispatcher.filters.state import StatesGroup, State

class SearchInfo(StatesGroup):
    types = State()
    