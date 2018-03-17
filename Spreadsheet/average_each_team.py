import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint, numpy, csv

def column(matrix, i):
    return [row[i] for row in matrix]

def main():
    printer = pprint.PrettyPrinter()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key('1F-mDcNMgpiLjxybfn6DhDYI7X_mClUwyVLxyrwztOhY')
    all_worksheets = spreadsheet.worksheets()
    responses = all_worksheets[0]
    for worksheet in all_worksheets:
        if worksheet != responses:
            spreadsheet.del_worksheet(worksheet)
    output_sheet = spreadsheet.add_worksheet('Averages', 1, 1)

    raw = responses.get_all_values()
    sheet = []

    for row in raw:
        if row[1][1].isdecimal():
            converted = []
            for cell in row:
                if len(cell) > 0:
                    encoded_cell = cell.encode('utf-8')
                    converted.append(
                        int(encoded_cell) if cell.isdecimal() else encoded_cell)
            if len(converted) > 0:
                sheet.append(converted)

    collected_teams = []
    data = []

    for entry in sheet:
        team = entry[1]
        if team not in collected_teams:
            collected_teams.append(team)
            data.append([team, []])
        index = collected_teams.index(team)
        entry[3] = 100 if entry[3] == b'Crossed' else 0 #baseline
        entry[7] = 100 if entry[7] == b'Yes' else 0 #auto_drop
        match_data = entry[2:13]
        match_data.append(sum(entry[8:10])) #tele_switch
        match_data.append(sum(entry[8:12])) #tele_cube
        data[index][1].append(match_data)

    export = [['Team', 'Matches Scouted', 'Crossed %', 'Auto Switch', 'Auto Scale', 'Auto Exchange',
        'Auto Drop %', 'Tele Switch', 'Tele Opp Switch', 'Tele Scale', 'Tele Exchange',
        'Tele Drop', 'Tele Total Switch', 'Tele Total Cube']]
    for team in data:
        matches = []
        match_indeces = []
        for match in team[1]:
            match_number = match[0]
            if match_number not in matches:
                matches.append(match_number)
                match_indeces.append(team[1].index(match))
            else:
                print('{} has a duplicate match #{}'.format(team[0], match_number), end=' ')
                discrepencies = 0
                for i in range(team[1].index(match)+1):
                    discrepencies += 1 if team[1][i] != match else 0
                if discrepencies > 0
                    print('and there is a discrepency ({})'.format(discrepencies))
        team_data = [team[0], len(team[1])]
        averages = [numpy.mean(column(team[1],i)) for i in range(1, len(team[1][0]))]
        team_data.extend(averages)
        export.append(team_data)

    with open('export.csv', 'w') as f:
        wr = csv.writer(f)
        for row in export:
            wr.writerow(row)

    for row in export:
        output_sheet.append_row(row)

if __name__ == '__main__':
    main()
