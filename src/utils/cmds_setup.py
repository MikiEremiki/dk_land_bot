from aiogram.types import BotCommand, BotCommandScopeDefault


async def setup_commands(bot):
    await bot.delete_my_commands(BotCommandScopeDefault())
    await bot.set_my_commands([
        BotCommand(command='start', description='Старт/Перезапуск бота'),
        BotCommand(command='balance', description='Отчет по балансам'),
    ],
        scope=BotCommandScopeDefault()
    )
