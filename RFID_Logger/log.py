import interface
import datetime, time, random
from pprint import pprint
def main():
    names = {1: 'Spencer', 2: 'Ethan', 3: 'Brennan'}
    log = [(1, 3600), (2, 12000), (3, 18000), (1, 3600 * 2), (2, 12000 * 2), (3, 18000 * 2)]

    connect = interface.database.open_connection('database.db')
    connect.delete_table('rawLog')
    connect.delete_table('timeLog')
    rawLog = connect.create_table('rawLog', 'id, timestamp', 'REAL, REAL')
    for i in range(2):
        for id, timestamp in log:
            connect.insert_entry(rawLog, (id, round(i * timestamp, 0)))
    connect.print_all_entries(rawLog)
    signInLog = connect.create_table('signInLog', 'id, timeIn, timeOut, timeLength', 'REAL, REAL, REAL, REAL')

    users = []
    for id, timestamp in log:
        if id not in users:
            users.append(id)
            sign_in = None
            sign_out = None
            for entry in connect.select_entries(rawLog, to_select='timestamp', conditions='id={}'.format(id)):
                entry = entry[0]
                if not sign_in:
                    sign_in = entry
                else:
                    sign_out = entry
                    logTime = sign_out - sign_in
                    if len(connect.select_entries(signInLog, conditions='timeIn={}'.format(sign_in))) == 0:
                        connect.insert_entry(signInLog, (id, sign_in, sign_out, logTime))
                    sign_out = None
                    sign_in = None

    connect.print_all_entries(signInLog)
    timeLog = connect.create_table('timeLog', 'name, hours', 'TEXT, REAL')
    users = {}
    for id, timeLength in connect.select_entries(signInLog, to_select='id, timeLength'):
        name = names[id]
        if name not in users:
            users[name] = timeLength
        else:
            users[name] += timeLength
    for user, seconds in users.items():
        connect.insert_entry(timeLog, (user, round(seconds / 3600, 1)))

    connect.print_all_entries(timeLog)
    connect.close_connection()

if __name__ == '__main__':
    main()
