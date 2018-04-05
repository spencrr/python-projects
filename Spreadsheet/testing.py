import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sys, csv

if len(sys.argv) != 3:
    exit()

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

# c = gspread.v4.Client(creds)
pprint(c)

with open(sys.argv[2], 'r') as f:
    reader = csv.reader(f)
    data = ''
    for row in reader:
        for s in row:
            data += ', '.join(str(s))
        data += '\n'

pprint(data)
# c.import_csv(sys.argv[1], data)
