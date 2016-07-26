__author__ = 'surya'

from Tkinter import *
from tkFileDialog import askopenfilename

from Gui_support import Gui_looks


#background="snow3"
background = "grey95"

#################################################################################################
#################################### DATABASE WINDOW   ###################################
###################################################################################################

def maspit_dbwindow(databasedo,projname,projReason,expgrpname,baitname,expname,expReason,ScanningDate,mbubaitcode,baitVectorType,stimulusType,
stimulusconc,protocolType,fusioncpd,fusioncpdConc,moleculeExtraInfo,txt,file,BaitTransfectDate):
    ## define the fields with default alues
    def FillAllField():
        from datetime import date
        today_date= date.today()
        projname.set("ProjectTest1")
        projReason.set("To test")
        expgrpname.set("EXPgrp1")
        baitname.set("")
        expname.set("exp1")
        expReason.set("to test the gui functionality")
        ScanningDate.set(today_date)
        BaitTransfectDate.set(today_date)
        mbubaitcode.set("")
        baitVectorType.set("F3bait")
        stimulusType.set("")
        stimulusconc.set(0.001)
        protocolType.set("A")
        mixinfo_update=file.split("/")[:-1]
        mixinfo_update.append("Mixture.txt")
        # mix_info.set('/'.join(mixinfo_update))
        fusioncpd.set("")
        fusioncpdConc.set(0.002)

    if databasedo.get():
        database = Toplevel(bg=background)
        database.geometry("%dx%d+%d+%d" % (1200, 500, 200, 100))
        Gui_looks.Streching([database], 12)
        ## initialize to enter the value by user

        projname_entry = Entry(database, width=5, textvariable=projname)
        projReason_entry = Entry(database, width=5, textvariable=projReason)
        expgrpname_entry = Entry(database, width=5, textvariable=expgrpname)
        baitnmae_entry=Entry(database, width=5, textvariable=baitname)
        expname_entry = Entry(database, width=5, textvariable=expname)
        expReason_entry = Entry(database, textvariable=expReason)
        baitTransfect_entry=Entry(database,textvariable=BaitTransfectDate)
        transfectdate_entry=Entry(database, textvariable=ScanningDate)
        mbubaitcode_entry=Entry(database, textvariable=mbubaitcode)
        baitVectorType_entry= Entry(database,textvariable=baitVectorType)
        stimulusType_entry=Entry(database,textvariable=stimulusType)
        stimulusconc_entry=Entry(database,textvariable=stimulusconc)
        protocolType_entry=Entry(database,textvariable=protocolType)
        # mix_info_entry=Entry(database,textvariable=mix_info)
        fusioncpd_entry=Entry(database,textvariable=fusioncpd)
        fusioncpdConc_entry=Entry(database,textvariable=fusioncpdConc)
        moleculeExtraInfo_entry=Entry(database,textvariable=moleculeExtraInfo)

        ## put the variable on the screen

        projname_entry.grid(column=2, row=2, sticky=(W, E))
        projReason_entry.grid(column=4, row=2, sticky=(W, E),columnspan=3)
        expgrpname_entry.grid(column=2, row=3, sticky=(W, E))
        baitnmae_entry.grid(column=4, row=3, sticky=(W, E))
        expname_entry.grid(column=2, row=4, sticky=(W, E))
        expReason_entry.grid(column=4, row=4, sticky=(W, E))
        baitTransfect_entry.grid(column=6, row=4, sticky=(W, E))
        transfectdate_entry.grid(column=2, row=5, sticky=(W, E))
        mbubaitcode_entry.grid(column=4, row=5, sticky=(W, E))
        baitVectorType_entry.grid(column=6, row=5, sticky=(W, E))
        stimulusType_entry.grid(column=2, row=6, sticky=(W, E))
        stimulusconc_entry.grid(column=4, row=6, sticky=(W, E))
        protocolType_entry.grid(column=6, row=6, sticky=(W, E))
        # mix_info_entry.grid(column=2, columnspan=3, row=7, sticky=(W, E))
        fusioncpd_entry.grid(column=2,row=7, sticky=(W, E))
        fusioncpdConc_entry.grid(column=4,row=7, sticky=(W, E))
        moleculeExtraInfo_entry.grid(column=2,row=8, sticky=(W, E),columnspan=3)



        ### place the name of the entry labels
        Gui_looks.CreateLabels(database, ["DATABASE ENTRY"], b=background, f=("Helvetica", 15, "bold"), g="dark green",
                               col_start=3)
        Gui_looks.CreateLabels(database,
                               ["Project Name*", "Experiment Group Name*", "Experiment Name*","Scanning Date*", "Stimulus Type*","Fusion cpd Type*","molecule extra info"], row_start=2,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Reason*","Bait Name*","Experiment Reason*", "MBU Bait Code*", "Stimulus Concentration*"], row_start=2, col_start=3, b=background,
                               f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Bait Transfect Date*","Bait Vector Type*","Protocol Version*"], row_start=4, col_start=5,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, [ "Fusion cpd Concentration*"], row_start=7,col_start=3,
                                b=background, f=("Helvetica", 9, "bold"), g="dark green")

        # Button(database, image=txt, command=(lambda:mix_info.set(askopenfilename())), bg="dark green").grid(column=5,
        #     row=7,sticky=W)
        Button(database, text="Submit", command=database.destroy, font=("Helvetica", 10, "bold"), fg="red").grid(
            column=5, row=8, sticky=E)
        Button(database, text="FillOut", command=FillAllField, font=("Helvetica", 10), fg="blue").grid(
            column=6, row=8, sticky=E)
