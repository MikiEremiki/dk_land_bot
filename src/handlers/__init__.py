from aiogram import Router

from filters import OnlyAdminFilter

from .start_cmd import start_router
from .settings_cmd import settings_router
from .echo_cmd import echo_router
from .report_of_balance import balance_router, send_report_of_balances


def get_routers(config) -> list[Router]:
    settings_router.message.filter(
        OnlyAdminFilter([config.bot.developer_chat_id]))
    return [
        start_router,
        settings_router,
        echo_router,
        balance_router
    ]
