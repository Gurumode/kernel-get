import sqlite3
from tabulate import tabulate

dbHnd = sqlite3.connect('history.db')
dbCursor = dbHnd.cursor()

#	Create the build table if it has not already been created
dbCursor.execute("SELECT * FROM builds ORDER BY id ASC")
rows = dbCursor.fetchall()

data = []
for row in rows:
	rowData = []
	rowData['id'] = row['id']
	rowData["version"] = row["version"]
	
	dt = datetime.datetime.fromtimestamp(row["started_at"])
	prettyDate = dt.strftime("%Y-%m-%d %H:%M:%S")
	row["started_at"] = prettyDate
	
	rowData["time_version"] = row["time_version"]
	
	rowData["time_make"] = str(row[4] // 3600) + ":" + str((row[4] % 3600) // 60) + ":" + str((row[4] % 3600) % 60)
	
	rowData["complete"] = row["complete"]
	
	data.append(row)
	
headers = ['id', 'version', 'started_at', 'time_version', 'time_make', 'complete']
print(tabulate(data, headers, tablefmt="fancy_grid"))

dbHnd.close()
