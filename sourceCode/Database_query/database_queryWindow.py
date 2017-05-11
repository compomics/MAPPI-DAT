

__author__ = 'surya'


## importing
from Tkinter import *
import os
from Database_query import DatabaseSearch
from Mysql_queries import Project_Query
from Gui_support import Gui_looks

background="grey95"
## to get the path of the current dir
path=os.getcwd()







#################################################################################################
#################################### Query Window   ###################################
###################################################################################################

## create first frame....

def query_window(Overview,cnx,callback, information_logo):
    bg_toshow="grey90"

    frame1 = Frame(Overview, borderwidth=5,relief=GROOVE,bg=bg_toshow)
    frame1.grid(column=1, row=1,columnspan=6,sticky=(N,S,W,E))
    Gui_looks.Streching([frame1],8)


    # ### method to get the experiment group entry
    def chooseproject(p_value,All_expgrp):
        expgrp_List.delete(0, END)
        del (All_expgrp[:])
        del(p_value[:])
        try:
            firstIndex = project_List.curselection()[0]
            value = All_projects[int(firstIndex)]
            All_expGroups=Project_Query.Select_all(Project_Query.Exp_gropAll,cnx,arg=True,argument=(value,))
            for x_entry in All_expGroups:
                All_expgrp.append(x_entry)
                expgrp_List.insert(END,x_entry)
        except IndexError:
            value=None
            expgrp_List.delete(0, END)
        p_value.append(value)
    #    print p_value
    ## method to get experiments

    def chooseexpgrp(p_value,All_expgrp,All_experiments,e_value,cnx):
        del(e_value[:])
        expgrp=All_expgrp
        exp_List.delete(0, END)
        del (All_experiments[:])
        try:
            secondIndex=expgrp_List.curselection()[0]
            expgrpvalue=expgrp[int(secondIndex)]
            All_exp=Project_Query.Select_all(Project_Query.ExpAll,cnx,arg=True,argument=(p_value[-1],expgrpvalue))
            for x_entry in All_exp:
                All_experiments.append(x_entry)
                exp_List.insert(END,x_entry)
        except IndexError:
            value=None
            exp_List.delete(0, END)
        e_value.append(expgrpvalue)


    ## for QUERY...... searching database.....

    ## PROJECT WINDOW............................................................
    global All_projects
    if cnx=="":
        All_projects=[]
    else:
        All_projects=Project_Query.Select_all(Project_Query.projectAll,cnx)

    ## create button on the top for quit
    Button(Overview, text="Quit", command=callback,fg="red",font = "Helvetica 10",relief=RAISED).grid(column=6, row=10, sticky=W)

    ## 3 frames in the window
    Gui_looks.CreateLabels(frame1,["Projects"],f="Helvetica 10 bold",row_start=1,b=bg_toshow)
    Gui_looks.CreateLabels(frame1,["**Select any one Project by double click"],g="red",row_start=3,b=bg_toshow)


    project_List  = Listbox(frame1, height=3,fg="blue")
    project_List.grid(column=1, row=2, sticky=(W,E))
    if All_projects!=None:
        for entry in All_projects:
            project_List.insert(END,entry)
    sbp = Scrollbar(frame1,orient=VERTICAL)
    sbp.grid(column=1, row=2, sticky=(E))
    sbp.configure(command=project_List.yview)
    project_List.configure(yscrollcommand=sbp.set)
    # onDoubeClick: get messages selected in listbox

    p_value=[]
    All_expgrp=[]
    project_List.bind('<Double-1>', (lambda event: chooseproject(p_value,All_expgrp)))


    ## ## Experiment Group WINDOW............................................................

    Gui_looks.CreateLabels(frame1,["Experiment Groups"],col_start=3,f="Helvetica 10 bold",b=bg_toshow)
    Gui_looks.CreateLabels(frame1,["**Select one Exp-group by double click"],g="red",row_start=3,col_start=3,b=bg_toshow)


    expgrp_List  = Listbox(frame1, height=3,fg="blue")
    expgrp_List.grid(column=3, row=2, sticky=(W,E))
    sbx = Scrollbar(frame1,orient=VERTICAL)
    sbx.grid(column=3, row=2, sticky=(E))
    sbx.configure(command=expgrp_List.yview)
    expgrp_List.configure(yscrollcommand=sbx.set)


    # onDoubeClick: get messages selected in listbox
    All_experiments=[]
    e_value=[]
    expgrp_List.bind('<Double-1>', (lambda event: chooseexpgrp(p_value,All_expgrp,All_experiments,e_value,cnx)))



    ####### Experiment Window
    Gui_looks.CreateLabels(frame1,["Experiments"],col_start=5,f="Helvetica 10 bold",b=bg_toshow)
    Gui_looks.CreateLabels(frame1,["**Select one experiment by double click"],g="red",row_start=3,col_start=5,b=bg_toshow)

    exp_List  = Listbox(frame1, height=3,fg="blue")
    exp_List.grid(column=5, row=2, sticky=(W,E))
    sbe = Scrollbar(frame1,orient=VERTICAL)
    sbe.grid(column=5, row=2, sticky=(E))
    sbe.configure(command=exp_List.yview)
    exp_List.configure(yscrollcommand=sbe.set)
    exp_List.bind('<Double-1>', (lambda event: DatabaseSearch.chooseexp(cnx,p_value,e_value,All_experiments,
                                        exp_List,Overview,bg_toshow,RetestExportPath,
            checkVar=elist,checkNames=EcheckNames,checkVarPath=Epath,info_logo=information_logo)))

    ######## Export Window
    Eprey,Ebait,Emolecule,Esdfound,Esdnotfound,Ecfound,Ecnotfound,Enafound,Enanotfound,Easpecfound,Easpecnotfound,ErawData,\
    EcytoscapeFile,EXMLFile=BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),\
                   BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar()

    elist=[Eprey,Ebait,Emolecule,Esdfound,Esdnotfound,Ecfound,Ecnotfound,Enafound,Enanotfound,
           Easpecfound,Easpecnotfound,ErawData,EcytoscapeFile,EXMLFile]

    Folderpath=StringVar()
    Epath=[Folderpath]
    EcheckNames="Prey,Bait,Molecule,NewHits Found,NewHits NotFound,A-specifics Found,A-specifics NotFound," \
                "RawDataFiles,cytoscape compatible File,PSI_MI XML File".split(",")

################ retest window
    RetestExportPath=StringVar()

    for i in elist:
        i.set(False)
    cnx.close()
    # if cnx.is_connected():
    #     cnx.cmd_quit()



