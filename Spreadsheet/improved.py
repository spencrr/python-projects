import sys, csv, numpy, pprint
import getsheet

def main(sheet_key):
    printer = pprint.PrettyPrinter()

    spreadsheet = getsheet.open_spreadsheet(sheet_key)
    worksheets = spreadsheet.worksheets()
    for i in range(1, len(worksheets)):
        spreadsheet.del_worksheet(worksheets[i])
    spreadsheet.add_worksheet('Averages', 1, 1)
    responses = worksheets[0]
    output = worksheets[1]
    raw = responses.get_all_values()[1:]

    teams = {}

    for row in raw:
        entry = []
        for data_point in row:
            entry.append(int(data_point) if data_point.isdecimal() else data_point)

        team = entry[1]
        match = entry[2]
        entry[3] = 100 if entry[3] == 'Crossed' else 0 #crossed
        entry[7] = 100 if entry[7] == 'Yes' else 0  #auto drop
        entry[13] = 100 if entry[13] == 'Yes' else 0 #defense
        entry[14] = 100 if entry[14] == 'Yes' else 0 #against
        entry[15] = 100 if entry[15] == 'Yes' else 0 if entry[15] == 'Attempted' else 0 #park
        entry[16] = 100 if entry[16] == 'Yes' else 0 #ramps
        entry[17] = 100 if entry[15] == 'Yes' else 0 if entry[15] == 'Attempted' else 0 #climb

        total_switch = sum(entry[i] for i in [8, 10])
        total_cube  = sum(entry[i] for i in range(8, 12))
        total_switch_exchange = sum(entry[i] for i in [8, 10, 11])

        data = {match: entry[3:18] + [total_switch, total_cube, total_switch_exchange]}

        if team not in teams:
            teams[team] = [data]
        else:
            teams[team].append(data)

    # printer.pprint(teams)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        sheet_key = sys.argv[1]
    else:
        exit()
    main(sheet_key)
