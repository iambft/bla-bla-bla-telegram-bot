import asyncio
from datetime import datetime, date, timedelta

from constants.app_constants import HISTORY_SHEET_NAME, MAX_CELL_RANGE
from google_api.google_drive_api import GoogleDriveApi
from messages.answers.abstract import AnswerAbstract, AnswerPriorityEnum
from constants.message_keys_constants import ASK_STATISTIC_MESSAGE_KEYS
from services.google_sheet_db import GoogleSheetDB, DatabaseCellEnum

drive_api = GoogleDriveApi()
google_sheet_db = GoogleSheetDB()


class Statistics(AnswerAbstract):
    priority = AnswerPriorityEnum.HEIGHT

    def is_proceed(self) -> bool:
        return self.message_holder.is_text_contain(ASK_STATISTIC_MESSAGE_KEYS)

    async def action(self) -> None:
        message = self.message_holder.message
        chat_id = str(message['chat_id'])
        msg = create_statistic_message(chat_id)
        await message.reply_text(msg)
        return


def get_messages(chat_id: str):
    range_name = f'{HISTORY_SHEET_NAME}!{MAX_CELL_RANGE}'
    message_list = google_sheet_db.get(chat_id, range_name)
    return message_list


def get_statistic(chat_id, from_date, to_date):
    message_list = get_messages(chat_id)
    has_statistic_for_whole_period = False
    res = {}
    for message in message_list:
        # todo: should use try catch to avoid bd error crashes
        # todo: have to filter bot messages
        date_cell_data = message[DatabaseCellEnum.DATE.value]
        message_date = datetime.fromisoformat(date_cell_data).date()

        if message_date <= from_date:
            has_statistic_for_whole_period = True

        if from_date <= message_date <= to_date:
            username = message[DatabaseCellEnum.USERNAME.value]
            res[username] = {
                'username': message[DatabaseCellEnum.USERNAME.value],
                'name':  message[DatabaseCellEnum.FIRST_NAME.value],
                'count': res.get(username, {'count': 0})['count'] + 1
            }
    return None if not has_statistic_for_whole_period else list(res.values())


def create_statistic_message(chat_id: str):
    today = date.today()
    week_ago = today - timedelta(days=7)
    statistic = get_statistic(chat_id, week_ago, today)
    if statistic is None:
        return "Ой всьо"
    user_statistics = sorted(statistic, key=lambda x: x['count'], reverse=True)[:10]
    res = f"Персони, які зіграли найзначнішу роль у житті чату за тиждень {week_ago.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')}"
    for index, item in enumerate(user_statistics):
        line = f'\n{index+1}. {item["name"]} ({item["username"]}) - {item["count"]}'
        res = f"{res}{line}"
    return res
