from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Format

from config.config import Config
import states
from scheduler.jobs import is_report_enabled, set_report_enabled
from .custom_widgets.i18n_format import I18NFormat


async def get_job_dialog_data(dialog_manager: DialogManager, **kwargs):
    """
    Provide current report scheduler status and localized labels.
    """
    enabled = is_report_enabled()
    print(enabled)
    i18n = dialog_manager.middleware_data.get("i18n")
    status_key = "settings-report-status-enabled" if enabled else "settings-report-status-disabled"
    on_off_text = "settings-report-toggle-disable" if enabled else "settings-report-toggle-enable"
    return {
        "report_enabled": enabled,
        "report_status_text": i18n.get(status_key),
        "report_on_off_text": i18n.get(on_off_text)
    }


async def switch_report_job(
        callback: CallbackQuery, button: Button, manager: DialogManager
):
    enabled = not is_report_enabled()
    config: Config = manager.middleware_data["config"]
    bot: Bot = manager.middleware_data["bot"]
    scheduler = manager.middleware_data.get("scheduler")
    set_report_enabled(enabled, config, bot, scheduler)
    await callback.answer()


config_job_balance_dialog = Dialog(
    Window(
        I18NFormat("settings-info"),
        Format("{report_status_text}"),
        Button(
            Format("{report_on_off_text}"),
            id="disable_report_btn",
            on_click=switch_report_job,
        ),
        Cancel(I18NFormat("cancel")),
        state=states.ConfigJobsDialog.config_job,
        getter=get_job_dialog_data,
    )
)
