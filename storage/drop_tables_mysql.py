import mysql.connector
db_conn = mysql.connector.connect(host="acit3855lab6.eastus.cloudapp.azure.com", user="user", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE new_cases, newly_vaccinated
''')
db_conn.commit()
db_conn.close()