import json
from functools import cached_property
from google.oauth2 import service_account
from googleapiclient.discovery import build
from constants.app_constants import SPREADSHEETS_SCOPES
from messages.helpers import decode_base64
import os


class GoogleAbstractApi:
    SERVICE_NAME = ''
    SERVICE_VERSION = ''
    SCOPES = []

    @cached_property
    def service(self):
        base64_key = os.environ["GCP_KEYFILE"]
        secret_json = decode_base64(base64_key)
        secret_info = json.loads(secret_json)
        credentials = service_account.Credentials.from_service_account_info(secret_info, scopes=SPREADSHEETS_SCOPES)
        service = build(self.SERVICE_NAME, self.SERVICE_VERSION, credentials=credentials)
        return service

