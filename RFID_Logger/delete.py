import interface

connection = interface.database.open_connection('database.db')
connection.delete_table('raw')
connection.delete_table('signIn')
connection.delete_table('times')
connection.close_connection()
