from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BI2-xYgDrfGqg9eRFg2cJYtSnjRm3wawEdXjtL2faaM'
#SAMPLE_RANGE_NAME = 'IDC Form Responses!A:CF'

def get_google_sheet(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    """Shows basic usage of the Sheets API.

    Prints values from a sample spreadsheet.
    """
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/Users/usmriz/PycharmProjects/AutomateCorrity/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME).execute()

    return result

def gsheet2df(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    gsheet = get_google_sheet(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)


    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.

    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                try:
                    column_data.append(row[col_id])
                except IndexError:
                    column_data.append("")
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
    return df

if __name__ == "__main__":
    #result = get_google_sheet()
    #print(result.keys())
    df = gsheet2df('1E6Po26eVE4R3bkDJzYfjVichgHhOj7LagFEWp-o_8XM', '2018!A:R')
    print(df.head())
