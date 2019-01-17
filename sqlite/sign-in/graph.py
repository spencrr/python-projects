import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

import interface
import log
from pprint import pprint

log.main()

c = interface.database.open_connection('database.db')
signIn = c.create_table('signIn', 'id, timeIn, timeOut, seconds', 'REAL, REAL, REAL, REAL')

ids = []
for id in signIn.select_entries(to_select='id'):
    if id not in ids:
        ids.append(id)
        a, b = [], []
        for timeIn, timeOut, second in signIn.select_entries(
        to_select='timeIn, timeOut, seconds', conditions='id={}'.format(id[0])):
            a.append((timeIn + timeOut) / 2)
            b.append(second)
        plt.plot(a, b, label=log.names[id[0]])
plt.legend()
plt.show()
