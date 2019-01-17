import random, time, sqlite3

conn = sqlite3.connect('d.db')

cur = conn.cursor()

for i in range(100):
    cur.execute('CREATE TABLE IF NOT EXISTS random(val REAL)')
    cur.execute('DELETE FROM random')
    conn.commit()

    t = 10
    q = 5
    for i in range(t):
        cur.execute('INSERT INTO random VALUES ({})'.format(random.randrange(q)))
    conn.commit()

    # s = time.time()
    cur.execute('SELECT * FROM random WHERE val={}'.format(random.randrange(q)))
    # print('{}%'.format(round(100 * len(cur.fetchall()) / t, q)))
    # print(time.time() - s)

    cur.execute('SELECT * FROM random')
    # s = time.time()
    l = 0
    for e in cur.fetchall():
        g = random.randrange(q)
        # print(g)
        if e[0] == g:
            l+=1
    # print(time.time() - s)
    # print('{}%'.format(round(100 * l / t, q)))

    a = len(cur.fetchall() / l
conn.close()
