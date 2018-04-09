import sys, csv, numpy
from pprint import pprint
import getsheet

def main(sheet_key, input_title, output_title):
    label_ranges = (('Team', [1]), ('Match', [3]), ('Baseline', [2]), ('Auto Switch', [4]), ('Auto Scale', [5]),
        ('Switch', [8]), ('Scale', [9]), ('Opp Switch', [10]), ('Exchange', [11]), ('Climb', [17]),
        ('Total Switch', [8, 10]), ('Total Switch & Exchange', [8, 10, 11]), ('Total Cube', [8, 9, 10, 11]))
    labels = [label[0] for label in label_ranges]
    spreadsheet = getsheet.open_spreadsheet(sheet_key)
    worksheets = spreadsheet.worksheets()
    responses = spreadsheet.worksheet(input_title)
    output_sheet = None
    for worksheet in worksheets:
        if worksheet.title == output_title:
            output_sheet = worksheet
            break
    if not output_sheet:
        output_sheet = spreadsheet.add_worksheet(output_title, 1, 1)
    raw = responses.get_all_values()[1:]

    teams = {}

    for row in raw:
        data = [sum(int(row[i]) if row[i].isdecimal() else 100 if row[i] == 'Crossed' or row[i] == 'Yes'
                else row[i] if label[1] == 'Team' else 0 for i in label[1]) for label in label_ranges]
        team = data[0]
        data = data[1:]
        if team not in teams:
            teams[team] = [data]
        else:
            teams[team].append(data)

    averages = {}
    for team in teams:
        flip = numpy.transpose(teams[team])[1:]
        transpose = [list(row) for row in flip]
        averages[team] = [numpy.mean(row) for row in transpose]
    export = [labels] + [[team, len(teams[team])] + averages[team] for team in averages]

    row_len = len(export)
    col_len = len(labels)

    pprint(export)

    write_sheet(output_sheet, export, row_len, col_len)

def write_sheet(output_sheet, data_matrix, row_len, col_len):
    cell_list = output_sheet.range(1, 1, row_len, col_len)
    index = 0
    for cell in cell_list:
        row = index // col_len
        col = index % col_len
        cell.value = data_matrix[row][col]
        index+=1
    output_sheet.update_cells(cell_list)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        sheet_key = sys.argv[1]
        input_title = sys.argv[2] if len(sys.argv) >= 3 else 'Responses'
        output_title = sys.argv[3] if len(sys.argv) >= 4 else 'Averages'
    else:
        exit()
    main(sheet_key, input_title, output_title)
