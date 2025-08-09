from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from api import googlesheets
from config.config import Config

balance_router = Router()


@balance_router.message(Command(commands='balance'))
async def report_of_balances(message: Message, config: Config, bot: Bot):
    access_chats = {
        config.bot.supply_chat_id,
        config.bot.developer_chat_id
    }
    message_chat_id = message.chat.id
    if message_chat_id not in access_chats:
        await message.answer('У вас нет прав для просмотра данной информации')
    else:
        text = await get_text_report_balance(config)

        if message_chat_id == config.bot.supply_chat_id:
            await bot.send_message(
                chat_id=message_chat_id,
                text=text,
                message_thread_id=config.bot.supply_thread_id
            )
        else:
            await message.answer(text)


async def send_report_of_balances(config: Config, bot: Bot):
    text = await get_text_report_balance(config)
    text += "\n<i>Вечерний отчет</i>"
    await bot.send_message(
        chat_id=config.bot.supply_chat_id,
        text=text,
        message_thread_id=config.bot.supply_thread_id
    )


async def get_text_report_balance(config):
    report = await googlesheets.balance_of_accountable_funds_report(
        config.google.ddc_ss_id,
        config.google.ddc_range,
        config.google.path_list_name_for_report
    )
    if len(report[0]) == 0:
        text = 'Настройте список для отчета\nИспользуйте /settings'
    else:
        text = f'#БалансСредств На текущий момент\n'
        for i in range(len(report[0])):
            text += f'{report[0][i]}: {report[1][i]}руб\n'
    return text
