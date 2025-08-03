from typing import Optional

from dynaconf import Dynaconf
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class BotSettings(BaseModel):
    token: SecretStr
    developer_chat_id: Optional[int]
    supply_chat_id: Optional[int]
    supply_thread_id: Optional[int]


class PathsSettings(BaseModel):
    locales: str


class GoogleSettings(BaseModel):
    ddc_ss_id: str
    ddc_range: str
    path_list_name_for_report: str


class Config(BaseSettings):
    bot: BotSettings
    paths: PathsSettings
    google: GoogleSettings


def load_config(env='default') -> Config:
    dyna_settings = Dynaconf(
        envvar_prefix='DYNACONF',
        settings_files=['settings.toml', '.secrets.toml'],
        environments=True,
        env=env
    )
    config = Config(
        bot=BotSettings(token=dyna_settings.bot.token,
                        developer_chat_id=dyna_settings.bot.developer_chat_id,
                        supply_chat_id=dyna_settings.bot.supply_chat_id,
                        supply_thread_id=dyna_settings.bot.supply_thread_id),
        paths=PathsSettings(locales=dyna_settings.path.locales),
        google=GoogleSettings(ddc_ss_id=dyna_settings.google.ddc_ss_id,
                              ddc_range=dyna_settings.google.ddc_range,
                              path_list_name_for_report=dyna_settings.google.path_list_name_for_report)
    )

    return config
