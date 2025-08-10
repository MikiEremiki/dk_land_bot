from aiogram.types import (
    BotCommand, BotCommandScopeDefault, BotCommandScopeChat)

from config.config import Config


async def setup_commands(bot, config: Config):
    await bot.delete_my_commands(BotCommandScopeDefault())
    balance_cmd = BotCommand(command='balance', description='Отчет по балансам')
    start_cmd = BotCommand(command='start', description='Старт/Перезапуск бота')
    await bot.set_my_commands([
        start_cmd,
        balance_cmd,
    ],
        scope=BotCommandScopeDefault()
    )
    await bot.set_my_commands([
        start_cmd,
        balance_cmd,
        BotCommand(command='settings', description='Настройки бота')
    ],
        scope=BotCommandScopeChat(chat_id=config.bot.developer_chat_id)
    )

