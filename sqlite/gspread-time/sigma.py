import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

def open_spreadsheet(client_open_key):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    return client.open_by_key(client_open_key)


def main():
	spreadsheet = open_spreadsheet('1vptL2WMDbj6XNyTgOICG3KBoa98yoVHr1W8pCVl8SUY')
	sheet = spreadsheet.get_worksheet(0)
	pprint(sheet.get_all_values())

if __name__ == '__main__':
	main()
	for o in dir():
		pprint((o, type(o), dir(o)))