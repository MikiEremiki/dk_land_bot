from __future__ import annotations

import logging
import os
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot

from config.config import Config
from handlers.report_of_balance import send_report_of_balances
from utils.read_write_utils import check_path
from .constant import _JOB_ID_REPORT, _FLAG_DIR, _FLAG_FILE_NAME

_logger = logging.getLogger("scheduler")


def _flag_path() -> str:
    return os.path.join(os.getcwd(), _FLAG_DIR, _FLAG_FILE_NAME)


def is_report_enabled() -> bool:
    """Return True if the report job is enabled. Defaults to True if no flag file exists."""
    try:
        check_path(_FLAG_DIR)
        path = _flag_path()
        if not os.path.exists(path):
            return True
        with open(path, mode="r", encoding="utf-8") as f:
            content = f.read().strip()
            return content == "1"
    except Exception as e:
        _logger.warning("Failed to read report enabled flag: %s", e)
        return True

def add_report_job(config, bot, scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        send_report_of_balances,
        "cron",
        args=[config, bot],
        hour=18,
        minute=0,
        day_of_week="mon-fri",
        id=_JOB_ID_REPORT,
        replace_existing=True,
    )


def _write_report_enabled(enabled: bool) -> None:
    check_path(_FLAG_DIR)
    path = _flag_path()
    with open(path, mode="w", encoding="utf-8") as f:
        f.write("1" if enabled else "0")


def set_report_enabled(enable: bool, config: Config, bot: Bot, scheduler: Optional[AsyncIOScheduler]) -> None:
    """Enable/disable the report job and persist the flag.

    If scheduler is running, add/remove the job accordingly.
    """
    _write_report_enabled(enable)

    job = scheduler.get_job(_JOB_ID_REPORT)
    if enable:
        if job is None:
            add_report_job(config, bot, scheduler)
            _logger.info("Job '%s' has been enabled and scheduled", _JOB_ID_REPORT)
        else:
            _logger.info("Job '%s' already enabled", _JOB_ID_REPORT)
    else:
        if job is not None:
            scheduler.remove_job(_JOB_ID_REPORT)
            _logger.info("Job '%s' has been disabled and removed", _JOB_ID_REPORT)
        else:
            _logger.info("Job '%s' already disabled", _JOB_ID_REPORT)
