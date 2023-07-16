from aiogram.dispatcher.filters.state import StatesGroup, State


class LoginStates(StatesGroup):
    choose_sign = State()
    input_login = State()
    input_password = State()

class RegisterStates(StatesGroup):
    input_fullname = State()
    input_phone = State()
