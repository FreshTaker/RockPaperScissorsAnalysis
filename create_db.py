"""Create the SQL database table"""
import sqlite3

def create_database_table(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS scorecard(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                score INTEGER DEFAULT 0)''')
    conn.commit()




file_name = 'rockpaperscissors.s3db'
create_database_table(file_name)