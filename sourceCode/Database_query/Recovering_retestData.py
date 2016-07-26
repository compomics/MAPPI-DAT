__author__ = 'surya'


from Tkinter import *
from tkFileDialog import askdirectory
from Mysql_queries import questions_query, Project_Query
from Gui_support import Gui_looks
from Plotting_graph import PlottingDist
from Mysql_queries import MySqlConnection

def MergeRowsTogether(retest_data_list):

    file_row_intensity={}
    file_row_other={}
    count=0
    for splits in retest_data_list:
        filename=splits[0].strip()
        row=splits[1].strip()
        col=splits[2].strip()
        intensity=splits[4].strip()
        protein_name=splits[5].strip()
        fibait=splits[7].strip()
        fiprey=splits[8].strip()
        tag=splits[9].strip()
        type=splits[10].strip()
        entrenz=splits[6].strip()
        # print(filename,row,col)
        if filename not in file_row_intensity:
            file_row_intensity[filename]={row:[[protein_name,entrenz,fibait,fiprey,tag,type],[intensity]]}
        elif filename in file_row_intensity:
            if row not in file_row_intensity[filename]:
                file_row_intensity[filename][row]=[[protein_name,entrenz,fibait,fiprey,tag,type],[intensity]]
            elif row in file_row_intensity[filename]:
                file_row_intensity[filename][row][1].append(intensity)
    return  file_row_intensity




def ExportSelectList(cnx,project,expgrp,exp,path):
    header="filename\tNS\tNS\tNS\tS\tS\tS\tNSB+\tNSB+\tNSB+\tSB+\tSB+\tSB+\tuniquename\tentrenzName\tFIwrtBait\tFIwrtPrey\ttag\ttype\n"
    Retest_AllValue={}
    def export():
        for varindex in range(len(retestVariableList)):
            if retestVariableList[AllRetest[varindex][0]].get():
                exportfile=open(path.get()+"/"+AllRetest[varindex][0]+".txt","w")
                exportfile.write(header)

                for files in Retest_AllValue[AllRetest[varindex][0]]:
                    exporline=[]
                    for eachrow in Retest_AllValue[AllRetest[varindex][0]][files]:
                        ln=[files]
                        ln+=Retest_AllValue[AllRetest[varindex][0]][files][eachrow][1]
                        ln+=Retest_AllValue[AllRetest[varindex][0]][files][eachrow][0]
                        ln="\t".join(ln)
                        ln+="\n"
                        exportfile.write(ln)
                exportfile.close()
                print "finised writing ",AllRetest[varindex][0],"in the file ",path.get()+"/"+AllRetest[varindex][0]+".txt"

    retestVariableList={}
    root=Toplevel()
    Gui_looks.Streching([root],20)
    root.geometry("%dx%d+%d+%d" % (1000, 500, 200, 100))

    Gui_looks.CreateLabels(root,["RetestName"],row_start=0,col_start=1,row=False,g="red")
    Gui_looks.CreateLabels(root,"Reason,SubmissionDate,ReTestDate,DoneBy".split(","),row_start=0,col_start=3,row=False,g="red")
    ## get all the re_test for project,experimentgrp and experiments
    AllRetest=Project_Query.Select_values(Project_Query.GetAllRetest,cnx,argument=(project,expgrp,exp),arg=True)
    ## for each retest get the data
    retest_nameOnly=[]
    for i in range(len(AllRetest)):
        retestName=AllRetest[i][0]
        retest_nameOnly.append(retestName)
        each_retest_data=Project_Query.Select_values(Project_Query.GetAllRetestData,cnx,argument=(project,expgrp,exp,retestName),arg=True)
        Retest_AllValue[retestName]=MergeRowsTogether(each_retest_data)
        retestVariableList[retestName]=BooleanVar()
        retestVariableList[retestName].set(False)
    for ind in range(len(AllRetest)):
        Checkbutton(root, text=AllRetest[ind][0], variable=retestVariableList[AllRetest[ind][0]], onvalue=True,font = "Helvetica 10").grid(column=1, row=1+ind,sticky="W") ## this create check buttons
        Gui_looks.CreateLabels(root,[AllRetest[ind][1],AllRetest[ind][2],AllRetest[ind][3],AllRetest[ind][4]],row_start=1+ind,col_start=3,row=False)
    Entry(root, width=12, textvariable=path).grid(column=3, row=10,columnspan=10,sticky=(W, E))## this create the entry for the path

    Gui_looks.create_button(root,["Browse"],col_start=13,command_input=[lambda:path.set(askdirectory())],s=(E,W),row_start=10)
    Gui_looks.CreateLabels(root,["*Enter the folder location where to save all selected files"],row_start=11,col_start=4,g="red")
    Button(root, text="Export", command=export,fg="red",font = "Helvetica 10",relief=RAISED).grid(column=5, row=12, sticky=W)
    Button(root,text="Toggle",command=lambda:Gui_looks.SelectAllButton(variable=retestVariableList,name=True,nameList=retest_nameOnly),
           fg="dark green",font = "Helvetica 10",relief=RAISED).grid(column=4, row=12, sticky=W)


