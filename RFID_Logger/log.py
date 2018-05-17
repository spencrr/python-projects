import interface
import datetime, time, random
from pprint import pprint

names = {1: 'Spencer', 2: 'Ethan', 3: 'Brennan', 4: 'John'}
def simulate_data():
    connect = interface.database.open_connection('database.db')
    connect.delete_table('raw')
    raw = connect.create_table('raw', 'id, timestamp', 'REAL, REAL')
    log = []
    for id in range(1, 5):
        for j in range(60):
            log.append((id, j * 3600))
            log.append((id, (pow() + 50) * 3600))
    for id, timestamp in log:
        raw.insert_entry((id, round(timestamp, 0)))

def main():
    connect = interface.database.open_connection('database.db')
    raw = connect.create_table('raw', 'id, timestamp', 'REAL, REAL')
    signIn = connect.create_table('signIn', 'id, timeIn, timeOut, seconds', 'REAL, REAL, REAL, REAL')
    times = connect.create_table('times', 'id, hours', 'REAL, REAL')
    last = {}
    for id, timestamp in raw.select_entries():
        if id not in last:
            last[id] = timestamp
        else:
            if len(signIn.select_entries(conditions='id={} AND timeIn={} AND timeOut={}'.format(id, last[id], timestamp))) == 0:
                signIn.insert_entry((id, last[id], timestamp, timestamp-last[id]))
            del(last[id])

    total = {}
    for id, seconds in signIn.select_entries(to_select='id, seconds'):
        if id not in total:
            total[id] = seconds
        else:
            total[id] += seconds

    times_list = [tup[0] for tup in times.select_entries()]
    for id, seconds in total.items():
        total[id] = round(seconds / 3600, 1)
        if id not in times_list:
            times.insert_entry((id, total[id]))
    for id, hours in times.select_entries():
        if total[id] != hours:
            times.update_entries('hours={}'.format(total[id]), conditions='id={}'.format(id))

    print(signIn)
    connect.close_connection()

if __name__ == '__main__':
    simulate_data()
    main()
    times = []
    for i in range(1):
        t = time.time()
        main()
        t = round(time.time() - t, 5)
        times.append(t)
    print('avg: {}'.format(sum(times)/len(times)))
