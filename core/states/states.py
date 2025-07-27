from aiogram.fsm.state import StatesGroup, State

class ProductCreation(StatesGroup):
    short_name = State()
    name = State()
    description = State()
    photo = State()
    price = State()
