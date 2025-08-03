import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from fluentogram import TranslatorHub
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

from config import load_config
from config.config import Config
from handlers.errors import on_unknown_intent, on_unknown_state
from log.logging_conf import load_log_config
from middlewares.logging import LoggingMiddleware
from middlewares.i18n import TranslatorRunnerMiddleware
from utils.cmds_setup import setup_commands
from utils.i18n import create_translator_hub
from handlers import get_routers, send_report_of_balances
from dialogs import get_dialog_routers

bot_logger = load_log_config()
bot_logger.info('Инициализация бота')


async def main():
    config: Config = load_config()

    bot = Bot(token=config.bot.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await setup_commands(bot)
    dp = Dispatcher(events_isolation=SimpleEventIsolation())
    scheduler = AsyncIOScheduler(timezone=timezone('Europe/Moscow'))

    translator_hub: TranslatorHub = create_translator_hub(config)

    dp.message.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(TranslatorRunnerMiddleware(translator_hub))

    dp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    dp.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))

    dp.include_routers(*get_routers(config))
    dp.include_routers(*get_dialog_routers())

    setup_dialogs(dp)

    scheduler.add_job(
        send_report_of_balances, 'cron', args=[config, bot],
        hour=18, minute=0, day_of_week='mon-fri')
    scheduler.start()

    try:
        await dp.start_polling(bot, config=config)
    except Exception as e:
        print(e)
    finally:
        await dp.stop_polling()


asyncio.run(main())
