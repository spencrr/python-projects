import sqlite3

def to_sql_verbose(names, types):
    names = names.split(', ')
    types = types.split(' ')
    l = len(names)
    if(l == len(types)):
        return ''.join(['{} {} '.format(names[i], types[i]) for i in range(l)])

class database:
    class table:
        def __init__(self, name, data_name, data_type):
            self.name = name
            self.data_name = data_name
            self.data_type = data_type

    def __init__(self, connection):
        self.connection = connection

    def open_connection(name):
        connection = sqlite3.connect(name)
        return database(connection)

    def close_connection(self):
        self.connection.cursor().close()
        self.connection.close()

    def create_table(self, name, data_name, data_type):
        table = self.table(name, data_name, data_type)
        self.connection.cursor().execute('CREATE TABLE IF NOT EXISTS {}({})'.format(table.name, to_sql_verbose(table.data_name, table.data_type)))
        return table

    def delete_table(self, table):
        if isinstance(table, self.table):
            table = table.name
        self.connection.cursor().execute('DROP TABLE IF EXISTS {}'.format(table))

    def insert_entry(self, table, data, data_name=None):
        if not data_name:
            data_name = table.data_name
        if(len(data) != 0):
            if(len(data) <= 1):
                data = str(data).replace(',', '')
            self.connection.cursor().execute('INSERT INTO {} ({}) VALUES {}'.format(table.name, data_name, data))
            self.connection.commit()

    def select_entries(self, table, to_select='*', conditions=''):
        if (conditions != ''):
            conditions = 'WHERE ' + conditions
        c = self.connection.cursor()
        c.execute('SELECT {} FROM {} {}'.format(to_select, table.name, conditions))
        return c.fetchall()

    def delete_entries(self, table, conditions=''):
        if (conditions != ''):
            conditions = 'WHERE ' + conditions
        self.connection.cursor().execute('DELETE FROM {} {}'.format(table.name, conditions))

    def print_all_entries(self, table):
        print('Entries in {}:'.format(table.name))
        for row in self.select_entries(table):
            print(row)
        print()
