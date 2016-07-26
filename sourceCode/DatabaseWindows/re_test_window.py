__author__ = 'surya'

from Tkinter import *
from tkFileDialog import askopenfilename
from Gui_support import Gui_looks

background = "grey95"

def retest_dbWindow(databasedo,projname,expgroup,experiment,dnaFile,dnaControlFile,reason,txt,folder,retestName,retest_date,doneby):
    ## define the fields with default alues
    def FillAllField():
        from datetime import date

        today_date= date.today()
        projname.set("ProjectTest1")
        expgroup.set("EXPgrp1")
        experiment.set("exp1")
        retestName.set("ReTest1")
        reason.set("to test the gui functionality")
        dnaControlFile.set(folder+"/control_dnaConc.txt")
        dnaFile.set(folder+"/DnaConcentrationFile.txt")
        retest_date.set(today_date)
        doneby.set("Name")




    if databasedo.get():
        database = Toplevel(bg=background)
        database.geometry("%dx%d+%d+%d" % (1000, 500, 200, 100))
        Gui_looks.Streching([database], 12)
        ## initialize to enter the value by user

        RetestName_entry = Entry(database, width=5, textvariable=retestName)
        projname_entry = Entry(database, width=5, textvariable=projname)
        expgroup_entry = Entry(database, width=5, textvariable=expgroup)
        experiment_entry = Entry(database, width=5, textvariable=experiment)
        dnaFile_entry = Entry(database, width=5, textvariable=dnaFile)
        dnaControlFile_entry = Entry(database, width=5, textvariable=dnaControlFile)
        reason_entry = Entry(database, width=5, textvariable=reason)
        retest_date_entry = Entry(database, width=5, textvariable=retest_date)
        doneby_entry = Entry(database, width=5, textvariable=doneby)



        ## put the variable on the screen


        projname_entry.grid(column=2, row=3, sticky=(W, E))
        expgroup_entry.grid(column=4, row=3, sticky=(W, E),columnspan=4)
        RetestName_entry.grid(column=2, row=4, sticky=(W, E))
        experiment_entry.grid(column=4, row=4, sticky=(W, E),columnspan=4)
        retest_date_entry.grid(column=2, row=5, sticky=(W, E))
        doneby_entry.grid(column=4, row=5, sticky=(W, E),columnspan=4)
        reason_entry.grid(column=2, row=6, sticky=(W, E),columnspan=6)
        dnaFile_entry.grid(column=2, row=7, sticky=(W, E),columnspan=6)
        dnaControlFile_entry.grid(column=2, row=8, sticky=(W, E),columnspan=6)

        ### place the name of the entry labels
        Gui_looks.CreateLabels(database, ["Retest Database Entry"], b=background, f=("Helvetica", 15, "bold"), g="dark green",
                               col_start=3)
        Gui_looks.CreateLabels(database,
                               ["Project Name*", "ReTest Name*", "ReTest Date*","Reason*","Normal DNAconc*","Control DNAConc*"], row_start=3,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Experiment Group*"], row_start=3, col_start=3, b=background,f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Experiments*(comma separated)","Done by"], row_start=4, col_start=3,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")

        Button(database, text="Submit", command=database.destroy, font=("Helvetica", 10, "bold"), fg="red").grid(
            column=2, row=9, sticky=E)
        Button(database, text="FillOut", command=FillAllField, font=("Helvetica", 10), fg="blue").grid(
            column=3, row=9, sticky=E)
        Button(database, image=txt, command=(lambda:dnaFile.set(askopenfilename())), bg=background).grid(column=7,
            row=7,sticky=(E))
        Button(database, image=txt, command=(lambda:dnaControlFile.set(askopenfilename())), bg=background).grid(column=7,
            row=8,sticky=(E))

