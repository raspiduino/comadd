# ComAdd - Focus app writen in Python
# Copyright @raspiduino on github.com
# Date created 1/11/2020

# Import ttk
try:
    # for Python2
    import Tkinter as tk
    from Tkinter import Toplevel, Button, Menu, messagebox
    from Tkinter import ttk

except ImportError:
    # for Python3
    import tkinter as tk
    from tkinter import Toplevel, Button, Menu, messagebox
    from tkinter import ttk

import os
import admin # https://github.com/raspiduino/pythonadmin
import webbrowser
import time
import subprocess

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
    bonesec = 360/breaktime
    # Read apps
    apps = settingfile.readline()[:-1].split(",")
    # Read sites
    sites = settingfile.readline()[:-1].split(",")
    # Read other settings
    settings = settingfile.readline()[:-1].split(",")

settingfile.close()

def advsetexec():
    global settings, setting, file, menubar

    if settings[0] == "0":
        setting.entryconfig("Advanced setting", state="disabled")
    else:
        setting.entryconfig("Advanced setting", state="normal")

    for apptup in [(3, "cmd.exe"), (4, "taskmgr.exe"), (5, "powershell.exe"), (8, "control.exe"), (8, "SystemSettings.exe")]:
        i, appblock = apptup
        if settings[i] == "1":
            if not appblock in apps:
                apps.append(appblock)
        else:
            if appblock in apps:
                apps.remove(appblock) 

# Function to rewrite the setting file
def wsetting():
    os.remove("setting.txt")
    settingfile = open("setting.txt", "a+")
    settingfile.write(str(sessiontime) + "\n" + str(breaktime) + "\n" + ",".join(apps) + "\n" + ",".join(sites) + "\n" + ",".join(settings))
    settingfile.close()

def breakclock():
    global btime_min, btime_sec
    if not (btime_sec <= 0 and btime_min <= 0):
        btime_sec -= 1
        if btime_sec < 0:
            btime_sec = 59
            btime_min -= 1
        canvas.itemconfigure(c1, extent=(bonesec*(btime_min*60 + btime_sec)))
        canvas.itemconfigure(clock, text=str(btime_min) + ":" + (str(btime_sec) if btime_sec > 9 else "0" + str(btime_sec)))
        gui.after(1000, breakclock)

    else:
        btime_min = breaktime // 60
        btime_sec = breaktime % 60
        messagebox.showinfo("End of breaktime!", "Back to your work!")
        startsession()

def takebreak():
    messagebox.showinfo("Break time!", "Enjoy your breaktime now!")
    canvas.itemconfigure(c1, fill="Blue", extent=360)
    canvas.itemconfigure(clock, text=str(btime_min) + ":" + (str(btime_sec) if btime_sec > 9 else "0" + str(btime_sec)))
    # Stop the block
    subprocess.Popen.terminate(blockapp) # Kill the block.py
    # Move the orignal host file back
    if os.name == "nt":
        os.system('xcopy /Y hosts.bck "C:\Windows\System32\drivers\etc\hosts"') # Move the host file back
    else:
        os.system("mv -f hosts.bck /etc/hosts")

    file.entryconfig("Stop session", state="normal")
    file.entryconfig("Exit", state="normal")
    menubar.entryconfig("Setting", state="normal")
    os.chmod("comadd.py", stat.S_IRWXU)
    os.chmod("setting.txt", stat.S_IRWXU)
    breakclock()

# Clock timeout function
def startclock():
    global stime_min, stime_sec, blockapp
    if not (stime_sec <= 0 and stime_min <= 0):
        stime_sec -= 1
        if stime_sec < 0:
            stime_sec = 59
            stime_min -= 1
        canvas.itemconfigure(c1, extent=(onesec*(stime_min*60 + stime_sec)))
        canvas.itemconfigure(clock, text=str(stime_min) + ":" + (str(stime_sec) if stime_sec > 9 else "0" + str(stime_sec)))
        
        if ((stime_min*60 + stime_sec) == (sessiontime//2)) and (settings[2] == "0"):
            # Breaktime
            takebreak()

        gui.after(1000, startclock)

    else:
        # Time ended, reset time
        global mainbutton
        mainbutton.config(image=mainbuttonimg, command=startsession)
        messagebox.showinfo("Session ended", "Your session has ended!")
        stop()
        #advsetexec()
        subprocess.Popen.terminate(blockapp) # Kill the block.py
        stime_min = sessiontime // 60
        stime_sec = sessiontime % 60

# Interactive functions
def startsession():
    advsetexec()

    # Advanced block
    if settings[6] == "1":
        file.entryconfig("Stop session", state="disabled")
        file.entryconfig("Exit", state="disabled")

    if settings[7] == "1":
        menubar.entryconfig("Setting", state="disabled")

    if settings[9] == "1":
        os.chmod("comadd.py", stat.S_IREAD)
        os.chmod("setting.txt", stat.S_IREAD)

    global mainbutton
    mainbutton.config(image=mainbuttonrun, command=stop)

    global blockapp
    if os.name == "nt":
        blockapp = subprocess.Popen(['python', 'block.py'])
        # Edit Windows host file
        os.system('copy /Y "C:\Windows\System32\drivers\etc\hosts" hosts') # Copy the host file to current directory
        os.system("copy /Y hosts hosts.bck") # Backup host file
    else:
        blockapp = subprocess.Popen(['python3', 'block.py'])
        # Edit Linux/MacOS host file
        os.system("cp -f /etc/hosts hosts") # Copy the host file to current directory
        os.system("cp -f hosts hosts.bck") # Backup host file

    hosts = open("hosts", "a+") # Open and add sites to host file
    hosts.write("\n# This rules created by ComAdd.py in session time\n")
    for site in sites:
        hosts.write("127.0.0.1 " + site + "\n")
    hosts.close()

    if os.name == "nt":
        os.system('xcopy /Y hosts "C:\Windows\System32\drivers\etc\"') # Move the host file back
    else:
        os.system("mv -f hosts.edit /etc/hosts")
    # Call startclock()
    startclock()
        
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

    file.entryconfig("Stop session", state="normal")
    file.entryconfig("Exit", state="normal")
    menubar.entryconfig("Setting", state="normal")
    os.chmod("comadd.py", stat.S_IRWXU)
    os.chmod("setting.txt", stat.S_IRWXU)

def exitapp():
    stop()
    exit(0)
    
def blocklist():
    wblocklist = tk.Toplevel(gui)
    wblocklist.title("Edit block list")
    label1 = ttk.Label(wblocklist, text="App list")
    label1.pack()
    global applist
    applist = tk.Listbox(wblocklist)
    for app in apps:
        applist.insert(tk.END, app)
    applist.pack()

    def inserta():
        winput = tk.Toplevel(wblocklist)
        winput.title("Add program")
        entry = ttk.Entry(winput, width=10)
        entry.pack()
        def getinput():
            global applist
            applist.insert(ttk.END, str(entry.get()))
            global apps
            apps.append(str(entry.get()))
            wsetting()
            winput.destroy()
        button = ttk.Button(winput, text="Add", command=getinput)
        button.pack()

    def removea():
        global applist
        removeline = applist.curselection()
        if removeline != ():
            # Not a empty tuple
            for line in removeline:
                applist.delete(line)
                global apps
                apps.pop(line)
        wsetting()

    insertab = ttk.Button(wblocklist, text="Insert", command=inserta)
    removeab = ttk.Button(wblocklist, text="Remove", command=removea)
    insertab.pack()
    removeab.pack()

    label2 = ttk.Label(wblocklist, text="Website list")
    label2.pack()
    global sitelist
    sitelist = tk.Listbox(wblocklist)
    for site in sites:
        sitelist.insert(tk.END, site)
    sitelist.pack()

    def insertb():
        winput = tk.Toplevel(wblocklist)
        winput.title("Add program")
        entry = ttk.Entry(winput, width=10)
        entry.pack()
        def getinput():
            global sitelist
            sitelist.insert(ttk.END, str(entry.get()))
            global sites
            sites.append(str(entry.get()))
            wsetting()
            winput.destroy()
        button = ttk.Button(winput, text="Add", command=getinput)
        button.pack()

    def removeb():
        global sitelist
        removeline = sitelist.curselection()
        if removeline != ():
            # Not a empty tuple
            for line in removeline:
                sitelist.delete(line)
                global sites
                sites.pop(line)
        wsetting()

    insertbb = ttk.Button(wblocklist, text="Insert", command=insertb)
    removebb = ttk.Button(wblocklist, text="Remove", command=removeb)
    insertbb.pack()
    removebb.pack()

class AskButtons():
    def __init__(self, root, question, value):
        global settings
        self.root = root
        try:
            self.lastval = settings[value]
        except IndexError:
            settings.append("0")
            self.lastval = "0"
        self.question = question
        self.value = value
        ttk.Label(self.root, text=self.question).pack()
        self.currentval = ttk.Label(self.root, text=("Currently: " + ("Enabled" if settings[self.value] == "1" else "Disabled")))
        self.currentval.pack()
        self.button = ttk.Button(self.root, text=("Enable" if settings[self.value] == "0" else "Disable"), command=self.change)
        self.button.pack()

    def change(self):
        settings[self.value] = "0" if self.lastval == "1" else "1"
        wsetting()
        advsetexec()
        self.lastval = settings[self.value]
        self.currentval.configure(text=("Currently: " + ("Enabled" if settings[self.value] == "1" else "Disabled")))
        self.button.configure(text=("Enable" if settings[self.value] == "0" else "Disable"))
    
def session():
    wsession = tk.Toplevel(gui)

    ttk.Label(wsession, text="Session time (in sec): ").pack()
    stimeinput = ttk.Entry(wsession, width=10)
    stimeinput.insert(tk.END, str(sessiontime))
    stimeinput.pack()

    ttk.Label(wsession, text="Break time (in sec): ").pack()
    btimeinput = ttk.Entry(wsession, width=10)
    btimeinput.insert(tk.END, str(breaktime))
    btimeinput.pack()

    def done():
        global sessiontime, stime_min, stime_sec, onesec, breaktime, btime_min, btime_sec
        sessiontime = int(stimeinput.get())
        stime_min = sessiontime // 60
        stime_sec = sessiontime % 60
        onesec = 360/sessiontime
    
        breaktime = int(btimeinput.get())
        btime_min = breaktime // 60
        btime_sec = breaktime % 60

        wsetting()

    ttk.Button(wsession, text="Ok!", command=done).pack()
    ttk.Label(wsession, text="_________________________________").pack()

    btn1 = AskButtons(wsession, "Advanced settings?", 0)
    #btn2 = AskButtons(wsession, "Unlimited session time?", 1) # Don't enable this!
    btn3 = AskButtons(wsession, "Disable breaktime?", 2)

def advanced():
    wadvanced = tk.Toplevel(gui)
    btn1 = AskButtons(wadvanced, "Disable CMD?", 3)
    btn2 = AskButtons(wadvanced, "Disable taskmgr?", 4)
    btn3 = AskButtons(wadvanced, "Disable Powershell?", 5)
    btn4 = AskButtons(wadvanced, "Disable stop button if in session time?", 6)
    btn5 = AskButtons(wadvanced, "Disable setting in session time?", 7)
    btn6 = AskButtons(wadvanced, "Disable system setting in session time?\n(Windows Only)", 8)
    btn7 = AskButtons(wadvanced, "Protect program from being edited or \ndeleted?", 9)

def onlinehelp():
    webbrowser.open_new_tab("https://github.com/raspiduino/comadd/wiki/help")
def about():
    messagebox.showinfo("About", "ComAdd v1.0\nCopyright @raspiduino on github.com\nDate created 1/11/2020")

def sapp():
    pass

#def sweb():
#    if os.name == "nt":
#        os.system("python track.py")
#    else:
#        os.system("python3 track.py")

def timespend():
    pass

# Create GUI
gui = tk.Tk()
if os.name == "nt":
    gui.iconbitmap("icons\\icon.ico")
else:
    gui.iconbitmap("icons/icon.ico")
gui.title("ComAdd v1.0")
gui.geometry('720x360')
gui.resizable(width=False, height=False)

# Create main session gui
canvas = tk.Canvas(gui, width=300, height=200)
canvas.pack(fill="both", expand=True)
c0 = canvas.create_oval(260, 30, 460, 230, fill="white")
c1 = canvas.create_arc(260, 30, 460, 230, start=0, extent=0, fill="green")
c2 = canvas.create_oval(280, 50, 440, 210, fill="white")
clock = canvas.create_text(360, 130, font=("SegoeUI", 24), text=str(stime_min) + ":" + (str(stime_sec) if stime_sec > 9 else "0" + str(stime_sec)))

if os.name == "nt":
    mainbuttonimg = tk.PhotoImage(file="icons\\button1.png")
    mainbuttonrun = tk.PhotoImage(file="icons\\button2.png")
else:
    mainbuttonimg = tk.PhotoImage(file="icons/button1.png")
    mainbuttonrun = tk.PhotoImage(file="icons/button2.png")

mainbutton = Button(gui, image=mainbuttonimg, borderwidth=0, command=startsession)
mainbutton.pack(side = tk.TOP)

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
#statistics = Menu(menubar, tearoff=0)
#statistics.add_command(label="Apps usage", command=sapp)
#statistics.add_command(label="Web usage", command=sweb)
#statistics.add_command(label="Time spend", command=timespend)
#menubar.add_cascade(label="Statistics", menu=statistics)

# Setting menu
setting = Menu(menubar, tearoff=0)
setting.add_command(label="Block list", command=blocklist)
setting.add_command(label="Session & break setting", command=session)
setting.add_command(label="Advanced setting", command=advanced)
menubar.add_cascade(label="Setting", menu=setting)

# Help menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Online help", command=onlinehelp)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

gui.configure(menu=menubar)

gui.mainloop()
