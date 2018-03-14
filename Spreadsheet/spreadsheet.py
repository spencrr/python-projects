import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import numpy
import csv

printer = pprint.PrettyPrinter()

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# sheet = client.open('CSV').sheet1
spreadsheet = client.open_by_key('13HodOGfmyhfA10e2AFPz5dDQXoQCIP1EsPX08yYvLC0')
sheet = spreadsheet.get_worksheet(0)
export_sheet = spreadsheet.get_worksheet(1)
# export_sheet.clear()

out = sheet.get_all_records()
team_col = sheet.col_values(2)
match_col = sheet.col_values(3)

baseline_col_str = sheet.col_values(4)
baseline_col = []
for i in range(len(baseline_col_str)):
    result = baseline_col_str[i]
    baseline_col.append(1 if result == u'Crossed' else 0)

auto_switch_col = sheet.col_values(5)
auto_scale_col = sheet.col_values(6)
auto_exchange_col = sheet.col_values(7)

drop_cube_col_str = sheet.col_values(8)
drop_cube_col = []
for i in range(len(drop_cube_col_str)):
    result = drop_cube_col_str[i]
    drop_cube_col.append(1 if result == u'Yes' else 0)

tele_switch_col = sheet.col_values(9)
tele_opp_switch_col = sheet.col_values(10)
tele_scale_col = sheet.col_values(11)
tele_exchange_col = sheet.col_values(12)
tele_drop_col = sheet.col_values(13)
# defense_col_str = sheet.col_values(14)
# defense_col = []
# for i in range(len(defense_col_str)):
#     result = defense_col_str[i]
#     defense_col.append(1 if result == u'Yes' else 0
# against_defense_col_str = sheet.col_values(15)
# against_defense_col = []
# for i in range(len(against_defense_col_str)):
#     result = against_defense_col_str[i]
#     against_defense_col.append(1 if result == u'Yes' else 0
# # against_defense_col_str
# # park_col_str
# # climb_col_str

teams = []
data = []
export = []

for i in range(len(team_col)):
    if i > 0:
        team = int(team_col[i])
        if team not in teams:
            teams.append(team)
            data.append([team, []])
        index = teams.index(team)
        match = int(match_col[i])
        for entry in data[index][1]:
            if entry[0] == match:
                print('duplicate match found with team ', team, ' on match ', match)
        crossed = baseline_col[i]
        auto_switch = int(auto_switch_col[i])
        auto_scale = int(auto_scale_col[i])
        auto_exchange = int(auto_exchange_col[i])
        drop_cube = int(drop_cube_col[i])
        tele_switch = int(tele_switch_col[i])
        tele_opp_switch = int(tele_opp_switch_col[i])
        tele_scale = int(tele_scale_col[i])
        tele_exchange = int(tele_exchange_col[i])

        total_switch = sum([tele_switch, tele_opp_switch])
        total_cube = sum([tele_switch, tele_opp_switch,
        tele_scale, tele_exchange])

        data[index][1].append(
        [match, crossed, auto_switch, auto_scale, auto_exchange, drop_cube,
        tele_switch, tele_opp_switch, tele_scale, tele_exchange, total_switch,
        total_cube])

export.append(['Team', 'Crossed %', 'Avg Auto Switch',
'Avg Auto Scale', 'Avg Auto Exchange', 'Avg Auto Dropped Cubes',
'Avg Tele Scale', 'Avg Tele Exchange', 'Avg Total Switches',
'Avg Total Cubes'])
for entry in data:
    team = entry[0]
    metadata = entry[1]
    crossed = []
    auto_switch = []
    auto_scale = []
    auto_exchange = []
    drop_cube = []
    tele_scale = []
    tele_exchange = []
    total_switch = []
    total_cube = []

    for match in metadata:
        crossed.append(match[1])
        auto_switch.append(match[2])
        auto_scale.append(match[3])
        auto_exchange.append(match[4])
        drop_cube.append(match[5])
        tele_scale.append(match[8])
        tele_exchange.append(match[9])
        total_switch.append(match[10])
        total_cube.append(match[11])

    avg_crossed = numpy.mean(crossed)
    avg_auto_switch = numpy.mean(auto_switch)
    avg_auto_scale = numpy.mean(auto_scale)
    avg_auto_exchange = numpy.mean(auto_exchange)
    avg_drop_cube = numpy.mean(drop_cube)
    avg_tele_scale = numpy.mean(tele_scale)
    avg_tele_exchange = numpy.mean(tele_exchange)
    avg_total_switch = numpy.mean(total_switch)
    avg_total_cube = numpy.mean(total_cube)

    export.append([team, avg_crossed, avg_auto_switch,
    avg_auto_scale, avg_auto_exchange, avg_drop_cube,
    avg_tele_scale, avg_tele_exchange, avg_total_switch, avg_total_cube])

# printer.pprint(export)

with open('export.csv', 'w') as f:
    wr = csv.writer(f)
    for row in export:
        wr.writerow(row)

exisiting_teams = export_sheet.col_values(1)
for index in range(len(export)):
    row = export[index]
    if not str(row[0]) in exisiting_teams:
        export_sheet.insert_row(row, index+1)
