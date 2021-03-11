import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE new_cases
          (id INTEGER PRIMARY KEY ASC, 
           patient_id VARCHAR(250) NOT NULL,
           patient_name VARCHAR(250) NOT NULL,
           case_id INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE newly_vaccinated
          (id INTEGER PRIMARY KEY ASC, 
           patient_id VARCHAR(250) NOT NULL,
           patient_name VARCHAR(250) NOT NULL,
           vaccination_id INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
