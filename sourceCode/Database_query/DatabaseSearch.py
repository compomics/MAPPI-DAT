
__author__ = 'surya'

from Tkinter import *
from tkFileDialog import askdirectory

from Database_query import ExportInformation
from Mysql_queries import questions_query, Project_Query
from Gui_support import Gui_looks
from Plotting_graph import PlottingDist
from Mysql_queries import MySqlConnection
from Database_query import Recovering_retestData


background = "grey95"


def chooseexp(cnx,p_value,e_value,All_experiments,exp_List,Overview,bg_toshow,RetestExportPath,checkNames=[],checkVar=[],checkVarPath=[],info_logo=0):
        if not cnx.is_connected():
            cnx=MySqlConnection.connectSql()
        ExportList={}

        ExportListHeader={"Prey":"Name\tType\tEntrenzName\n",
                          "Bait":"Name\tMBU_bait_code\tbait_vetor_type\n",
                          "Molecule":"fusion_cpd_type\tfusion_cpd_conc\n",
                          "A-specifics Found":"Name\tType\tEntrenzName\tFC\tQ-val\tP_value\tFiltration_label\n",
                          "A-specifics NotFound":"Name\tType\tEntrenzName\n",
                         "NewHits Found":"Name\tType\tEntrenzName\tFC\tQ-val\tP_value\tFiltration_label\n",
                          "NewHits NotFound":"Name\tType\tEntrenzName\n",
                        }

    # try:
        secondIndex=exp_List.curselection()[0]
        expvalue=All_experiments[int(secondIndex)]
 ## for project info
        def getProjectReason():
            project_input=[Project_Query.Select_all(Project_Query.projectInfo,cnx,arg=True,argument=(p_value[-1],p_value[-1],p_value[-1]))[3]]
            Gui_looks.create_window(output=project_input,header_list=["Project Reason or Aim"],row=True,smallwid=True)

        Gui_looks.create_button(Overview,["Project Aim"],b=background,f="Helvetica 10 bold",row_start=2,command_input=[getProjectReason])

## for distribution
        Gui_looks.CreateLabels(Overview,["Distribution"],row=False,col_start=3,row_start=2,b=background,f="Helvetica 10 bold",s=(W))
        def dcheck(*args):
            IntintS=Project_Query.Select_all(Project_Query.Stimulating_intInt,cnx,arg=True,argument=(p_value[-1],e_value[-1],expvalue,dvar.get(),"Stimulating"),int=True)
            IntintNS=Project_Query.Select_all(Project_Query.Stimulating_intInt,cnx,arg=True,argument=(p_value[-1],e_value[-1],expvalue,dvar.get(),"Non-Stimulating"),int=True)
            PlottingDist.create_plot(IntintS,IntintNS,dvar.get())
        dchoices=Project_Query.Select_all(Project_Query.plates,cnx,arg=True,argument=(p_value[-1],e_value[-1],expvalue))

        if dchoices==[]:
            dchoices=["NA"]
        dvar = StringVar()
        dvar.set("Select")
        option=OptionMenu(Overview, dvar, *dchoices, command=dcheck)
        option.grid(column=3,row=3,sticky=W)
##### Replicate
        Gui_looks.CreateLabels(Overview,["Replicates:\tNS\tS"],row=False,col_start=4,row_start=2,b=background,f="Helvetica 10 bold",s=(E))
        repli_input=questions_query.replicateNumber(expvalue,e_value[-1],p_value[-1],cnx)
        Gui_looks.CreateLabels(Overview,["\t"+str(repli_input[1])+"\t"+str(repli_input[2])],row=False,row_start=3,col_start=4,f="Helvetica 10",g="dark green",b=background,s=(E))
## enter analysis parameter window with a button here
        def getAnalysisParameter():
            analysisParameter_input=Project_Query.Select_all(Project_Query.Parameter_Analysis,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1]),int=True)
#            print(analysisParameter_input)
            if analysisParameter_input[2]==0:
                analysisParameter_input[2]="No Quartile Filtration"
            elif analysisParameter_input[2]==1:
                analysisParameter_input[2]="Quartile Filtration is Active"
            Gui_looks.create_window(output=analysisParameter_input,header_list="pfp;particle count filtration;quartile filtration".split(";"),row=True,col_start=3,smallwid=True)

        Gui_looks.create_button(Overview,["Analysis Parameters"],b=background,f="Helvetica 10 bold",row_start=2,col_start=6,command_input=[getAnalysisParameter])

## also add the button for the re_test
        def getRetestDataResults():
            Recovering_retestData.ExportSelectList(cnx,p_value[-1],e_value[-1],expvalue,RetestExportPath)

        Gui_looks.create_button(Overview,["ReTests"],b=background,f="Helvetica 10 bold",row_start=3,col_start=6,command_input=[getRetestDataResults])

## also add the well and quartile filtration

## frame 2
        frame2 = Frame(Overview, borderwidth=5,relief=GROOVE, width=150, height=200,bg=bg_toshow)
        frame2.grid(column=1, row=4, rowspan=5,columnspan=3,sticky=(N,S,W,E))
        Gui_looks.Streching([frame2],8)
## frame 3
        frame3 = Frame(Overview, borderwidth=5,relief=GROOVE, width=200, height=200,bg=bg_toshow)
        frame3.grid(column=4, row=4, rowspan=5,columnspan=3,sticky=(N,S,W,E))
        Gui_looks.Streching([frame3],8)

## Experimental reason window
        def getExpReason():
            All_exp=Project_Query.Select_all(Project_Query.ExpAllInfo,cnx,arg=True,argument=(p_value[-1],e_value[-1],expvalue))[2] ## selects only the reason from the output
            Gui_looks.create_window(output=[All_exp],header_list=["ExperimentReason"],row=True,smallwid=True)

        Gui_looks.CreateLabels(frame2,["Name","Experiment type","Stimulus type","Input Date"],b=bg_toshow,f="Helvetica 10 bold",s=(W))
        Gui_looks.create_button(frame2,["Reason"],b=background,f="Helvetica 10 bold",row_start=1,col_start=3,command_input=[getExpReason])
        Gui_looks.CreateLabels(frame2,["protocol version","stimulus concentration","Transfect Date"],f="Helvetica 10 bold",b=bg_toshow,col_start=3,row_start=2,s=(W))
        All_exp=Project_Query.Select_all(Project_Query.ExpAllInfo,cnx,arg=True,argument=(p_value[-1],e_value[-1],expvalue))
#        print All_exp
        Gui_looks.CreateLabels(frame2,All_exp[0:2],col_start=2,s=(W),f="Helvetica 10",g="dark green",b=bg_toshow) ## this creats labels for experiment name and experiment type
        Allcondition=Project_Query.Select_all(Project_Query.conditionInfowithTreatment,cnx,arg=True,argument=(p_value[-1],e_value[-1],expvalue)) ## output : c.Stimulus_type,c.Stimulus_conc,c.Transfect_date,c.protocol_version,c.input_date
        Gui_looks.CreateLabels(frame2,[Allcondition[0],Allcondition[4]],col_start=2,row_start=3,s=(W),f="Helvetica 10",g="dark green",b=bg_toshow) ## stimulus type, input_date
        Gui_looks.CreateLabels(frame2,[Allcondition[3],Allcondition[1],Allcondition[2]],col_start=4,row_start=2,s=(W),f="Helvetica 10",g="dark green",b=bg_toshow) ## protocol version, stimulus conc, transfect date

        ## make a line if the treatmnet exist in the experiment and than add the value to it
        if Allcondition[5]!="None" and Allcondition[6]!="None" and Allcondition[7]!="None":
            Gui_looks.CreateLabels(frame2,["Treatment Type","Treatment concentration","Treatment Date"],f="Helvetica 10 bold",b=bg_toshow,row=False,row_start=5,s=(W))
            Gui_looks.CreateLabels(frame2,[Allcondition[5],Allcondition[6],Allcondition[7]],row=False,row_start=6,s=(W),f="Helvetica 10",g="dark green",b=bg_toshow) ## stimulus type, input_date
##
#...................................................................................
## Interactors

        bait=Project_Query.Select_all(Project_Query.bait,cnx,arg=True,argument=(p_value[len(p_value)-1],e_value[len(e_value)-1],expvalue)) ## b.b_name,c.mbu_bait_code,c.bait_vector_type
        ExportList["Bait"]=bait
        def get_bait():
            Gui_looks.create_window(bait,"Bait Name;MBU_bait_code;bait_vector_type".split(";"),row=True,col_start=2,smallwid=True)

        prey=Project_Query.Select_values(Project_Query.AllPrey,cnx,arg=True,argument=(expvalue,e_value[0],p_value[0]))
        ExportList["Prey"]=prey
#        print prey
        def get_prey():
            Gui_looks.create_window(prey,"Name Type EntrenzName".split(),webActive=True)

        molecule_found=Project_Query.Select_all(Project_Query.molecule,cnx,arg=True,argument=(p_value[len(p_value)-1],e_value[len(e_value)-1],expvalue))#m.fusion_cpd_type,m.fusion_cpd_conc
        ExportList["Molecule"]=molecule_found

        def get_molecule():
            Gui_looks.create_window(molecule_found,"fusion_cpd_type; fusion_cpd_concentration".split(";"),row=True,col_start=2,smallwid=True)

        Gui_looks.CreateLabels(frame3,["Interactors: "],b=bg_toshow ,f="Helvetica 10 bold")
    ## get buttons
        Gui_looks.create_button(frame3,"Prey Bait Molecule".split(),b=background,f="Helvetica 10 bold",col_start=2,row=False,command_input=[get_prey,get_bait,get_molecule])
    ## get counts
        interactor_input=Project_Query.Select_all(Project_Query.All_interactor,cnx,arg=True,argument=(p_value[-1],e_value[-1],
        expvalue,p_value[-1],e_value[-1],expvalue,p_value[-1],e_value[-1],expvalue))
        Gui_looks.CreateLabels(frame3,interactor_input,row=False,row_start=2,col_start=2,f="Helvetica 10",g="dark green",b=bg_toshow)
#......................................................................................

## Positives Found:
    ## A-specific
        aspecific_inut=Project_Query.Select_values(Project_Query.select_positives,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"A-specific"))
        aspecific_inut.sort(key=lambda x: (float(x[5]),float(x[4])))
        ExportList["A-specifics Found"]=aspecific_inut
        def a_specific():
            Gui_looks.create_window(aspecific_inut,"Name Type EntrenzName fc qval P_value FiltrationLabel".split(),webActive=True)

    ## new hits
        na=Project_Query.Select_values(Project_Query.select_positives,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"NA"))
        sd=Project_Query.Select_values(Project_Query.select_positives,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"NAsd+"))
        c=Project_Query.Select_values(Project_Query.select_positives,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"NAc+"))
        pos_final=c+sd+na
        pos_final.sort(key=lambda x: (float(x[5]),float(x[4])))
        ExportList["NewHits Found"]=pos_final
        def pos_NA():
            Gui_looks.create_window(pos_final,"Name Type EntrenzName FC qval P_value FiltrationLabel".split(),webActive=True)

    ## create the labels for the matrix
        Gui_looks.CreateLabels(frame3,["New_Hits","A-specific" ],b=bg_toshow,f="Helvetica 10 bold",row_start=3,col_start=2,row=False)
    ## get buttons
#        Gui_looks.create_button(frame3,["SD+","Control+","New_Hits","A-specific" ],b=background,f="Helvetica 10 bold",row_start=3,col_start=2,row=False,command_input=[pos_SD,pos_controls,pos_NA,a_specific])
        Gui_looks.CreateLabels(frame3,["Positive Found "],b=bg_toshow ,f="Helvetica 10 bold",row_start=4)
    ## get count
        pos_input=[]
        pos_input=(questions_query.PositivesFound(expvalue,e_value[-1],p_value[-1],cnx))
        Gui_looks.create_button(frame3,pos_input,row=False,row_start=4,col_start=2,f="Helvetica 10",g="dark green",b=background,command_input=[pos_NA,a_specific])
## Not Found
        Gui_looks.CreateLabels(frame3,["Not Found "],b=bg_toshow ,f="Helvetica 10 bold",row_start=5)
    ## NA not found
        na_nf=Project_Query.Select_values(Project_Query.NotFound,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"NA",expvalue,e_value[-1],p_value[-1],"NA"))
        nac_nf=Project_Query.Select_values(Project_Query.NotFound,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"NAc+",expvalue,e_value[-1],p_value[-1],"NAc+"))
        nas_nf=Project_Query.Select_values(Project_Query.NotFound,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"NAsd+",expvalue,e_value[-1],p_value[-1],"NAsd+"))
        nafinal_nf=na_nf+nac_nf+nas_nf
        ExportList["NewHits NotFound"]=nafinal_nf
        def NFna():
            nafinal_nf.sort(key=lambda x: (x[0]))
            Gui_looks.create_window(nafinal_nf,"Name Type EntrenzName".split(),webActive=True)
    ## Aspecific not found
        aspec_nf=Project_Query.Select_values(Project_Query.NotFound,cnx,arg=True,argument=(expvalue,e_value[-1],p_value[-1],"A-specific",expvalue,e_value[-1],p_value[-1],"A-specific"))
        ExportList["A-specifics NotFound"]=aspec_nf
        def NFaspec():
            aspec_nf.sort(key=lambda x: (x[0]))
            Gui_looks.create_window(aspec_nf,"Name Type EntrenzName".split(),webActive=True)


    ## get count
        NotFound=[]
        # NotFound=[len(sd_nf)]
        # NotFound.append(len(control_nf))
        NotFound.append(len(nafinal_nf))
        NotFound.append(len(aspec_nf))
        Gui_looks.create_button(frame3,NotFound,row=False,row_start=5,col_start=2,f="Helvetica 10",g="dark green",b=background,command_input=[NFna,NFaspec])

##............................................................................................................................

## check which of the arguments are selected and than print the related file
        def export():
            for varindex in range(len(checkVar)):
                if checkVar[varindex].get():
                    exportfile=open(checkVarPath[0].get()+"/"+checkNames[varindex]+".txt","w")
                    exportfile.write(ExportListHeader[checkNames[varindex]])
#                    print checkVarPath[varindex].get()
                    if checkNames[varindex] in ["Bait","Molecule"]:
                        exporline=[]
                        for lines in ExportList[checkNames[varindex]]:
                                exporline.append(lines+"\t")
                        exporline.append("\n")
    #                        print exporline
                        exportfile.writelines(exporline)
                    else:
#                        print(ExportList[checkNames[varindex]])
                        for lines in ExportList[checkNames[varindex]]:
                            exporline=[]
                            for val in lines:
                                exporline.append(str(val)+"\t")
                            exporline.append("\n")
    #                        print exporline
                            exportfile.writelines(exporline)
                    exportfile.close()
                    print "finised writing ",checkNames[varindex],"in the file ",checkVarPath[0].get()+"/"+checkNames[varindex]+".txt"

## create the export buttons
        ### trial
        def checkwork():
            print "under construction"


        def ExportSelectList():
#            Gui_looks.create_window(checkbox=True,checknames=checkNames,checkVar=checkVar,checkvarpath=checkVarPath,information=info_logo,buttoncommand=export)
            root=Toplevel()
            Gui_looks.Streching([root],20)
            root.geometry("%dx%d+%d+%d" % (1000, 500, 200, 100))
            for ind in range(len(checkNames)):
                Checkbutton(root, text=checkNames[ind], variable=checkVar[ind], onvalue=True,font = "Helvetica 10").grid(column=1, row=1+ind,sticky="W") ## this create check buttons
            Entry(root, width=12, textvariable=checkVarPath[0]).grid(column=2, row=14,columnspan=10,sticky=(W, E))## this create the entry for the path

            Gui_looks.CreateLabels(root,[ExportInformation.prey,ExportInformation.bait,ExportInformation.molecule,ExportInformation.NewHitsFound,ExportInformation.NewHitNotFound,
                                         ExportInformation.AspecificFound,ExportInformation.AspecificNotFound],col_start=2,s=(W))
            Gui_looks.create_button(root,["Browse"],col_start=13,command_input=[lambda:checkVarPath[0].set(askdirectory())],s=(E,W),row_start=14)
            Gui_looks.CreateLabels(root,["*Enter the folder location where to save all selected files"],row_start=15,col_start=2,g="red")
            Button(root, text="Export", command=export,fg="red",font = "Helvetica 10",relief=RAISED).grid(column=3, row=16, sticky=W)
            Button(root,text="Toggle",command=lambda:Gui_looks.SelectAllButton(variable=checkVar),fg="dark green",font = "Helvetica 10",relief=RAISED).grid(column=2, row=16, sticky=W)

### more window option

        def MoreWindow():
            root=Toplevel()
            Gui_looks.Streching([root],20)
            root.geometry("%dx%d+%d+%d" % (300, 300, 200, 100))
            Gui_looks.create_button(root,["Plates"],[checkwork],col_start=2,g="black",f = "Helvetica 10 bold")
            Gui_looks.create_button(root,"Art Wells Tplate".split(),[checkwork]*3,row_start=2,row=False,g="black",f = "Helvetica 10 bold")
            Gui_looks.create_button(root,["Mixtures"],[checkwork],row_start=3,col_start=2,g="black",f = "Helvetica 10 bold")


        ## button to choose
        Button(Overview, text="Export Selections", command=ExportSelectList,font = "Helvetica 10 bold",relief=RAISED).grid(column=5, row=10, sticky=W)

