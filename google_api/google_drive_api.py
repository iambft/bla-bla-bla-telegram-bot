from google_api.google_abstract_api import GoogleAbstractApi


class GoogleDriveApi(GoogleAbstractApi):
    SERVICE_NAME = 'drive'
    SERVICE_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def get_spreadsheet_id_by_name(self, name: str):
        file_list = self.get_file_list()
        return next((i['id'] for i in file_list if i['name'] == name), None)

    def add_permission(self, file_id: str, email: str):
        print(email)
        data = {
            "emailAddress": email,
            "role": "writer",
            "type": "user"
        }
        self.service.permissions().create(fileId=file_id, body=data).execute()

    def get_file_list(self):
        # TODO: list pagination
        res = self.service.files().list().execute()
        return res['files']

    def remove_file(self, file_id):
        print(file_id)
        self.service.files().delete(fileId=file_id).execute()

    def rename_spreadsheet(self, file_id: str, new_name: str):
        body = {
            "name": new_name
        }
        return self.service.files().update(fileId=file_id, body=body).execute()


