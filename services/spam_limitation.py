# In the file is placed a logic for messages that the bot can send one time per a particular period

import os
from telegram import Bot
from datetime import timedelta, datetime
from messages.helpers import delay_message_replying, delay_message_sending
from services.google_sheet_db import GoogleSheetDB

google_sheet_db = GoogleSheetDB()


def is_period_of_silence_is_over(message, range_name, silent_period):
    chat_id = str(message['chat_id'])
    now = datetime.now()
    hours_ago = now - timedelta(hours=silent_period)
    data_list = google_sheet_db.get(chat_id, range_name)
    last_message_date = next((d[0] for d in data_list), None)
    if last_message_date is None or datetime.strptime(last_message_date, '%Y-%m-%d %H:%M:%S') < hours_ago:
        google_sheet_db.update(chat_id, range_name, [now.isoformat()])
        return True
    else:
        return False


async def reply_to_message_with_spam_limitation(message, text, range_name, silent_period, delay=0):
    is_should_be_send = is_period_of_silence_is_over(message, range_name, silent_period)
    if is_should_be_send:
        await delay_message_replying(message, text, delay)
    return


async def send_message_with_spam_limitation(message, text, range_name, silent_period, delay=0):
    is_should_be_send = is_period_of_silence_is_over(message, range_name, silent_period)
    if is_should_be_send:
        chat_id = str(message['chat_id'])
        bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
        await delay_message_sending(bot, chat_id, text, delay)
    return
