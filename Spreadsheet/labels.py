import sys, csv, numpy, pprint
import getsheet

def main(sheet_key):

    spreadsheet = getsheet.open_spreadsheet(sheet_key)
    worksheets = spreadsheet.worksheets()
    for i in range(1, len(worksheets)):
        spreadsheet.del_worksheet(worksheets[i])
    spreadsheet.add_worksheet('Averages', 1, 1)
    responses = worksheets[0]
    output = worksheets[1]
    raw = responses.get_all_values()[1:]

    teams = {}

    imports = (('Match', 2), ('Baseline', 3), ('Auto Switch', 4), ('Auto Scale', 5), ('Switch', 8), ('Scale', 9), ('Opp Switch', 10), ('Exchange', 11), ('Climb', 17))
    labels = ['Team'] + [label[0] for label in imports] + ['Total Switch', 'Total Cube', 'Total Switch & Exchange']

    unlabeled = {}
    for row in raw:
        data = [int(row[label[1]]) if row[label[1]].isdecimal() else 100 if row[label[1]] == 'Crossed' or row[label[1]] == 'Yes' else 0 for label in imports]
        team = int(row[1])
        data += [
        sum(int(row[i]) for i in [8, 10]),
        sum(int(row[i]) for i in range(8, 12)),
        sum(int(row[i]) for i in [8, 10, 11])
        ]
        if team not in unlabeled:
            unlabeled[team] = [data]
        else:
            unlabeled[team].append(data)
    averages = {}

    pprint(unlabeled)
    for team in unlabeled:
        flip = numpy.transpose(unlabeled[team])[1:]
        transpose = [list(row) for row in flip]
        averages[team] = [numpy.mean(row) for row in transpose]
    export = [[team, len(unlabeled[team])] + averages[team] for team in averages]

    export = [labels] + export

    for row in export:
        output.append_row(row)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        sheet_key = sys.argv[1]
    else:
        exit()
    main(sheet_key)
