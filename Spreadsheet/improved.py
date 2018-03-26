import sys, csv, numpy, pprint
import getsheet

printer = pprint.PrettyPrinter()

if len(sys.argv) == 2:
    sheet_key = sys.argv[1]
else:
    exit()

spreadsheet = getsheet.open_spreadsheet(sheet_key)
worksheets = spreadsheet.worksheets()
responses = worksheets[0]
raw = responses.get_all_values()[1:]

teams = {}

for row in raw:
    entry = []
    for data_point in row:
        entry.append(int(data_point) if data_point.isdecimal() else data_point)

    team = entry[1]
    match = entry[2]
    entry[3] = 100 if entry[3] == 'Crossed' else 0
    entry[7] = 100 if entry[7] == 'Yes' else 0
    entry[13] = 100 if entry[13] == 'Yes' else 0 #defense
    entry[14] = 100 if entry[14] == 'Yes' else 0 #against
    entry[15] = 100 if entry[15] == 'Yes' else 50 if entry[15] == 'Attempted' else 0 #park
    entry[16] = 100 if entry[16] == 'Yes' else 0 #ramps
    entry[17] = 100 if entry[15] == 'Yes' else 50 if entry[15] == 'Attempted' else 0 #climb

    data = {match: entry[3:18]}

    if team not in teams:
        teams[team] = [data]
    else:
        teams[team].append(data)

for team in teams:


printer.pprint(teams)
