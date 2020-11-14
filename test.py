import tkinter as tk

root = tk.Tk()
session = tk.Toplevel(root)
CheckVar = tk.IntVar()
checkbutton = tk.Checkbutton(session, text='Block Internet',variable=CheckVar, onvalue=1, offvalue=0)
checkbutton.pack()
checkbutton.select()
root.mainloop()
