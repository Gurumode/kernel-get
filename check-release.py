import getpass
import os
import requests
import time
import subprocess
import sys
from bs4 import BeautifulSoup

#downloadDir = "/home/" + getpass.getuser() + "/Code/kernel-get/Downloads"
downloadDir = "Downloads"

def check_latest_kernel():
	url = "https://www.kernel.org/"
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	try:
		version_element = soup.select_one("#latest_link")
		latest_version = version_element.get_text(strip=True)
		latest_link = version_element.find('a')
		latest_tarball = "linux-" + latest_version + ".tar.xz"
		
		print("Latest kernel version:", latest_version)
		
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
	download_file(link, downloadDir + "/" + latest_tarball)
	return latest_version, link

def create_directory(directory_path):
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)
	

def download_file(url, save_path):
	create_directory(downloadDir)
	response = requests.get(url)
	with open(save_path, 'wb') as file:
		file.write(response.content)

start_time = time.time()
version, link = check_latest_kernel()
print("Version: ", version)
print("Link: ", link)
time_version = time.time() - start_time


#	This is where we need to check if the latest version is newer than the
#	previously compiled version.  If so, then it needs to be downloaded,
#	extracted, and built.

#	For now, we assume it is newer
start_time = time.time()
tarball = "linux-" + version + ".tar.xz"
download_file(link, downloadDir + "/" + tarball)
time_download = time.time() - start_time

start_time = time.time()
subprocess.call(["bash", "extract.sh", version])
time_extract = time.time() - start_time

start_time = time.time()
subprocess.call(["bash", "config.sh", version])
time_config = time.time() - start_time

start_time = time.time()
subprocess.call(["bash", "make.sh", version])
time_make = time.time() - start_time

print("Kernel successfully built.")
print(f"Check:\t\t{time_version}")
print(f"Download:\t{time_download}")
print(f"Extract:\t{time_extract}")
print(f"Config:\t\t{time_config}")
print(f"Make:\t\t{time_make}")
