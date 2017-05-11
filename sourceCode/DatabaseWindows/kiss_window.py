__author__ = 'surya'

from Tkinter import *
from tkFileDialog import askopenfilename

from Gui_support import Gui_looks


#background="snow3"
background = "grey95"

#################################################################################################
#################################### DATABASE WINDOW   ###################################
###################################################################################################

def kiss_dbwindow(databasedo, projname, projReason, expgrpname, baitname, expname, expReason, Scanningdate,
                        mbubaitcode, baitVectorType, stimulusType,
                        stimulusconc, protocolType, treatmentType, treatementConc, Treatementdate, treatment_starttime,
                        treatment_endtime, txt, file, treatment, BaitTransfectDate):


    ## define the fields with default alues
    def FillAllField():
        from datetime import date, time, datetime
        today_date = date.today()
        start_time = datetime.now().time()
        end_time = datetime.now().time()
        projname.set("ProjectTest1")
        projReason.set("To test")
        expgrpname.set("EXPgrp1")
        baitname.set("mbu")
        expname.set("exp1")
        expReason.set("to test the gui functionality")
        Scanningdate.set(today_date)
        BaitTransfectDate.set(today_date)
        mbubaitcode.set("abc")
        baitVectorType.set("F3bait")
        stimulusType.set("leptin")
        stimulusconc.set(0.001)
        protocolType.set("A")
        mixinfo_update = file.split("/")[:-1]
        mixinfo_update.append("Mixture.txt")
        # mix_info.set('/'.join(mixinfo_update))
        if treatment:
            treatmentType.set("")
            treatementConc.set(0.002)
            Treatementdate.set(today_date)
            treatment_starttime.set(start_time)
            treatment_endtime.set(end_time)
    ###############################################################

    if databasedo.get():
        database = Toplevel(bg=background)
        database.geometry("%dx%d+%d+%d" % (1200, 500, 200, 100))
        Gui_looks.Streching([database], 12)
        ## initialize to enter the value by user

        projname_entry = Entry(database, width=5, textvariable=projname)
        projReason_entry = Entry(database, width=5, textvariable=projReason)
        expgrpname_entry = Entry(database, width=5, textvariable=expgrpname)
        baitnmae_entry = Entry(database, width=5, textvariable=baitname)
        expname_entry = Entry(database, width=5, textvariable=expname)
        expReason_entry = Entry(database, textvariable=expReason)
        baitTransfect_entry = Entry(database, textvariable=BaitTransfectDate)
        transfectdate_entry = Entry(database, textvariable=Scanningdate)
        mbubaitcode_entry = Entry(database, textvariable=mbubaitcode)
        baitVectorType_entry = Entry(database, textvariable=baitVectorType)
        stimulusType_entry = Entry(database, textvariable=stimulusType)
        stimulusconc_entry = Entry(database, textvariable=stimulusconc)
        protocolType_entry = Entry(database, textvariable=protocolType)
        # mix_info_entry=Entry(database,textvariable=mix_info)
        if treatment:
            treatmentType_entry = Entry(database, textvariable=treatmentType)
            treatementConc_entry = Entry(database, textvariable=treatementConc)
            treatmentdate_entry = Entry(database, textvariable=Treatementdate)
            treatment_starttime_entry = Entry(database, textvariable=treatment_starttime)
            treatment_endtime_entry = Entry(database, textvariable=treatment_endtime)

        ## put the variable on the screen

        projname_entry.grid(column=2, row=2, sticky=(W, E))
        projReason_entry.grid(column=4, row=2, sticky=(W, E), columnspan=3)
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

        if treatment:
            treatmentType_entry.grid(column=2, row=8, sticky=(W, E))
            treatementConc_entry.grid(column=4, row=8, sticky=(W, E))
            treatmentdate_entry.grid(column=6, row=8, sticky=(W, E))
            treatment_starttime_entry.grid(column=2, row=9, sticky=(W, E))
            treatment_endtime_entry.grid(column=4, row=9, sticky=(W, E))

        ### place the name of the entry labels
        Gui_looks.CreateLabels(database, ["DATABASE ENTRY"], b=background, f=("Helvetica", 15, "bold"), g="dark green",
                               col_start=3)
        Gui_looks.CreateLabels(database,
                               ["Project Name*", "Experiment Group Name*", "Experiment Name*", "Scanning Date*",
                                "Stimulus Type*"], row_start=2,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database,
                               ["Reason*", "Bait Name*", "Experiment Reason*", "MBU Bait Code*", "Stimulus Concentration*"],
                               row_start=2, col_start=3, b=background,
                               f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Bait Transfect Date*", "Bait Vector Type*", "Protocol Version*"], row_start=4,
                               col_start=5,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        if treatment:
            Gui_looks.CreateLabels(database, ["Treatment Type*", "Treatment StartTime*"], row_start=8,
                                   b=background, f=("Helvetica", 9, "bold"), g="dark green")
            Gui_looks.CreateLabels(database, ["Treatment concentration*", "Treatment EndTime*"], row_start=8, col_start=3,
                                   b=background, f=("Helvetica", 9, "bold"), g="dark green")
            Gui_looks.CreateLabels(database, ["Treatement Date*"], row_start=8, col_start=5,
                                   b=background, f=("Helvetica", 9, "bold"), g="dark green")

        # Button(database, image=txt, command=(lambda:mix_info.set(askopenfilename())), bg="dark green").grid(column=5,
        #     row=7,sticky=W)
        Button(database, text="Submit", command=database.destroy, font=("Helvetica", 10, "bold"), fg="red").grid(
            column=5, row=10, sticky=E)
        Button(database, text="FillOut", command=FillAllField, font=("Helvetica", 10), fg="blue").grid(
            column=6, row=10, sticky=E)

