from aiogram import Router

from .main import main_dialog
from .settings import settings_dialog
from .report_balance_config_dialog import report_config_dialog
from .config_job_balance import config_job_balance_dialog


def get_dialog_routers() -> list[Router]:
    return [
        main_dialog,
        settings_dialog,
        report_config_dialog,
        config_job_balance_dialog,
    ]