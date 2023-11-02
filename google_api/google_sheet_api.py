from google_api.google_abstract_api import GoogleAbstractApi


class GoogleSheetApi(GoogleAbstractApi):
    SERVICE_NAME = 'sheets'
    SERVICE_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def batch_update(self, requests, spreadsheet_id):
        body = {
            'requests': requests
        }
        return self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    def create_sheet(self, spreadsheet_id: str, title: str):
        sheet = {
            "addSheet": {
                "properties": {
                    "title": title
                }
            }
        }
        self.batch_update(sheet, spreadsheet_id)

    def create_spreadsheet(self, title: str):
        spreadsheet = {
            'properties': {
                'title': title
            },
            'sheets': {

            }
        }

        return self.service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()['spreadsheetId']

    def rename_sheet(self, spreadsheet_id, sheet_id, new_name):
        updates = {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "title": new_name,
                },
                "fields": "title",
            }
        }
        return self.batch_update(updates, spreadsheet_id)

    def get_spreadsheet_values(self, spreadsheet_id: str, range_name: str):
        return self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

    def append_spreadsheet_values(self, spreadsheet_id, values, range_name):
        data = {
            "range": range_name,
            "majorDimension": "ROWS",
            "values": values,
        }
        return self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            body=data,
            range=range_name,
            valueInputOption='USER_ENTERED'
        ).execute()

    def update_spreadsheet_values(self, spreadsheet_id, values, range_name):
        data = {
            "range": range_name,
            "majorDimension": "ROWS",
            "values": values,
        }
        return self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            body=data,
            range=range_name,
            valueInputOption='USER_ENTERED'
        ).execute()
