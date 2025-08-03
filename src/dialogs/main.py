from aiogram.types import User
from aiogram_dialog import LaunchMode, Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Cancel

import states
from .custom_widgets.i18n_format import I18NFormat


async def get_username(event_from_user: User, **kwargs):
    return {'username': event_from_user.username or event_from_user.full_name}

main_dialog = Dialog(
    Window(
        I18NFormat('settings-balance-info'),
        Cancel(I18NFormat('cancel')),
        state=states.Main.MAIN,
    ),
    getter=get_username,
    launch_mode=LaunchMode.ROOT,
)
