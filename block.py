# ComAdd - Focus app writen in Python
# Copyright @raspiduino on github.com
# Date created 1/11/2020

import os
import time

settingfile = open("setting.txt", "r")
settingfile.seek(0)
for i in range(2):
    settingfile.readline()
apps = settingfile.readline().split(",")

# Block apps
while True:
    for program in apps:
        if os.name == "nt":
            os.system('taskkill.exe /F /IM "' + program + '"') # For Windows
        else:
            os.system('pkill "' + program + '"') # For Linux and MacOS
    time.sleep(10)
