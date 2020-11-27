import time
import os
from datetime import date

atime = 0
appdict = {}

# Get the active window name
if os.name == "nt":
    import win32gui
    currentw = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    lastw = currentw
    while True:
        currentw = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if lastw != currentw:
            if not lastw in appdict:
                appdict[lastw[:20]] = atime # Add to dict
            else:
                appdict[lastw[:20]] += atime # Add the time to existed name
            # Save to log
            logfile = open("logs\\applog"+date.today().strftime("%d%m%y")+".txt", "a+")
            logfile.write(str(appdict) + "\n")
            logfile.close()
            atime = 0
        time.sleep(1)
        atime += 1 # Keep counting
        lastw = currentw
else:
    import subprocess
    currentw = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
    lastw = currentw
    while True:
        currentw = subprocess.check_output(['xdotool', 'getactivewindow', 'getwindowname'])
        if lastw != currentw:
            if not lastw in appdict:
                appdict[lastw[:20]] = atime # Add to dict
            else:
                appdict[lastw[:20]] += atime # Add the time to existed name
            # Save to log
            logfile = open("logs\\applog"+date.today().strftime("%d%m%y")+".txt", "a+")
            logfile.write(str(appdict) + "\n")
            logfile.close()
            atime = 0
        time.sleep(1)
        atime += 1 # Keep counting
        lastw = currentw
