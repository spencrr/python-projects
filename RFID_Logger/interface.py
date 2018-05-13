import sqlite3

def to_sql_verbose(names, types):
    names = names.split(', ')
    types = types.split(' ')
    l = len(names)
    if(l == len(types)):
        return ''.join(['{} {} '.format(names[i], types[i]) for i in range(l)])

class database:

    def __init__(self, connection):
        self.connection = connection

    def open_connection(name):
        connection = sqlite3.connect(name)
        return database(connection)

    def close_connection(self):
        self.connection.cursor().close()
        self.connection.close()

    def create_table(self, name, data_name, data_type):
        table = self.table(name, data_name, data_type, self)
        self.connection.cursor().execute('CREATE TABLE IF NOT EXISTS {}({})'.format(table.name, to_sql_verbose(table.data_name, table.data_type)))
        return table

    def delete_table(self, table):
        if isinstance(table, self.table):
            table = table.name
        self.connection.cursor().execute('DROP TABLE IF EXISTS {}'.format(table))

    class table:
        def __init__(self, name, data_name, data_type, database):
            self.name = name
            self.data_name = data_name
            self.data_type = data_type
            self.database = database

        def insert_entry(self, data, data_name=None):
            if not data_name:
                data_name = self.data_name
            if(len(data) != 0):
                if(len(data) <= 1):
                    data = str(data).replace(',', '')
                self.database.connection.cursor().execute('INSERT INTO {} ({}) VALUES {}'.format(self.name, data_name, data))
                self.database.connection.commit()
            return data

        def update_entries(self, data, conditions=''):
            if (conditions != ''):
                conditions = 'WHERE ' + conditions
            self.database.connection.cursor().execute('UPDATE {} SET {} {}'.format(self.name, data, conditions))
            self.database.connection.commit()

        def select_entries(self, to_select='*', conditions=''):
            if (conditions != ''):
                conditions = 'WHERE ' + conditions
            c = self.database.connection.cursor()
            c.execute('SELECT {} FROM {} {}'.format(to_select, self.name, conditions))
            return c.fetchall()

        def delete_entries(self, conditions=''):
            if (conditions != ''):
                conditions = 'WHERE ' + conditions
            self.database.connection.cursor().execute('DELETE FROM {} {}'.format(self.name, conditions))

        def __str__(self):
            s = ('Entries in {}:'.format(self.name))
            for row in self.select_entries():
                s += str(row) + '\n'
            return(s)
