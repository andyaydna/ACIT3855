import sqlite3
import mysql.connector

conn = sqlite3.connect('readings.sqlite')

db_conn = mysql.connector.connect(host="acit3855lab6.eastus.cloudapp.azure.com", user="user", password="password", database="events")

db_cursor = db_conn.cursor()

# c = conn.cursor()

db_cursor.execute('''
          CREATE TABLE new_cases
          (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
           patient_id VARCHAR(250) NOT NULL,
           patient_name VARCHAR(250) NOT NULL,
           case_id INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

db_cursor.execute('''
          CREATE TABLE newly_vaccinated
          (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
           patient_id VARCHAR(250) NOT NULL,
           patient_name VARCHAR(250) NOT NULL,
           vaccination_id INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

# conn.commit()
# conn.close()

db_conn.commit()
db_conn.close()
