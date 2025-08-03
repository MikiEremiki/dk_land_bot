import logging

from gspread_asyncio import AsyncioGspreadClientManager, AsyncioGspreadClient
from google.oauth2.service_account import Credentials

from utils.read_write_utils import get_list_items_in_file

googlesheets_logger = logging.getLogger('bot.googlesheets')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

FIRST_VALUE = 'Беляков Анатолий'
LAST_VALUE = 'Касса'


def get_creds():
    creds = Credentials.from_service_account_file('credentials.json')
    scoped = creds.with_scopes(SCOPES)
    return scoped


agcm = AsyncioGspreadClientManager(get_creds)


async def balance_of_accountable_funds_report(ss_id, range, path):
    agc: AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(ss_id)
    values = await ss.values_get(range)
    values = values['values']

    first_index = values[0].index(FIRST_VALUE)

    list_id_for_report = get_list_items_in_file(path)

    list_for_report = [[], []]
    for index in list_id_for_report:
        list_for_report[0].append(values[0][int(index)+first_index])
        list_for_report[1].append(values[1][int(index)+first_index])
    return list_for_report


async def get_list_of_all_names_from_sheet(ss_id, range):
    agc: AsyncioGspreadClient = await agcm.authorize()
    ss = await agc.open_by_url(ss_id)
    values = await ss.values_get(range)
    values = values['values']

    first_index = values[0].index(FIRST_VALUE)
    last_index = values[0].index(LAST_VALUE)

    return values[0][first_index:last_index + 1]
