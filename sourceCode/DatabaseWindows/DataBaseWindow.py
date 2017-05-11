

__author__ = 'surya'

from Tkinter import *
from tkFileDialog import askopenfilename
from Gui_support import Gui_looks
from Database_input import mysql_mappit
from Mysql_queries import MySqlConnection
from datetime import datetime
background = "grey95"

#################################################################################################
#################################### DATABASE WINDOW   ###################################
###################################################################################################

def databasewindow(databasedo,projname,projReason,expgrpname,expname,expdate,expReason,scanningdate,
                   baitfile,baitconc,brandEPO,stimulusepo,stimulusleptin,molecule,moleculefile,txt,mainFile,VectorType,mix_info):
    def FillAllField():
        from datetime import date
        today_date= date.today()
        projname.set("ProjectTest1")
        projReason.set("To test")
        expgrpname.set("EXPgrp1")
        expname.set("exp1")
        expdate.set(today_date)
        expReason.set("to test the gui functionality")
        VectorType.set("F3bait")
        # baittranfdate.set(today_date)
        # arraymatedate.set(today_date)
        scanningdate.set(today_date)
        bfile_update=mainFile.split("/")[:-1]
        bfile_update.append("bait.txt")
        baitfile.set('/'.join(bfile_update))

        mfile_update=mainFile.split("/")[:-1]
        mfile_update.append("molecule.txt")
        moleculefile.set('/'.join(mfile_update))

        # mixinfo_update=mainFile.split("/")[:-1]
        # mixinfo_update.append("Mixture.txt")
        # mix_info.set('/'.join(mixinfo_update))

        baitconc.set(0.05)
        brandEPO.set("ABC")
        stimulusepo.set(0.002)
        stimulusleptin.set(0.01)

    if databasedo.get():
        database = Toplevel(bg=background)
        database.geometry("%dx%d+%d+%d" % (1200, 500, 200, 100))
        Gui_looks.Streching([database], 12)
        ## initialize to enter the value by user

        projname_entry = Entry(database, width=5, textvariable=projname)
        projReason_entry = Entry(database, width=5, textvariable=projReason)
        expgrpname_entry = Entry(database, width=5, textvariable=expgrpname)
        expname_entry = Entry(database, width=5, textvariable=expname)
        expdate_entry = Entry(database, textvariable=expdate)
        expReason_entry = Entry(database, textvariable=expReason)
        # baittranfdate_entry = Entry(database, textvariable=baittranfdate)
        # arraymatedate_entry = Entry(database, textvariable=arraymatedate)
        scanningdate_entry = Entry(database, textvariable=scanningdate)
        baitfile_entry = Entry(database,textvariable=baitfile)
        baitconc_entry = Entry(database, textvariable=baitconc)
        brandEPO_entry = Entry(database, textvariable=brandEPO)
        VectorType_entry= Entry(database,textvariable=VectorType)
        stimulusepo_entry = Entry(database, textvariable=stimulusepo)
        stimulusleptin_entry = Entry(database, textvariable=stimulusleptin)
        molecule_entry = Checkbutton(database, text="Molecule also present", variable=molecule, onvalue=True,
                                     bg=background, fg="dark green", font=("Helvetica", 9, "bold"))
        moleculefile_entry = Entry(database,textvariable=moleculefile)
        mix_info_entry=Entry(database,textvariable=mix_info)
        ## put the variable on the screen

        projname_entry.grid(column=2, row=2, sticky=(W, E))
        projReason_entry.grid(column=4, row=2, sticky=(W, E))
        expgrpname_entry.grid(column=2, row=3, sticky=(W, E))
        expname_entry.grid(column=2, row=4, sticky=(W, E))
        expdate_entry.grid(column=4, row=4, sticky=(W, E))
        expReason_entry.grid(column=6, row=4, sticky=(W, E))
        # baittranfdate_entry.grid(column=2, row=5, sticky=(W, E))
        # arraymatedate_entry.grid(column=4, row=5, sticky=(W, E))
        scanningdate_entry.grid(column=6, row=5, sticky=(W, E))
        baitfile_entry.grid(column=2, columnspan=3, row=7, sticky=(W, E))
        moleculefile_entry.grid(column=2, columnspan=3, row=8, sticky=(W, E))
        mix_info_entry.grid(column=2, columnspan=3, row=9, sticky=(W, E))
        molecule_entry.grid(column=6, row=8, sticky=(W))
        baitconc_entry.grid(column=2, row=5, sticky=(W, E))
        brandEPO_entry.grid(column=4, row=5, sticky=(W, E))
        VectorType_entry.grid(column=6,row=6,sticky=(W,E))
        stimulusepo_entry.grid(column=2, row=6, sticky=(W, E))
        stimulusleptin_entry.grid(column=4, row=6, sticky=(W, E))



        ### place the name of the entry labels
        Gui_looks.CreateLabels(database, ["DATABASE ENTRY"], b=background, f=("Helvetica", 15, "bold"), g="dark green",
                               col_start=3)
        Gui_looks.CreateLabels(database,
                               ["Project Name*", "Experiment Group Name*", "Experiment Name*","Bait Concentration*", "Stimulus EPO*","Bait File*", "Molecule File","Mixture Info List"], row_start=2,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Reason*"], row_start=2, col_start=3, b=background,
                               f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Experiment Date*","Brand EPO*", "Stimulus Leptin*"], row_start=4, col_start=3,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        Gui_looks.CreateLabels(database, ["Experiment Reason*", "Scanning Date*","Vector type*"], row_start=4, col_start=5,
                               b=background, f=("Helvetica", 9, "bold"), g="dark green")
        # Gui_looks.CreateLabels(database, [], row_start=8, col_start=3, b=background,
        #                        f=("Helvetica", 9, "bold"), g="dark green")

        Button(database, image=txt, command=(lambda: moleculefile.set(askopenfilename())), bg="dark green").grid(
            column=5, row=8, sticky=W)
        Button(database, image=txt, command=(lambda: baitfile.set(askopenfilename())), bg="dark green").grid(column=5,
            row=7,sticky=W)
        Button(database, image=txt, command=(lambda:mix_info.set(askopenfilename())), bg="dark green").grid(column=5,
            row=9,sticky=W)
        Button(database, text="Submit", command=database.destroy, font=("Helvetica", 10, "bold"), fg="red").grid(
            column=5, row=9, sticky=E)
        Button(database, text="FillOut", command=FillAllField, font=("Helvetica", 10), fg="blue").grid(
            column=6, row=9, sticky=E)


## to get the database window to add the entry
def DatabaseEntry(Tplate2Path,bait2plate,plate2subfolder,nslist,slist,projname,projReason,expgrpname,baitname,expname,expdate,
                   expReason,Scanningdate,mbubaitcode,baitVectorType,stimulusType,stimulusconc,protocolType,
                  treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,AspecificDic,cnx,
                   mappit,maspit,kiss,treatment,fusioncpd,fusioncpdConc,moleculeExtraInfo,
                  linkageDic,pfp,pcfil,quartfil,plate_tfileDic,PCpresent,BaitTransfectDate,path):

    exp, expgrp,project,platDic = mysql_mappit.input_mysql(Tplate2Path,plate2subfolder,nslist.get(),slist.get(),projname.get(),projReason.get(),
                                           expgrpname.get(),baitname.get(),expname.get(),expdate,expReason.get(),Scanningdate.get(),mbubaitcode.get(),
                                           baitVectorType.get(),stimulusType.get(),stimulusconc.get(),protocolType.get(),treatmentType.get(),
                                           treatementConc.get(),Treatementdate.get(),treatment_starttime.get(),treatment_endtime.get(),AspecificDic,cnx,#plateinfodic,
                                           mappit.get(),maspit.get(),kiss.get(),treatment.get(),fusioncpd.get(),fusioncpdConc.get(),moleculeExtraInfo.get(),
                                           linkageDic,plate_tfileDic,BaitTransfectDate.get(),path)

    ########### first get all the interactors and add analysis parameters
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()

    prey_interactors={}
    cursor1 = cnx.cursor()
    ## get all the interactor ids for the exp group and exp and project
    cursor1.execute("""select i.idinteractors,pr.p_name from interactors i
        inner join experiment_group g on i.ref_expgrpid=g.expgrp_id
        inner join project j on j.project_id=g.ref_projid
        inner join experiments e on g.expgrp_id=e.ref_expgrpid
        inner join prey pr on pr.prey_id=i.ref_preyid
        where g.expgrp_id=%s and e.experiment_id=%s and j.project_id=%s""",
                    (expgrp, exp,project))
    for (inte,preyname) in cursor1:
        prey_interactors[preyname]=inte

    analysis_parameter_input=(""" insert into analysis_parameters (q_val_threshold,particle_count_filtration,quartile_filtration,ref_expid)
                            values (%s,%s,%s,%s) """)

    if PCpresent.get():
        pcfiltration=pcfil.get()
    else:
        pcfiltration=0
    ## first add the parameters in the table analysis_paramater
    cursor1.execute(analysis_parameter_input,(pfp.get(),pcfiltration,quartfil.get(),exp))
    analysisid=cursor1.lastrowid
    cnx.commit()
    cursor1.close()

########################### add the data in the database
    print "stated with adding analysis results...."
    for bait in bait2plate:
        mysql_mappit.analysis_mysql(exp, expgrp,project, path+"/"+bait + "/Analysis/AllPlatesWithoutControlNormalized_SelectedAnalyzed.txt",
                                    cnx,pfp.get(),pcfiltration,quartfil.get(),platDic,prey_interactors,analysisid)

    print "closing now...."
    print(datetime.now())
    if cnx.is_connected:
        cnx.close()
