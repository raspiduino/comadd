# ComAdd - Focus app writen in Python
# Copyright @raspiduino on github.com
# Date created 1/11/2020

# Import tk
try:
    # for Python2
    import Tkinter as tk
    from Tkinter import Toplevel, Button, Menu, messagebox
except ImportError:
    # for Python3
    import tkinter as tk
    from tkinter import Toplevel, Button, Menu, messagebox

import os
import admin # https://github.com/raspiduino/pythonadmin
import webbrowser

if not admin.isUserAdmin():
    # Not run as root yet
    if os.name == "nt":
        admin.runAsAdmin("python comadd.py")
    else:
        admin.runAsAdmin("python3 comadd.py")
    exit(1)

# Read setting
# Setting file layout:
# 1. Session time
# 2. Break session time
# 3. Apps to block list
# 4. Sites to block list
# 5. Other settings
settingfile = open("setting.txt", "a+")
settingfile.seek(0) # Read at the top of the file
if settingfile.read() != "":
    settingfile.seek(0) # Read at the top of the file
    # Read session time
    sessiontime = int(settingfile.readline())
    stime_min = sessiontime // 60
    stime_sec = sessiontime % 60
    onesec = 360/sessiontime
    # Read break time
    breaktime = int(settingfile.readline())
    btime_min = breaktime // 60
    btime_sec = breaktime % 60
    # Read apps
    apps = settingfile.readline().split(",")
    # Read sites
    sites = settingfile.readline().split(",")
    # Read other settings
    settings = settingfile.readline().split(",")
# Main app function
def block():
    # Block apps
    for program in apps:
        if os.name == "nt":
            os.spawnl(os.P_DETACH, "C:\\Windows\\System32\\taskkill.exe", "/F /IM " + program) # For Windows
        else:
            os.system("pkill " + program + " &") # For Linux and MacOS
    
# Create GUI
gui = tk.Tk()
gui.iconbitmap("icon.ico")
gui.title("ComAdd v1.0")
gui.geometry('720x360')

# Create main session gui
canvas = tk.Canvas(gui, width=300, height=200)
canvas.pack(fill="both", expand=True)
c0 = canvas.create_oval(260, 30, 460, 230, fill="white")
c1 = canvas.create_arc(260, 30, 460, 230, start=0, extent=0, fill="green")
c2 = canvas.create_oval(280, 50, 440, 210, fill="white")
clock = canvas.create_text(360, 130, font=("Roboto", 24), text=str(stime_min) + ":" + (str(stime_sec) if stime_sec > 9 else "0" + str(stime_sec)))

def start():
    global stime_min, stime_sec
    if not (stime_sec <= 0 and stime_min <= 0):
        block() # Call block function to block apps and sites
        stime_sec -= 1
        if stime_sec < 0:
            stime_sec = 59
            stime_min -= 1
        canvas.itemconfigure(c1, extent=(onesec*(stime_min*60 + stime_sec)))
        canvas.itemconfigure(clock, text=str(stime_min) + ":" + (str(stime_sec) if stime_sec > 9 else "0" + str(stime_sec)))
        gui.after(1000, start)
    else:
        # Time ended, reset time
        messagebox.showinfo("Session ended", "Your session has ended!")
        stime_min = sessiontime // 60
        stime_sec = sessiontime % 60

# Interactive functions
def startsession():
    # Block websites
    if os.name == "nt":
        # Edit Windows host file
        os.system('copy /Y "C:\Windows\System32\drivers\etc\hosts" hosts') # Copy the host file to current directory
        os.system("copy /Y hosts hosts.bck") # Backup host file
    else:
        # Edit Linux/MacOS host file
        os.system("cp -f /etc/hosts hosts") # Copy the host file to current directory
        os.system("cp -f hosts hosts.bck") # Backup host file
    hosts = open("hosts", "a+") # Open and add sites to host file
    hosts.write("\n# This rules created by ComAdd.py in session time\n")
    for site in sites:
        hosts.write("127.0.0.1 " + site)
    hosts.close()
    if os.name == "nt":
        os.system('xcopy /Y hosts "C:\Windows\System32\drivers\etc\"') # Move the host file back
    else:
        os.system("mv -f hosts.edit /etc/hosts")
    # Call start()
    start()
        
def stop():
    # Stop start() function
    global stime_sec, stime_min
    stime_sec = 0
    stime_min = 0
    # Move the orignal host file back
    if os.name == "nt":
        os.system('xcopy /Y hosts.bck "C:\Windows\System32\drivers\etc\hosts"') # Move the host file back
    else:
        os.system("mv -f hosts.bck /etc/hosts")

def exitapp():
    stop()
    exit(0)
    
def blocklist():
    pass
def session():
    pass
def breaksetting():
    pass
def advanced():
    pass
def onlinehelp():
    webbrowser.open_new_tab("https://github.com/raspiduino/comadd/wiki/help")
def about():
    messagebox.showinfo("About", "ComAdd v1.0\nCopyright @raspiduino on github.com\nDate created 1/11/2020")

# Create menubar
menubar = Menu()

# File menu
file = Menu(menubar, tearoff=0)
file.add_command(label="Start session", command=startsession)
file.add_command(label="Stop session", command=stop)
file.add_separator()
file.add_command(label="Exit", command=exitapp)
menubar.add_cascade(label="File", menu=file)

# Statistics menu
statistics = Menu(menubar, tearoff=0)
statistics.add_command(label="Apps usage", command=sapp)
statistics.add_command(label="Web usage", command=sweb)
statistics.add_command(label="Time spend", command=timespend)
menubar.add_cascade(label="Statistics", menu=statistics)

# Setting menu
setting = Menu(menubar, tearoff=0)
setting.add_command(label="Block list", command=blocklist)
setting.add_command(label="Session setting", command=session)
setting.add_command(label="Break setting", command=breaksetting)
setting.add_command(label="Advanced setting", command=advanced)
menubar.add_cascade(label="Setting", menu=setting)

# Help menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Online help", command=onlinehelp)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

gui.configure(menu=menubar)

gui.mainloop()
