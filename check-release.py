import getpass
import os
import requests
import time
import shutil
import sqlite3
import subprocess
import sys
from bs4 import BeautifulSoup

#downloadDir = "/home/" + getpass.getuser() + "/Code/kernel-get/Downloads"
downloadDir = "Downloads"
buildPrefix = "linux-"
buildSuffix = "-bpi-gurumode"

#	Create a few variables to track how long each step takes.
time_version = 0
time_download = 0
time_extract = 0
time_config = 0
time_make = 0

#	Globals
dbHnd = ""
dbCursor = ""

def cleanEnvironment():
	#	We need to remove any of the build artifacts
	#		pkgbuild
	#			src
	#			pkg
	
	if not os.path.exists("linux-bpir64-gurumode"):
		print("pkgbuild information is missing.")
		sys.exit(1)
	
	for filename in os.listdir("linux-bpi64-gurumode"):
		if filename.endswith(".tar.xz"):
			file_path = os.path.join("linux-bpi64-gurumode", filename)
			os.remove(file_path)
	

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
	
	create_directory(downloadDir)
	#download_file(link, downloadDir + "/" + latest_tarball)
	
	time_version = time.time() - start_time
	
	return latest_version, link

def create_directory(directory_path):
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)
	

def download_file(url, save_path):
	start_time = time.time()
	global time_download
	
	create_directory(downloadDir)
	response = requests.get(url)
	with open(save_path, 'wb') as file:
		file.write(response.content)

	time_download = time.time() - start_time


def extract_tarball(version):
	start_time = time.time()
	global time_extract
	
	subprocess.call(["bash", "extract.sh", version])
	
	time_extract = time.time() - start_time


def config_build(version):
	start_time = time.time()
	global time_config
	
	subprocess.call(["bash", "config.sh", version])
	
	time_config = time.time() - start_time


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
	
	with open("linux-bpi64-gurumode/PKGBUILD", 'w') as file:
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

#	Now we need to copy the pkgbuild template to the build directory.
generate_Pkgbuild(version)

#	Run makepkg on the new pkgbuild
make_build(version)
dbCursor.execute("UPDATE builds SET time_make = ? WHERE id = ?", [time_make, row_id])
dbHnd.commit()

#	Packages are built.  These will need to be added to the repo
#	The process for that comes later tonight

#	Exit for now while testing.
sys.exit(0)

#	For now, we assume it is newer
tarball = "linux-" + version + ".tar.xz"
download_file(link, downloadDir + "/" + tarball)

extract_tarball(version)
config_build(version)
make_build(version)


print("Kernel successfully built.")
print(f"Check:\t\t{time_version}")
print(f"Download:\t{time_download}")
print(f"Extract:\t{time_extract}")
print(f"Config:\t\t{time_config}")
print(f"Make:\t\t{time_make}")
