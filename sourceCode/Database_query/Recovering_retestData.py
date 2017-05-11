__author__ = 'surya'


from Tkinter import *
from tkFileDialog import askdirectory
from Mysql_queries import questions_query, Project_Query
from Gui_support import Gui_looks
# from Plotting_graph import PlottingDist
# from Mysql_queries import MySqlConnection

def MergeRowsTogetherTreatment(retest_data_list):
    prot2Line={}
    count=0
    for splits in retest_data_list:
        filename=splits[0].strip()
        uniqId=splits[1].strip()
        intensity=splits[4]
        well_type=splits[3]
        if uniqId not in prot2Line:
            prot2Line[uniqId]=[[filename],[splits[2]]+splits[5:],[],[],[],[],[],[]]#[annotation],[NS],[S],[ST],[NSB+],[SB+],[SB+T],[header]
        else:
            if filename not in prot2Line[uniqId][0]:
                prot2Line[uniqId][0].append(filename)
        if well_type=="NS":
            prot2Line[uniqId][2].append(intensity)
        elif well_type=="S":
            prot2Line[uniqId][3].append(intensity)
        elif well_type=="ST":
            prot2Line[uniqId][4].append(intensity)
        elif well_type=="NSB+":
            prot2Line[uniqId][5].append(intensity)
        elif well_type=="SB+":
            prot2Line[uniqId][6].append(intensity)
        elif well_type=="SB+T":
            prot2Line[uniqId][7].append(intensity)
    return  prot2Line

def MergeRowsTogether(retest_data_list):
    prot2Line={}
    count=0
    for splits in retest_data_list:
        filename=splits[0].strip()
        uniqId=splits[1].strip()
        intensity=splits[4]
        well_type=splits[3]
        if uniqId not in prot2Line:
            prot2Line[uniqId]=[[filename],[splits[2]]+splits[5:],[],[],[],[]]#[annotation],[NS],[S],[NSB+],[SB+]
        else:
            if filename not in prot2Line[uniqId][0]:
                prot2Line[uniqId][0].append(filename)
        if well_type=="NS":
            prot2Line[uniqId][2].append(intensity)
        elif well_type=="S":
            prot2Line[uniqId][3].append(intensity)
        elif well_type=="NSB+":
            prot2Line[uniqId][4].append(intensity)
        elif well_type=="SB+":
            prot2Line[uniqId][5].append(intensity)
    return  prot2Line

def MergeRowsTogetherKiss(retest_data_list):
    prot2Line={}
    count=0
    for splits in retest_data_list:
        filename=splits[0].strip()
        uniqId=splits[1].strip()
        intensity=splits[4]
        well_type=splits[3]
        if uniqId not in prot2Line:
            prot2Line[uniqId]=[[filename],[splits[2]]+splits[5:],[],[]]#[annotation],[NS],[S],[NSB+],[SB+]
        else:
            if filename not in prot2Line[uniqId][0]:
                prot2Line[uniqId][0].append(filename)
        if well_type=="B-":
            prot2Line[uniqId][2].append(intensity)
        elif well_type=="B+":
            prot2Line[uniqId][3].append(intensity)
    return  prot2Line


def ExportSelectList(cnx,project,expgrp,exp,path):
    header="FileNames\tUniqueName\tEntrenzNames\tNS\tNS\tNS\tS\tS\tS\tNSB+\tNSB+\tNSB+\tSB+\tSB+\tSB+\tFIbaitNull" \
           "\tFIPreyNull\ttag\twellName\ttype\n"
    headerkiss="FileNames\tUniqueName\tEntrenzNames\tB-\tB-\tB-\tB-\tB-\tB-\tB+\tB+\tB+\tB+\tB+\tB+\tFIbaitNull" \
           "\tFIPreyNull\ttag\twellName\ttype\n"
    headerT="FileNames\tUniqueName\tEntrenzNames\tNS\tNS\tNS\tS\tS\tS\tST\tST\tST" \
          "\tNSB+\tNSB+\tNSB+\tSB+\tSB+\tSB+\tSB+T\tSB+T\tSB+T" \
          "\tFIbaitNull\tFIPreyNull\tFIbaitNullT\tFIPreyNullT\ttag\ttagT\twellName\ttype\n"
    Retest_AllValue={}
    ############# export method
    def export():
        for varindex in range(len(retestVariableList)):
            if retestVariableList[AllRetest[varindex][0]].get():
                treatment = int(AllRetest[varindex][-3])
                kiss = int(AllRetest[varindex][-1])
                exportfile=open(path.get()+"/"+AllRetest[varindex][0]+".txt","w")
                if treatment:
                    exportfile.write(headerT)
                elif kiss:
                    exportfile.write(headerkiss)
                else:
                    exportfile.write(header)
                for protein in Retest_AllValue[AllRetest[varindex][0]]:
                    fileName="_".join(Retest_AllValue[AllRetest[varindex][0]][protein][0])#filenamesTogether
                    entrezName=Retest_AllValue[AllRetest[varindex][0]][protein][1][0]
                    annotations="\t".join(Retest_AllValue[AllRetest[varindex][0]][protein][1][1:])
                    ln="\t".join([fileName,protein,entrezName])+"\t"
                    for index in range(2,len(Retest_AllValue[AllRetest[varindex][0]][protein])):
                        ln+="\t".join(Retest_AllValue[AllRetest[varindex][0]][protein][index])+"\t"
                    ln+=annotations
                    exportfile.write(ln+"\n")
                exportfile.close()
                print "finised writing ",AllRetest[varindex][0],"in the file ",path.get()+"/"+AllRetest[varindex][0]+".txt"
    ###############################################
    retestVariableList={}
    retest_window=Toplevel()
    Gui_looks.Streching([retest_window],100)
    retest_window.geometry("%dx%d+%d+%d" % (1000, 700, 600, 50))

    Gui_looks.CreateLabels(retest_window,["RetestName"],row_start=0,col_start=1,row=False,g="red")
    Gui_looks.CreateLabels(retest_window,"Reason,SubmissionDate,ReTestDate,DoneBy,Treatment,Threshold,Kiss".split(","),row_start=0,col_start=3,row=False,g="red")
    ## get all the re_test for project,experimentgrp and experiments
    AllRetest=Project_Query.Select_values(Project_Query.GetAllRetest,cnx,argument=(project,expgrp,exp),arg=True)
    ## for each retest get the data
    retest_nameOnly=[]
    for i in range(len(AllRetest)):
        retestName=AllRetest[i][0]
        retest_nameOnly.append(retestName)
        treatment=int(AllRetest[i][-3])

        ## first check if the retest is treatment data
        if treatment:
            each_retest_data=Project_Query.Select_values(Project_Query.GetAllRetestDataT,cnx,argument=(project,expgrp,exp,retestName),arg=True)
            each_retest_dataControl=Project_Query.Select_values(Project_Query.GetAllRetestDataConT,cnx,argument=(project,expgrp,exp,retestName),arg=True)
            Retest_AllValue[retestName]=MergeRowsTogetherTreatment(each_retest_data+each_retest_dataControl)
        else:
            each_retest_data=Project_Query.Select_values(Project_Query.GetAllRetestData,cnx,argument=(project,expgrp,exp,retestName),arg=True)
            each_retest_dataControl=Project_Query.Select_values(Project_Query.GetAllRetestDataCon,cnx,argument=(project,expgrp,exp,retestName),arg=True)
            kiss = AllRetest[i][-1]
            if kiss!=None or kiss=="1":
                Retest_AllValue[retestName] = MergeRowsTogetherKiss(each_retest_data + each_retest_dataControl)
            else:
                Retest_AllValue[retestName]=MergeRowsTogether(each_retest_data+each_retest_dataControl)


        retestVariableList[retestName]=BooleanVar()
        retestVariableList[retestName].set(False)
    for ind in range(len(AllRetest)):
        Checkbutton(retest_window, text=AllRetest[ind][0], variable=retestVariableList[AllRetest[ind][0]],
                    onvalue=True,font = "Helvetica 10").grid(column=1, row=1+ind,sticky=(W)) ## this create check buttons
        Gui_looks.CreateLabels(retest_window,AllRetest[ind][1:],row_start=1+ind,col_start=3,row=False)
    Entry(retest_window, width=12, textvariable=path).grid(column=3, row=len(AllRetest)+3,columnspan=10,sticky=(W, E))## this create the entry for the path

    Gui_looks.create_button(retest_window,["Browse"],col_start=13,command_input=[lambda:path.set(askdirectory())],s=(E,W),row_start=len(AllRetest)+3)
    Gui_looks.CreateLabels(retest_window,["*Enter the folder location where to save all selected files"],row_start=len(AllRetest)+4,col_start=4,g="red")
    Button(retest_window, text="Export", command=export,fg="red",font = "Helvetica 10",relief=RAISED).grid(column=5, row=len(AllRetest)+5, sticky=W)
    Button(retest_window,text="Toggle",command=lambda:Gui_looks.SelectAllButton(variable=retestVariableList,name=True,nameList=retest_nameOnly),
           fg="dark green",font = "Helvetica 10",relief=RAISED).grid(column=4, row=len(AllRetest)+5, sticky=W)


