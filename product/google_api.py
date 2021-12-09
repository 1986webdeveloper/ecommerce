import os.path
import pickle

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleSheet(object):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    SAMPLE_SPREADSHEET_ID = "1qbZy1JqtlvpVrYSaKU9-esipXox5RufzoOB1hR8UMOU"
    SAMPLE_RANGE_NAME = "A:Z"
    CLIENT_ID = os.environ.get('CLIENT_ID', 'unsafe-secret-id')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'unsafe-secret-key')

    @classmethod
    def read(cls, sheet_id=None):
        """
        Read google-sheet and return a records of google-sheet
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "../ecommerce/credentials.json", cls.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId=sheet_id or cls.SAMPLE_SPREADSHEET_ID,
                range=cls.SAMPLE_RANGE_NAME,
            )
            .execute()
        )
        values = result.get("values", [])
        if values:
            df = pd.DataFrame(values)
            df.columns = df.iloc[0]  # Selecting 0th row as columns
            df = df.iloc[1:]  # Selecting from the 1st row
            return df.to_dict("records")
        return []
