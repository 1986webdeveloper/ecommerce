"""google sheet read module"""
import os.path
import pickle

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.conf import settings
import os
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_RANGE_NAME = "A:Z"


def read_gsheet(sheet_id=None):
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
                os.path.join(settings.BASE_DIR, "credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(os.path.join(settings.BASE_DIR, "token.pickle"), "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(
            spreadsheetId=sheet_id,
            range=SAMPLE_RANGE_NAME,
        )
        .execute()
    )
    values = result.get("values", [])
    if values:
        data_frame = pd.DataFrame(values)
        data_frame.columns = data_frame.iloc[0]  # Selecting 0th row as columns
        data_frame = data_frame.iloc[1:]  # Selecting from the 1st row
        return data_frame.to_dict("records")
    return []
