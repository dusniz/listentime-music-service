import sqlite3

connection = sqlite3.connect('music.db')
cursor = connection.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS Tracks (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL
               )
               ''')

connection.commit()
connection.close()
