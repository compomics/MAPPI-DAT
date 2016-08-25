

__author__ = 'surya'


from Tkinter import *
from Gui_support import Gui_looks, GuiCommands
from DatabaseWindows import maspit_window,mappit_window,kiss_window
background="grey95"


def opendb_window(maspit,mappit,treatment,kiss,databasedo,projname,projReason,expgrpname,baitname,expname,expReason,ScanningDate,mbubaitcode,baitVectorType,stimulusType,
stimulusconc,protocolType,treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,fusioncpd,fusioncpdConc,moleculeExtraInfo,txt,file,root,BaitTransfectDate):

    if maspit:
        maspit_window.maspit_dbwindow(databasedo,projname,projReason,expgrpname,baitname,expname,expReason,ScanningDate,mbubaitcode,baitVectorType,stimulusType,
stimulusconc,protocolType,fusioncpd,fusioncpdConc,moleculeExtraInfo,txt,file,BaitTransfectDate)
    elif mappit:
        mappit_window.mappit_dbwindow(databasedo,projname,projReason,expgrpname,baitname,expname,expReason,ScanningDate,mbubaitcode,baitVectorType,stimulusType,
stimulusconc,protocolType,treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,txt,file,treatment,BaitTransfectDate)
    elif kiss:
        kiss_window.kiss_dbwindow()

    root.destroy()







################################################################################################################################
################################# selection for the database window #############################################################
################################################################################################################################


def createPre_databaseWindow(mappit,maspit,kiss,treatment,databasedo,projname,projReason,expgrpname,baitname,expname,expReason,ScanningDate,mbubaitcode,baitVectorType,stimulusType,
stimulusconc,protocolType,treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,fusioncpd,fusioncpdConc,moleculeExtraInfo,txt,file,BaitTransfectDate):
    if databasedo.get():
        root=Toplevel()
        root.geometry("%dx%d+%d+%d" % (500, 300, 500, 300))
        Label(root,text="      Select Options for Database       ",font=("Helvetica", 10, "bold")).grid(column=1,row=0,sticky=(W,E),columnspan=3) ## headline
        Label(root,text="                                                                          ").grid(column=1,row=1,sticky=(W,E),columnspan=3) ## space to differentiate between the button and checkbox
        Label(root,text="                                                                          ").grid(column=1,row=6,sticky=(W,E),columnspan=3) ## space to differentiate between the button and checkbox


        Gui_looks.Streching([root],20)
        maspit.set(False)
        mappit.set(False)
        kiss.set(False)
        treatment.set(False)

        mappit_entry = Checkbutton(root, text="MAPPIT", variable=mappit, onvalue=True,bg=background ,font = "Helvetica 10",
                                   command=lambda:GuiCommands.disable_checkbox(maspit_entry,kiss_entry,treatment_entry,host_box=mappit.get()))
        maspit_entry = Checkbutton(root, text="MASPIT", variable=maspit, onvalue=True,bg=background ,font = "Helvetica 10",
                                   command=lambda:GuiCommands.disable_checkbox(mappit_entry,kiss_entry,host_box=maspit.get()))#,treatment_opp=treatment_entry))
        kiss_entry = Checkbutton(root, text="KISS    ", variable=kiss, onvalue=True,bg=background ,font = "Helvetica 10",
                                 command=lambda:GuiCommands.disable_checkbox(maspit_entry,mappit_entry,treatment_entry,host_box=kiss.get()))
        treatment_entry = Checkbutton(root, text="Treatment", variable=treatment, onvalue=True,bg=background ,font = "Helvetica 10")
        treatment_entry.configure(state='disable')


        maspit_entry.grid(column=1, row=2, sticky=(W, E))
        mappit_entry.grid(column=1, row=3, sticky=(W, E))
        kiss_entry.grid(column=1, row=4, sticky=(W, E))

        treatment_entry.grid(column=2, row=5, sticky=(W, E))

        Button(root, text="Start Database window", command=lambda:(opendb_window(maspit.get(),mappit.get(),treatment.get(),kiss.get(),databasedo,projname,projReason,expgrpname,baitname,expname,expReason,
                                                                                 ScanningDate,mbubaitcode,baitVectorType,stimulusType,stimulusconc,protocolType,treatmentType,treatementConc,
                                                                             Treatementdate,treatment_starttime,treatment_endtime,fusioncpd,fusioncpdConc,moleculeExtraInfo,txt,file,root,BaitTransfectDate)),fg="dark green",relief=RAISED,font = "Helvetica 10").grid(column=2, row=8, sticky=(W,E))