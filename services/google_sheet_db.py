import json
from enum import Enum
from telegram import Message
from constants.app_constants import DB_PREFIX, HISTORY_SHEET_NAME, HISTORY_RANGE, MAX_CELL_RANGE
from google_api.google_drive_api import GoogleDriveApi
from google_api.google_sheet_api import GoogleSheetApi
import os

google_drive_api = GoogleDriveApi()
google_sheets_api = GoogleSheetApi()


class DatabaseCellEnum(Enum):
    ARCHIVE = 0
    DATE = 1
    USERNAME = 2
    FIRST_NAME = 3
    IS_BOT = 4


class GoogleSheetDB:
    def get(self, chat_id, range_name):
        spreadsheet_id = self.get_spreadsheet_id(chat_id)
        result = google_sheets_api.get_spreadsheet_values(spreadsheet_id, range_name)
        values = result.get('values', [])
        return values

    def append(self, chat_id, range_name, value):
        spreadsheet_id = self.get_spreadsheet_id(chat_id)
        values = [
            value
        ]
        return google_sheets_api.append_spreadsheet_values(spreadsheet_id, values, range_name)

    def update(self, chat_id, range_name, value):
        spreadsheet_id = self.get_spreadsheet_id(chat_id)
        values = [
            value
        ]
        return google_sheets_api.update_spreadsheet_values(spreadsheet_id, values, range_name)

    def get_spreadsheet_id(self, chat_id: str) -> str:
        spreadsheet_name = f'{DB_PREFIX}{chat_id}'
        spreadsheet_id = google_drive_api.get_spreadsheet_id_by_name(spreadsheet_name)
        if spreadsheet_id is None:
            spreadsheet_id = self.create_spreadsheet(spreadsheet_name)
        return spreadsheet_id

    def create_spreadsheet(self, spreadsheet_name):
        email = os.environ["ADMIN_EMAIL"]
        spreadsheet_id = google_sheets_api.create_spreadsheet(spreadsheet_name)
        google_sheets_api.create_sheet(spreadsheet_id, HISTORY_SHEET_NAME)
        google_drive_api.add_permission(spreadsheet_id, email)
        return spreadsheet_id

    def put_message(self, message: Message):
        original_message = '{}'
        first_name = message.from_user.first_name
        username = message.from_user.username
        is_bot = message.from_user.is_bot
        date = message.date.isoformat()
        chat_id = str(message['chat_id'])
        range_name = f'{HISTORY_SHEET_NAME}!{HISTORY_RANGE}'
        value = [
            original_message,  # DatabaseCellEnum.ARCHIVE
            date,  # DatabaseCellEnum.DATE
            username,  # DatabaseCellEnum.USERNAME
            first_name,  # DatabaseCellEnum.FIRST_NAME
            is_bot  # DatabaseCellEnum.IS_BOT
        ]
        return self.append(chat_id, range_name, value)

    def get_history(self, chat_id: str):
        range_name = f'{HISTORY_SHEET_NAME}!{MAX_CELL_RANGE}'
        return self.get(chat_id, range_name)
