import sys
import csv
import numpy
from pprint import pprint
from time import time
import getsheet


def main(sheet_key, input_title, output_title):
    start = time()

    label_ranges = (('Team', [1]), ('Match', [2]), ('Baseline', [3]), ('Auto Switch', [4]), ('Auto Scale', [5]), ('Switch', [7]), ('Scale', [8]), ('Opp Switch', [
                    9]), ('Exchange', [10]), ('Climb', [11]), ('Total Switch', [7, 9]), ('Total Switch & Exchange', [7, 9, 10]), ('Total Cube', [7, 8, 9, 10]))

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

    filtered = {}
    for team in teams:
        if not len(teams[team]) < 3 or True: ## REVIEW:
            filtered[team] = teams[team]
            matches = {}
            for match in teams[team]:
                num = match[0]
                if num not in matches:
                    matches[num] = 1
                else:
                    matches[num] += 1
            for num in matches:
                if matches[num] > 1:
                    print('{} has {} match {}'.format(team, matches[num], num))

    averages = {}
    for team in filtered:
        flip = numpy.transpose(filtered[team])[1:]
        transpose = [list(row) for row in flip]
        averages[team] = [numpy.mean(row) for row in transpose]
    export = [labels] + [[team, len(filtered[team])] + averages[team] for team in averages]

    row_len = len(export)
    col_len = len(labels)
    write_sheet(output_sheet, export, row_len, col_len)
    print('Finished in {} sec'.format(time() - start))


def write_sheet(output_sheet, data_matrix, row_len, col_len):
    output_sheet.clear()
    output_sheet.resize(2, 2)
    cell_list = output_sheet.range(1, 1, row_len, col_len)
    index = 0
    for cell in cell_list:
        row = index // col_len
        col = index % col_len
        cell.value = data_matrix[row][col]
        index += 1
    output_sheet.update_cells(cell_list)


if __name__ == '__main__':
    sheet_key = sys.argv[1] if len(
        sys.argv) >= 2 else 'Qualification Responses'
    input_title = sys.argv[2] if len(sys.argv) >= 3 else 'Responses'
    output_title = sys.argv[3] if len(sys.argv) >= 4 else 'Averages'
    if(sys.argv[1] == '-f'):
        sheet_key = 'Detroit National Qualification Match Scouting Form (Responses)'
        input_title = 'Form Responses 1'
    main(sheet_key, input_title, output_title)
