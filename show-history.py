import sqlite3
from tabulate import tabulate

dbHnd = sqlite3.connect('history.db')
dbCursor = dbHnd.cursor()

#	Create the build table if it has not already been created
dbCursor.execute("SELECT * FROM builds ORDER BY id ASC")
rows = cursor.fetchall()

data = []
for row in rows:
	data.append(row)
	
headers = ['id', 'version', 'started_at', 'time_version', 'time_make', 'complete']
print(tabulate(data, headers, tablefmt="fancy_grid"))

dbHnd.close()
