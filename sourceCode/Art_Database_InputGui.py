__author__ = 'surya'

from Tkinter import *
import ttk
from tkFileDialog import askopenfilename
from Gui_support.Gui_looks import *
from Mysql_queries import MySqlConnection
########################################################################


def changefile():
    print "under construction"


root = Tk()
root.title("Experiment information")
root.geometry("%dx%d+%d+%d" % (700, 200, 200, 200))

mainframe = ttk.Frame(root, borderwidth=50,relief="sunken", width=2000, height=1000)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=3)
mainframe.columnconfigure(1, weight=3)
mainframe.columnconfigure(2, weight=3)
mainframe.columnconfigure(3, weight=3)
mainframe.columnconfigure(4, weight=3)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(1, weight=3)
mainframe.rowconfigure(2, weight=3)
mainframe.rowconfigure(3, weight=3)
mainframe.rowconfigure(4, weight=3)

# art_aliqot,mixture = StringVar(),StringVar()
# done=StringVar()
####################################################################
## check for mysql
cnx=""
try:
    cnx= MySqlConnection.connectSql()
except Exception:
    print("Database is not connected")
    pass

## first ask user what type of information wants to add
if cnx!="":
    from Art_Window_Method import small_windows
    # import small_windows
    ttk.Label(mainframe, text=" what type of information do you want to add in the database? ").grid(column=1, row=1, sticky=W, columnspan=3)
    ttk.Button(mainframe, text="Add ART main", command=small_windows.artWindow).grid(column=1, row=2, sticky=W)
    ttk.Button(mainframe, text="Add ART aliqot", command=small_windows.artAliqotWindow).grid(column=2, row=2, sticky=W)
    ttk.Button(mainframe, text="Add mixture inforamtion", command=small_windows.mixtureWindow).grid(column=3, row=2, sticky=W)
    ttk.Button(mainframe, text="Add Printing Info", command=small_windows.ScreeningWindow).grid(column=4, row=2, sticky=W)


cnx.close()
root.mainloop()