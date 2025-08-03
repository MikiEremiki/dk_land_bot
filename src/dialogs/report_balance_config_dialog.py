import operator

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Multiselect, Button, Group, ManagedMultiselect
from aiogram_dialog.widgets.text import Const, Format

from api import googlesheets
from config.config import Config
from states import ReportConfigDialog
from utils.read_write_utils import (
    write_list_of_items_in_file, get_list_items_in_file)


async def get_names_data(
        dialog_manager: DialogManager,
        config: Config,
        **kwargs
):
    """
    Загружает список имен для отчета.
    """
    list_of_all_names_for_report = (
        await googlesheets.get_list_of_all_names_from_sheet(
            config.google.ddc_ss_id, config.google.ddc_range)
    )
    names = [(name, i) for i, name in enumerate(list_of_all_names_for_report)]
    return {
        "names": names,
    }


async def set_checked_names(start_data: dict, manager: DialogManager):
    """
    Загружает сохраненные выбранные имена и устанавливает их в MultiSelect.
    """
    config: Config = manager.middleware_data['config']
    selected_ids = get_list_items_in_file(config.google.path_list_name_for_report)
    multiselect: ManagedMultiselect = manager.find("names_multiselect")
    for i in selected_ids:
        await multiselect.set_checked(int(i), True)


async def on_done_clicked(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager
):
    """
    Вызывается при нажатии кнопки "Готово".
    Сохраняет выбранные элементы и завершает диалог.
    """
    selected_ids = manager.find("names_multiselect").get_checked()

    await callback.answer("Сохраняю выбор...")

    config: Config = manager.middleware_data['config']
    write_list_of_items_in_file(selected_ids,
                                config.google.path_list_name_for_report)

    await callback.message.edit_text(
        f"Отлично! Настройки отчета сохранены. Выбрано {len(selected_ids)} чел.")

    await manager.done()


report_config_dialog = Dialog(
    Window(
        Const("Выберите сотрудников для включения в отчет по остаткам:"),
        Group(
            Multiselect(
                Format("✓ {item[0]}"),  # Текст для выбранного элемента
                Format("{item[0]}"),  # Текст для невыбранного элемента
                id="names_multiselect",  # Уникальный ID для виджета
                item_id_getter=operator.itemgetter(1),
                # Функция для получения ID из элемента списка
                items="names",  # Ключ из геттера, по которому лежат данные
            ),
            Button(Const("Готово"), id="done_btn",
                   on_click=on_done_clicked),
            width=1
        ),
        state=ReportConfigDialog.select_names,
        getter=get_names_data,
    ),
    on_start=set_checked_names
)


async def configure_report_of_balances(message: Message,
                                       dialog_manager: DialogManager):
    """
    Запускает диалог настройки отчета.
    """
    command = dialog_manager.middleware_data.get('command')
    await dialog_manager.start(ReportConfigDialog.select_names,
                               data={'command_args': command.args},
                               mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.DELETE_AND_SEND)
