import time
import average_each_team, improved, labels, getsheet

q = 'Qualification Responses'

getsheet.open_spreadsheet(q)

timer = time.time()
average_each_team.main(q)
print(time.time() - timer)
# timer = time.time()
# improved.main(q)
# print(time.time() - timer)
timer = time.time()
labels.main(q)
print(time.time() - timer)
