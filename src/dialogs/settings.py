from aiogram_dialog import LaunchMode, Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Cancel

import states
from .custom_widgets.i18n_format import I18NFormat

settings_dialog = Dialog(
    Window(
        I18NFormat("settings-info"),
        Start(
            I18NFormat("settings-report-status-text"),
            id="report_toggle_btn",
            state=states.ConfigJobsDialog.config_job,
        ),
        Start(
            I18NFormat("settings-balance"),
            id="name_config_for_balance_report",
            state=states.ReportConfigDialog.select_names,
        ),
        Cancel(I18NFormat("cancel")),
        state=states.Settings.MAIN,
    ),
    launch_mode=LaunchMode.ROOT,
)
