import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import re

from . import scopes
# The ID and range of a sample spreadsheet.
spreadsheets_id = "1lFqtMo0jicu9JAkHgNisQnIlFQc1mJlJyCLnOuaGQX8"

def test():
    print(scopes)
    print(spreadsheets_id)

class GameSheet:
    def __init__(self, spreadsheets_id, scopes):
        self.scopes = scopes
        self.spreadsheets_id = spreadsheets_id
        self.service = self._build_sheet_service()
    def _build_sheet_service(self):
        return build_sheet_service(self.scopes)

class Sheet(GameSheet):
    def __init__(self, name, spreadsheets_id, scopes, max_col="I"):
        super().__init__(spreadsheets_id, scopes)
        self.name = name
        self.max_col = max_col
        # self._max_col = string.ascii_uppercase.find(max_col) + 1
    def _get(self, range):
        _range = f"{self.name}!{range}"
        values = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheets_id, range=_range).execute()
        return values['values']
    def _update(self, row_index, values):
        _range = f"{self.name}!A{row_index}:{self.max_col}{row_index}"
        body = {'values': [values]}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheets_id, range=_range,
            valueInputOption="USER_ENTERED", body=body).execute()
        return result
    def _append(self, values):
        _range = f"{self.name}!A{self.last_row+1}:{self.max_col}{self.last_row+1}"
        body = {'values': [values]}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheets_id, range=_range,
            valueInputOption='RAW', body=body).execute()
        return result
    @property
    def last_row(self):
        return len(self._get("A1:A"))
    @staticmethod
    def _create_values(index, value):
        values = [None]*(index+1)
        values[index] = value
        return values


   
def build_sheet_service(scopes):
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", scopes)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:     
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", scopes
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    return service
  
  except HttpError as err:
    print(err)
