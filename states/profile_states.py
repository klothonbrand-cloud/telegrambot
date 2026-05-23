from aiogram.fsm.state import State, StatesGroup

class ProfileSetup(StatesGroup):

    waiting_for_gender = State()

    waiting_for_age = State()

    waiting_for_country = State()