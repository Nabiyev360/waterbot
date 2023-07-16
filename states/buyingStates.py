from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyStates(StatesGroup):
    wait_product_count = State()
    wait_updating_count = State()