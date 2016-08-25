
__author__ = 'surya'

## importing module
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
import ttk
from Tkinter import PhotoImage
import os
from DatabaseWindows import re_test_window, selection_database_type, DataBaseWindow
from Gui_support import Gui_looks, GuiCommands
from tkMessageBox import *
import Process_Analysis_Normalization
from Mysql_queries import MySqlConnection
from Error_handle import ErrorHandling, checkingDublicateEntry
from Database_query import database_queryWindow
from Database_input import ReTestDatabaseInput
from datetime import date
from Retest import preprocessing
# import Art_Window_Method


background="grey95" # defining background color of GUI

## to get the path of the current dir
path=os.getcwd()


############################################################################################################
############################################################################################################
## call Back Function
def callback():
    if askyesno('Verify', 'Really quit?'):
        root.destroy()

## to set the default options
def default():
    cutoff.set(0.05)
    geneNum.set(0)
    nslist.set("W1")
    slist.set("W2,W3,W4")
    mainfile=file.get()
    pfile_update=mainfile.split("/")[:-1]
    pfile_update.append("linkageFile.txt")
    pfile.set('/'.join(pfile_update))
    link.set('/'.join(mainfile.split("/")[:-1]))
    aspecifics.set("F3Bait.txt")

############################################################################################################
#################################### Run Analysis ##########################################################
############################################################################################################


def files():
    run=False
    ## check if all the important fields are entered
    if ReProcessing.get():
        if os.path.isfile(file.get()) and os.path.isdir(
                link.get()) and cutoff.get() != "" \
                and geneNum.get() != "" and nslist.get() != "" and slist.get() != "" and quartfilt.get() != "":
            run=True
        else:
            ErrorHandling.IO_prob("Please fill all the required field with valid input...")
            run=False
    else:
        if os.path.isfile(pfile.get()) and os.path.isfile(file.get()) and os.path.isdir(link.get()) and cutoff.get()!="" \
                and geneNum.get()!="" and nslist.get()!="" and slist.get()!="" and quartfilt.get() !="" and allprocess.get()!="":
            run=True
        else:
            ErrorHandling.IO_prob("Please fill all the required field with valid input...")
            run=False
    if run:
            ## run the analysis
            path,Positive_count,pplot,Tplate2Path,bait2PlateList,plate2subfolder,AspecificDic,linkageDic,plate_tfileDic=\
                Process_Analysis_Normalization.processAnalysisNormalization(pfile.get(),link.get(),file.get(),analysis.get(),
                float(cutoff.get()),float(geneNum.get()),nslist.get(),slist.get(),quartfilt.get(),allprocess.get(),aspecifics.get(),
                aspecificpresent.get(),PCpresent.get(),PCthreshold.get(),ReProcessing.get(),cnx)

    ## if database are checked and than initiate database entry as well
            if databasedo.get():
                if checkingDublicateEntry.checkExistingInfo(plate2subfolder,cnx):
                    DataBaseWindow.DatabaseEntry(Tplate2Path,bait2PlateList,plate2subfolder,nslist,slist,projname,projReason,expgrpname,baitname,expname,today_date,
                          expReason,Scanningdate,mbubaitcode,baitVectorType,stimulusType,stimulusconc,protocolType,
                        treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,AspecificDic,cnx,mappit,#plateinfo
                          maspit,kiss,treatment,fusioncpd,fusioncpdConc,moleculeExtraInfo,linkageDic,cutoff,
                            PCthreshold,quartfilt,plate_tfileDic,PCpresent,BaitTransfectDate,path)


    #    print "Done !!!"

##########################################################################################################################################################
##########################################################################################################################################################
##########################################   STARTS   ####################################################################################################
##################################################################################################################################################
# define root and frame
root = Tk()
root.title("MAPPI-DAT (Mappit Array Protein-Protein Interaction-Database and Analysis Tool)")
root.geometry("%dx%d+%d+%d" % (1200, 700, 200, 100)) ## length/width/positions..

## define the different tabs
mainframe = ttk.Notebook(root)
mainframe.pack(fill='both', expand='yes')
enter = Frame(mainframe,bg=background )
Overview = Frame(mainframe,bg=background )
Retest=Frame(mainframe,bg=background)

mainframe.add(enter, text='PrimaryScreenAnalysis')
mainframe.add(Retest,text='Re-test Analysis')
mainframe.add(Overview, text='Database Overview')

Gui_looks.Streching([enter,Overview,Retest],10)

####################################################################
## check for mysql connection
cnx=""
try:
    cnx= MySqlConnection.connectSql()

except Exception:
    print("Database is not connected")
    pass

################################################################################
## define picture logos
xml=PhotoImage(file="pictures/xml.gif")
txt = PhotoImage(file="pictures/txt.gif")
folder=PhotoImage(file="pictures/folderIcon.gif")
information_logo=PhotoImage(file="pictures/info.gif")

#################################################################################################
#################################### Entry Window   ###################################
###################################################################################################
Gui_looks.CreateLabels(enter,["Primary Filtration & Analysis"],row_start=0,b=background ,f=("Helvetica", 15, "bold"),col_start=3,s=(W))

file,pfile,link,cutoff,geneNum,nslist,slist,aspecifics,PCthreshold = StringVar(),StringVar(),StringVar(),StringVar(),\
                                StringVar(),StringVar(),StringVar(),StringVar(),StringVar()

analysis,quartfilt,allprocess,databasedo,aspecificpresent,PCpresent,ReProcessing=BooleanVar(),BooleanVar(),BooleanVar(),\
                                BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar()

analysis.set(False)
quartfilt.set(False)
allprocess.set(False)
databasedo.set(False)
PCpresent.set(False)
ReProcessing.set(False)
photos=[]

file_entry = Entry(enter, width=12, textvariable=file)

pfile_entry=Entry(enter, width=12, textvariable=pfile)

link_entry=Entry(enter, width=12, textvariable=link)


asepcific_entry=Entry(enter,width=12,textvariable=aspecifics)

PCthreshold_entry=Entry(enter,textvariable=PCthreshold)
cutoff_entry=Entry(enter,textvariable=cutoff)
geneNum_entry=Entry(enter,textvariable=geneNum)
nslist_entry=Entry(enter,textvariable=nslist)
slist_entry=Entry(enter,textvariable=slist)

analysis_entry = Checkbutton(enter, text=" also include Analysis", variable=analysis, onvalue=True,bg=background ,font = "Helvetica 10")
quartfilt_entry = Checkbutton(enter, text=" also include Quartile Filtration", variable=quartfilt, onvalue=True,bg=background ,font = "Helvetica 10")
allprocess_entry= Checkbutton(enter, text="Process all quantification parameters", variable=all, onvalue=True ,bg=background,font = "Helvetica 10")


###############################################################################################################################################
######################################## run the database input #############################################################################
## check if the database is connected than create cehck button, else dont
if cnx!="":
    databasedo_entry = Checkbutton(enter, text="submit data in database", variable=databasedo, onvalue=True,bg=background ,
                                   command=lambda:(selection_database_type.createPre_databaseWindow(mappit,maspit,kiss,treatment,
                        databasedo,projname,projReason,expgrpname,baitname,expname,expReason,Scanningdate,mbubaitcode,baitVectorType,stimulusType,
                        stimulusconc,protocolType,treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,fusioncpd,
                        fusioncpdConc,moleculeExtraInfo,txt,file.get(),BaitTransfectDate)),font = "Helvetica 10")#lambda:showinfo('Confirmation', 'If want to add data in database than fill the foloowing'))
    databasedo_entry.grid(column=4,row=9, sticky=(W, E))

aspecificpresent_entry = Checkbutton(enter, text="Include A-specific Filtration", variable=aspecificpresent, onvalue=True,bg=background ,font = "Helvetica 10")
PCpresent_entry = Checkbutton(enter, text="Include Particle Count Threshold", variable=PCpresent, onvalue=True,bg=background ,font = "Helvetica 10")
ReProcessing_entry = Checkbutton(enter, text="ReProcess Data", variable=ReProcessing, onvalue=True,bg=background ,font = "Helvetica 10",
        command=lambda: GuiCommands.disableForReprocessing(asepcific_entry,aspecificpresent_entry,host_box=ReProcessing.get()) )


file_entry.grid(column=2, row=1,columnspan=3, sticky=(W, E))
pfile_entry.grid(column=2, row=2,columnspan=3, sticky=(W, E))
link_entry.grid(column=2, row=3,columnspan=3, sticky=(W, E))
asepcific_entry.grid(column=2, row=4,columnspan=3, sticky=(W, E))

PCpresent_entry.grid(column=2,row=5,sticky=E)
PCthreshold_entry.grid(column=3,row=5,sticky=W)
aspecificpresent_entry.grid(column=4,row=5,sticky=W)
ReProcessing_entry.grid(column=1,row=5,sticky=(W, E))


# PlateInfo_entry.grid(column=2, row=6,columnspan=3, sticky=(E,W))
cutoff_entry.grid(column=2,row=7,sticky=(W,E))
geneNum_entry.grid(column=4,row=7,sticky=(W,E))
nslist_entry.grid(column=2,row=8,sticky=(W,E))
slist_entry.grid(column=4,row=8,sticky=(W,E))
analysis_entry.grid(column=1, row=9, sticky=(W, E))
quartfilt_entry.grid(column=2, row=9, sticky=(W, E))
allprocess_entry.grid(column=3, row=9, sticky=(W, E))


Gui_looks.CreateLabels(enter,["XML File Name*","Linkage File*", "Folder Link*","A-specific File",],b=background ,f="Helvetica 10")
Gui_looks.CreateLabels(enter,["q-value threshold*", "Non-Stimulus Wells*"],b=background ,f="Helvetica 10",row_start=7)

Gui_looks.CreateLabels(enter,["Number of Positives*","Stimulus Wells*"],row_start=7,col_start=3,b=background ,f="Helvetica 10")


Button(enter, text="Quit", command=callback,fg="red",font = "Helvetica 10",relief=RAISED).grid(column=3, row=10, sticky=W)
Button(enter, text="Calculate", command=files,fg="dark green",relief=RAISED,font = "Helvetica 10").grid(column=3, row=10, sticky=(E))
Button(enter, text="Fill Out", command=default,fg="Blue",relief=RAISED,font = "Helvetica 10").grid(column=4, row=10, sticky=E)


Button(enter,image=xml,command=(lambda:file.set(askopenfilename())),relief=RAISED,bg="black").grid(column=6,row=1,sticky=(W))
Button(enter,image=txt,command=(lambda: pfile.set(askopenfilename())),relief=RAISED,bg="black").grid(column=6,row=2,sticky=W)
Button(enter,image=folder,command=(lambda:link.set(askdirectory())),relief=RAISED,bg="black").grid(column=6,row=3,sticky=W)
Button(enter,image=txt,command=(lambda: aspecifics.set(askopenfilename())),relief=RAISED,bg="black").grid(column=6,row=4,sticky=W)

#################################################################################################
#################################### OUTPUT file of the statics #################################
###################################################################################################
exportStatistic=StringVar()


#################################################################################################
#################################### Retest WINDOW   ###################################
###################################################################################################


def retest_analysis():
    print "started analysis"
    retest_outputFile=preprocessing.mergeFiles(controlfile.get(),primaryscreenfile.get(),primary2retestlink.get(),retestfolderpath.get(),replicateArrangement.get(),outputfile="ReTestOutputFile.txt")
    print "done with analysis!"
    if retestdatabasewindow.get():
        ReTestDatabaseInput.reTestInput(r_projname.get(),r_expgroup.get(),r_experiment.get(),cnx,retest_reason.get(),retest_outputFile,dnaControlFile.get(),dnaFile.get(),
                                        replicateArrangement.get(),retest_name.get(),today_date,retest_date.get(),doneby.get())

def retestdeafault():
    mainfile=primaryscreenfile.get()
    connection_update=mainfile.split("/")[:-1]
    connection_update.append("Primary2RetestConnection.txt")
    primary2retestlink.set('/'.join(connection_update))
    control_update=mainfile.split("/")[:-1]
    control_update.append("controlFormatFile.txt")
    controlfile.set('/'.join(control_update))
    retestfolderpath.set('/'.join(mainfile.split("/")[:-1]))
    replicateArrangement.set("NS,NS,NS,S,S,S,NSB+,NSB+,NSB+,SB+,SB+,SB+")

Gui_looks.CreateLabels(Retest,["Retest Filtration & Analysis"],row_start=0,b=background ,f=("Helvetica", 15, "bold"),col_start=3,s=(W))

# variables
primaryscreenfile,primary2retestlink,controlfile,retestfolderpath,replicateArrangement=StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
retestdatabasewindow=BooleanVar()
retestdatabasewindow.set(False)

# type of variables
primaryscreenfile_entry = Entry(Retest, width=12, textvariable=primaryscreenfile)
primary2retestlink_entry = Entry(Retest, width=12, textvariable=primary2retestlink)
controlfile_entry = Entry(Retest, width=12, textvariable=controlfile)
retestfolderpath_entry = Entry(Retest, width=12, textvariable=retestfolderpath)
replicateArrangement_entry = Entry(Retest, width=12, textvariable=replicateArrangement)

#position of variables
primaryscreenfile_entry.grid(column=2, row=1,columnspan=4, sticky=(W, E))
primary2retestlink_entry.grid(column=2, row=2,columnspan=4, sticky=(W, E))
controlfile_entry.grid(column=2, row=3,columnspan=4, sticky=(W, E))
retestfolderpath_entry.grid(column=2, row=4,columnspan=4, sticky=(W, E))
replicateArrangement_entry.grid(column=2, row=5,columnspan=4, sticky=(W, E))

# create labels for the entry windows

Gui_looks.CreateLabels(Retest,["PrimaryScreen Analysis File*","Connection File*","Control Format File*", "Folder Link*","Arrangement of Replicates*"],b=background ,f="Helvetica 10",s=(W))

## browse buttons
Button(Retest,image=txt,command=(lambda: primaryscreenfile.set(askopenfilename())),relief=RAISED,bg="black").grid(column=6,row=1,sticky=W)
Button(Retest,image=txt,command=(lambda: primary2retestlink.set(askopenfilename())),relief=RAISED,bg="black").grid(column=6,row=2,sticky=W)
Button(Retest,image=txt,command=(lambda: controlfile.set(askopenfilename())),relief=RAISED,bg="black").grid(column=6,row=3,sticky=W)
Button(Retest,image=folder,command=(lambda:retestfolderpath.set(askdirectory())),relief=RAISED,bg="black").grid(column=6,row=4,sticky=W)

## extra buttons
Button(Retest, text="Fill Out", command=retestdeafault,fg="Blue",relief=RAISED,font = "Helvetica 10").grid(column=4, row=6, sticky=E)

Button(Retest, text="Calculate", command=retest_analysis,fg="dark green",relief=RAISED,font = "Helvetica 10").grid(column=3, row=6, sticky=(E))

## database window submission
if cnx!="":
    retestdatabasewindow_entry = Checkbutton(Retest, text="submit retest data in database", variable=retestdatabasewindow, onvalue=True,bg=background ,
                                   command=lambda:(re_test_window.retest_dbWindow(retestdatabasewindow,r_projname,r_expgroup,r_experiment,dnaFile,
                                                dnaControlFile,retest_reason,txt,retestfolderpath.get(),retest_name,retest_date,doneby)),
                                   font = "Helvetica 10")
    retestdatabasewindow_entry.grid(column=1,row=6, sticky=(W, E))










#################################################################################################
#################################### DATABASE WINDOW   ###################################
###################################################################################################
### for the data base tab:
today_date=date.today()
projname,projReason,expgrpname,baitname,expname,expReason,Scanningdate,mbubaitcode,baitVectorType,stimulusType,\
stimulusconc,protocolType,treatmentType,treatementConc,Treatementdate,treatment_starttime,treatment_endtime,fusioncpd,fusioncpdConc,moleculeExtraInfo,BaitTransfectDate=\
    StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()\
        ,StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()


mappit,maspit,kiss,treatment=BooleanVar(),BooleanVar(),BooleanVar(),BooleanVar()
# molecule=BooleanVar()
# molecule.set(False)

################################### retest screen ###############################################

retest_name,r_projname,r_expgroup,r_experiment,dnaFile,dnaControlFile,retest_reason,retest_date,doneby=\
    StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()





#################################################################################################
#################################### DATABASE query WINDOW   ###################################
###################################################################################################

if cnx:
    database_queryWindow.query_window(Overview,cnx,callback, information_logo)


#################################################################################################
#################################### End the loop   ###################################
###################################################################################################
#cnx.close()
root.mainloop()

