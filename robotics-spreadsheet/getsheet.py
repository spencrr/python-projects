import gspread
from oauth2client.service_account import ServiceAccountCredentials

def open_spreadsheet(client_open_key):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    return client.open(client_open_key)
