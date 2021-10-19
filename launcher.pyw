from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
from traceback import format_tb
import sys
import os
from requests import get
import urllib

import winshell


from win32com.client import Dispatch



def log(message,filename="latest.log"):
    f = open(filename,'a+')
    curtim = str(datetime.datetime.now())
    f.write('['+curtim[0:len(curtim)-3]+']')
    f.write(' '+str(message))
    f.write('\n')
    f.close()

def toplevelerror(message,title='Error'):
    title = str(title)
    message = str(message)
    root = Tk()
    root.wm_attributes("-topmost",True)
    root.withdraw()
    messagebox.showerror(title,message)

def handle_exception(type,value,traceback):
    if issubclass(type, KeyboardInterrupt):
        pass
    else:
        try:
            log('!UNCAUGHT EXCPETION!'+'\n'+str(type)+'\n'+str(value)+'\n'+str(format_tb(traceback)[0]))
        except:
            pass
        try:
            global STATE
            STATE = "CRASHED"
        except:
            pass
        toplevelerror('A fatal exception occured. ERROR:\n'+str(type)+'\n'+str(value)+'\n'+str(format_tb(traceback)[0]))

sys.excepthook = handle_exception
#Creating Shortcuts
ICON = "ep.ico"

topl = Tk()
topl.title('Working')
l = Label(topl,text="Downloading Files")
l.grid(column=0,row=0)
topl.update()
log('Scanning for game files')
if not os.path.isfile("planegame.exe"):
    log("couldn't find file planegame.exe! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/releases/download/PR1/planegame.exe", "planegame.exe")

if not os.path.isfile("pg_music.ogg"):
    log("couldn't find file pg_music.ogg! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/raw/main/pg_music.ogg", "pg_music.ogg")

if not os.path.isfile("ep.ico"):
    log("couldn't find file ep.ico! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/raw/main/ep.ico", "ep.ico")

if not os.path.isfile("doc.txt"):
    log("couldn't find file doc.txt! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/raw/main/doc.txt", "doc.txt")

if not os.path.isfile("pg_death.ogg"):
    log("couldn't find file pg_death.ogg! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/raw/main/pg_death.ogg", "pg_death.ogg")

if not os.path.isfile("pg_background_1080.png"):
    log("couldn't find file pg_background_1080.png! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/raw/main/pg_background_1080.png", "pg_background_1080.png")

if not os.path.isfile("plane.png"):
    log("couldn't find file plane.png! Downloading.")
    urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/PlaneGame/raw/main/plane.png", "plane.png")

l.config(text='Scanning for shortcuts')
topl.update()
log('START Scanning for shortcuts')
if not os.path.isfile(os.path.join(winshell.desktop(common=False),"Enderbyte Programs Launcher.lnk")):
    log('Making dsktop shortcut')
    target = os.getcwd()+"\\launcher.exe"
    wDir = os.getcwd()
    path = os.path.join(winshell.desktop(common=False),"Enderbyte Programs Launcher.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation=ICON
    shortcut.save()

if not os.path.isfile(os.path.join(winshell.programs(common=False),"Enderbyte Programs Launcher.lnk")):
    log('making start menu shortcut')
    target = os.getcwd()+"\\launcher.exe"
    wDir = os.getcwd()
    path = os.path.join(winshell.programs(common=False),"Enderbyte Programs Launcher.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation=ICON
    shortcut.save()

def expas():
    pass

def unins():
    Tk().withdraw()
    e = messagebox.askyesno("Q","Are you sure you want to uninstall?")
    if e:
        try:
            os.remove(os.path.join(winshell.desktop(common=False),"Enderbyte Programs Launcher.lnk"))
        except:
            donothing = 0
        try:
            os.remove(os.path.join(winshell.programs(common=False),"Enderbyte Programs Launcher.lnk"))
        except:
            donothing = 0

        try:
            os.remove("latest.log")
        except:
            donothing = 0

        try:
            os.remove("game.lvl")
        except:
            donothing = 0

        sys.exit()

def delog():
    try:
        os.remove('latest.log')
    except:
        pass
    Tk().withdraw()
    messagebox.showinfo('Info',"Deleted log.")

def delsv():
    Tk().withdraw()
    x = messagebox.askyesno("Q","Are you sure you want to delete the save?")
    if x == True:
        try:
            os.remove('game.lvl')
        except:
            pass
l.config(text="All finished!")
l.update()
topl.destroy()
log('start finished.')
root = Tk()
root.title('Enderbyte Programs Launcher')
root.geometry('600x300')
root.iconbitmap('ep.ico')
style = ttk.Style(root)
style.theme_use('vista')
lbl0 = ttk.Label(root,text='Welcome to the Enderbyte Programs Launcher. \nPlease select your option for PLANE GAME',font=('Arial',18,"bold"))
lbl0.pack()
lbl = ttk.Label(root,text='Creates new game (may overwrite game.lvl savefile)')
lbl.pack()
btn0 = ttk.Button(root,text='New Game',command=lambda: os.startfile('planegame.exe'))
btn0.pack()
lbl1 = ttk.Label(root,text='Continues game with data found in game.lvl')
lbl1.pack()
btn3 = ttk.Button(root,text='Continue Game',command=lambda: os.system(".\\planegame.exe game.lvl"))
btn3.pack()
btn1 = ttk.Button(root,text='Exit',command=sys.exit)
btn1.pack()
btn4 = ttk.Button(root,text='Uninstall',command=unins)
btn4.pack()

btn5 = ttk.Button(root,text="Delete log",command=delog)
btn5.pack()

btn6 = ttk.Button(root,text="Wipe save",command=delsv)
btn6.pack()
btn7 = ttk.Button(root,text="Documentation",command=lambda: os.startfile('doc.txt'))
btn7.pack()
try:
    lbl3 = Label(root,text="TODAY'S MESSAGE- "+str(get("https://pastebin.com/raw/WgFCuPqM").text))
    lbl3.pack(side=BOTTOM)
except:
    pass
root.protocol("WM_DELETE_WINDOW",expas)
root.mainloop()