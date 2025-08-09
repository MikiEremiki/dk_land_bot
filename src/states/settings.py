from aiogram.fsm.state import State, StatesGroup


class Settings(StatesGroup):
    MAIN = State()

class ReportConfigDialog(StatesGroup):
    select_names = State()

class ConfigJobsDialog(StatesGroup):
    config_job = State()
