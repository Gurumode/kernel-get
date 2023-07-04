import os
import requests
import time
import shutil
import sqlite3
import subprocess
import sys
from bs4 import BeautifulSoup

#	Create a few variables to track how long each step takes.
time_version = 0
time_make = 0

#	Globals
dbHnd = ""
dbCursor = ""

def cleanEnvironment():
	#	Clean up the build environment.  This includes removing any pkg and src
	#	directories.  It also includes copying the kernel configuration.
	
	if not os.path.exists("linux-bpir64-gurumode"):
		print("pkgbuild information is missing.")
		sys.exit(1)
	
	for filename in os.listdir("linux-bpir64-gurumode"):
		if filename.endswith(".tar.xz"):
			file_path = os.path.join("linux-bpir64-gurumode", filename)
			os.remove(file_path)
	
	if os.path.exists("linux-bpir64-gurumode/src"):
		shutil.rmtree("linux-bpir64-gurumode/src")
	
	if os.path.exists("linux-bpir64-gurumode/pkg"):
		shutil.rmtree("linux-bpir64-gurumode/pkg")
		
	#	Copy the kernel configuration
	with open("config/kernel.config", 'r') as file:
		kernelConfig = file.read()
	
	with open("linux-bpir64-gurumode/defconfig", 'w') as file:
		file.write(kernelConfig)

def check_latest_kernel():
	start_time = time.time()
	global time_version
	
	url = "https://www.kernel.org/"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	try:
		version_element = soup.select_one("#latest_link")
		latest_version = version_element.get_text(strip=True)
		latest_link = version_element.find('a')
		latest_tarball = "linux-" + latest_version + ".tar.xz"
		
		if latest_link:
			link = latest_link['href']
			#print("Link: ", link)
		else:
			print("No download link found.")
			sys.exit(1)

	except Exception as e:
			print("Error:", e)
			sys.exit(1)
	
	time_version = time.time() - start_time
	
	return latest_version, link
	

def make_build(version):
	start_time = time.time()
	global time_make
	
	#subprocess.call(["bash", "make.sh", version])
	subprocess.call(['makepkg', '-c'], cwd="linux-bpir64-gurumode")
	
	time_make = time.time() - start_time
	
def config_database():
	global dbHnd
	global dbCursor
	
	dbHnd = sqlite3.connect('history.db')
	dbCursor = dbHnd.cursor()
	
	#	Create the build table if it has not already been created
	dbCursor.execute('''CREATE TABLE IF NOT EXISTS builds (
						id INTEGER PRIMARY KEY,
						version TEXT,
						started_at INTEGER,
						time_version INTEGER,
						time_make INTEGER,
						complete INTEGER
					)''')
	dbHnd.commit()
	
def generate_Pkgbuild(version):
	with open("pkgbuild-template", 'r') as file:
		pbtemplate = file.read()
		
	pbtemplate = pbtemplate.replace("[KERNELVERSION]", version)
	
	with open("linux-bpir64-gurumode/PKGBUILD", 'w') as file:
		file.write(pbtemplate)

################################################################################
#
#	Code and stuff
#
################################################################################

#	First, check that the local database has been configured
config_database()

version, link = check_latest_kernel()
print("Kernel Version: ", version)
print("Kernel Link: ", link)

#	Check the newest kernel version with the most recently built kernel
dbCursor.execute("SELECT * FROM builds ORDER BY id DESC LIMIT 1")
recent = dbCursor.fetchone()

if recent is None or recent["version"] is not version:
	print("Kernel appears to be new.")
else:
	print("No update.")
	sys.exit(0)

#	Create a database entry for this kernel version so that it isn't built
#	multiple times.
dbCursor.execute("INSERT INTO builds (version, started_at, time_version) VALUES (?, ?, ?)", (version, time.time(), time_version))
dbHnd.commit()
row_id = dbCursor.lastrowid

#	Clean up the environment
cleanEnvironment()

#	Now we need to copy the pkgbuild template to the build directory.
generate_Pkgbuild(version)

#	Run makepkg on the new pkgbuild
make_build(version)
dbCursor.execute("UPDATE builds SET time_make = ? WHERE id = ?", [time_make, row_id])
dbHnd.commit()

#	Packages are built.  These will need to be added to the repo
#	The process for that comes later tonight






