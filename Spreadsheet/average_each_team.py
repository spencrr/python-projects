import getsheet
import pprint, numpy, csv, sys

def column(matrix, i):
    return [row[i] for row in matrix]

def write_to_csv(filename, output):
    with open(filename, 'w') as f:
        wr = csv.writer(f)
        for row in output:
            wr.writerow(row)

def main():
    printer = pprint.PrettyPrinter()

    if len(sys.argv) == 2:
        sheet_key = sys.argv[1]
    else:
        exit()

    spreadsheet = getsheet.open_spreadsheet(sheet_key)
    all_worksheets = spreadsheet.worksheets()
    responses = all_worksheets[0]
    for worksheet in all_worksheets:
        if worksheet != responses:
            spreadsheet.del_worksheet(worksheet)
    # spreadsheet.del_worksheet(all_worksheets[1])
    output_sheet = spreadsheet.add_worksheet('Averages', 1, 1)

    raw = responses.get_all_values()
    sheet = []

    for row in raw:
        if row[1].isdecimal():
            converted = []
            for cell in row:
                if len(cell) > 0:
                    encoded_cell = cell.encode('utf-8')
                    converted.append(
                        int(encoded_cell) if cell.isdecimal() else encoded_cell)
            if len(converted) > 0:
                sheet.append(converted)

    collected_teams = []
    collected_matches = {}
    data = []

    for entry in sheet:
        team = entry[1]
        match_number = entry[2]

        if match_number not in collected_matches:
            collected_matches[match_number] = 1
        else:
            collected_matches[match_number] = collected_matches[match_number] + 1

        if team not in collected_teams:
            collected_teams.append(team)
            data.append([team, []])
        index = collected_teams.index(team)


        entry[3] = 100 if entry[3] == b'Crossed' else 0 #baseline
        entry[7] = 100 if entry[7] == b'Yes' else 0 #auto_drop
        match_data = entry[2:13]
        match_data.append(entry[8] + entry[10]) #tele_switch
        match_data.append(sum(entry[8:12])) #tele_cube
        match_data.append(entry[8] + entry[10] + entry[11])
        data[index][1].append(match_data)

    # printer.pprint(collected_matches)
    for match_number, value in collected_matches.items():
        if value != 6:
            print('Match #{} scouted {} times'.format(match_number, value))

    export = [['Team', 'Matches Scouted', 'Crossed %', 'Auto Switch', 'Auto Scale', 'Auto Exchange',
        'Auto Drop %', 'Tele Switch', 'Tele Scale', 'Tele Opp Switch', 'Tele Exchange',
        'Tele Drop', 'Tele Total Switch', 'Tele Total Cube', 'Tele Switch and Exchange']]
    for team in data:
        matches = []
        for match in team[1]:
            match_number = match[0]
            if match_number not in matches:
                matches.append(match_number)
            else:
                print('Team #{} duplicate on Match #{}'.format(team[0], match_number))
        team_data = [team[0], len(team[1])]
        averages = [numpy.mean(column(team[1],i)) for i in range(1, len(team[1][0]))]
        team_data.extend(averages)
        export.append(team_data)

    write_to_csv('export.csv', export)

    for row in export:
        output_sheet.append_row(row)

if __name__ == '__main__':
    main()
