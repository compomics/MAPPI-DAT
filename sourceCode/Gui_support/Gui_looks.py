__author__ = 'surya'

from Tkinter import *
from WebSupport import DirectWebPage
from tkFileDialog import askdirectory

background="grey95"

###
## method to create labels after getting the output

def CreateLabels(Root_frame,list,row_start=1,col_start=1,row=True,b="gray95",f = "Helvetica 8", g="black",s=(W,E)):
    rc=0
    for value in list:
        if row:
            Label(Root_frame, text= value,font=f,bg=b,fg=g).grid(column=col_start, row=row_start+rc, sticky=s)
        else:
            Label(Root_frame, text= value,font=f,bg=b,fg=g).grid(column=col_start+rc, row=row_start, sticky=s)
        rc+=1

##############################################
## method that helps to retain the structure of the GUI when shrink or streched
## defines the column and row with the expansion of the row and col
#
def Streching(lists,length,r=True):
    for i in range(0,length):
        for window in lists:
            window.columnconfigure(i, weight=1)
            if r:
                window.rowconfigure(i,weight=1)



##############################################################
## create a method to create buttons

def create_button(master,text_list,command_input,col=False,row=True,row_start=1,col_start=1,b="gray95",f = "Helvetica 8", g="black",s=(W,E),image=False):
    rc=0
    for entry in text_list:
        if image:
            if row:
                Button(master, image=entry, command=command_input[rc],bg=b,relief=RAISED).grid(column=col_start, row=row_start+rc, sticky=s)
            else:
                Button(master, image=entry, command=command_input[rc],bg=b,relief=RAISED).grid(column=col_start+rc, row=row_start, sticky=s)
        else:
            if row:
                Button(master, text=entry, command=command_input[rc],bg=b,fg=g,font =f,relief=RAISED).grid(column=col_start, row=row_start+rc, sticky=s)
            else:
                Button(master, text=entry, command=command_input[rc],bg=b,fg=g,font =f,relief=RAISED).grid(column=col_start+rc, row=row_start, sticky=s)
        rc+=1

###################################################################################################
#################################################################
## create a list box and put it in the root left side

def createListandadjust(root,height_set,sbp,header_list,output,OnMouseWheel,listboxes,Alluniques,NameCol,index=False,webconnect=False,valcol=0,fontcolor="black",width=18):
    listbox_name=Listbox(root, height=height_set,width=width,fg=fontcolor,yscrollcommand=sbp.set)#,font=("Helvetica", 10, "bold"))
    listbox_name.pack(side="left")
    listbox_name.bind("<MouseWheel>", OnMouseWheel)
    if index:
        namelist=[]
        listbox_name.insert(END,header_list)
        listbox_name.insert(END," ")
        for entry in output:
            listbox_name.insert(END,entry)
            namelist.append(entry)
    else:
        namelist=[]
        listbox_name.insert(END,header_list[valcol])
        listbox_name.insert(END,"---")
        for entry in output:
            listbox_name.insert(END,entry[valcol])
            namelist.append(entry[valcol])
            if webconnect:
                listbox_name.bind('<Double-1>', (lambda event: DirectWebPage.directWeb(listbox_name,Alluniques,NameCol)))
    listboxes.append(listbox_name)

### trial
def checkwork():
    print "under construction"



####################################################################################################################
## create dictionary to give the header for each file
#"Prey,Bait,Molecule,Sd+ Found,Sd+ NotFound,Control Found,Control NotFound,NewHits Found,NewHits NotFound,A-specifics Found,A-specifics NotFound"
#headers={"Prey":"";"Bait":}



## create a separate window
def create_window(output=[],header_list=[],row=False,row_start=1,col_start=1,webActive=False,NameCol=2,rowname=True,smallwid=False):
    root=Toplevel()
    if smallwid:
        root.geometry("%dx%d+%d+%d" % (700, 200, 500, 300))
    Streching([root],20)
    nrow=0
    listboxes=[]
    Alluniques=[]
    if len(output)>10:
        for val in output:
            s=""
            for each in val:
                s=s+each+" "
            Alluniques.append(s)
        def onMouseWheel(event):
            """
            Convert mousewheel motion to scrollbar motion.
            """
            delta = event.delta
            for lb in listboxes:
                lb.yview("scroll", delta, "units")
            # Return 'break' to prevent the default bindings from
            # firing, which would end up scrolling the widget twice.
            return "break"

        def OnVsb(*args):
            for lists in listboxes:
                lists.yview(*args)

        sbp = Scrollbar(root,orient="vertical", command=OnVsb)
        sbp.pack(side="right",fill="y")

        s=range(1,len(Alluniques)+1)
        if len(Alluniques)<=25:
            height_set=len(Alluniques)+5
        else:
            height_set=30
        numcol=len(header_list)
        createListandadjust(root,height_set,sbp,"",s,onMouseWheel,listboxes,Alluniques,NameCol,index=True,width=5)
        for i in range(numcol):
            if i==2:
                createListandadjust(root,height_set,sbp,header_list,output,onMouseWheel,listboxes,Alluniques,NameCol,valcol=i,webconnect=webActive,fontcolor="blue")
            else:
                createListandadjust(root,height_set,sbp,header_list,output,onMouseWheel,listboxes,Alluniques,NameCol,valcol=i)

    else:
        if row:
            CreateLabels(root,header_list,f="Helvetica 10 bold")
            CreateLabels(root,output,f="Helvetica 10",g="dark green",row_start=row_start+nrow,col_start=col_start)
            nrow+=1

        else:
            CreateLabels(root,header_list,f="Helvetica 10 bold",row=False,row_start=0,col_start=2)
            for each in output:
                if rowname:
                    CreateLabels(root,[nrow+1]+each,f="Helvetica 10",g="dark green",row_start=row_start+nrow,col_start=col_start,row=False)
                else:
                    CreateLabels(root,each,f="Helvetica 10",g="dark green",row_start=row_start+nrow,col_start=col_start,row=False)
                nrow+=1


###########################################################################################################################

## create a button which activate all the tick box and deactivate others
def SelectAllButton(variable=[],name=False,nameList=[]):
    if name:
        for eachName in nameList:
            if variable[eachName].get():
                variable[eachName].set(False)
            else:
                variable[eachName].set(True)

    else:
        for index in range(len(variable)):
            # print(variable[index].get())
            if variable[index].get():
                variable[index].set(False)
            else:
                variable[index].set(True)
