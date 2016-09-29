__author__ = 'surya'

from Tkinter import *
import ttk
from tkFileDialog import askopenfilename
from Gui_support.Gui_looks import *
from mysqlFile import *

from datetime import date,time,datetime
today_date= date.today()


from tkMessageBox import *

##########


## method for opening the art window
def artWindow():
    # txt = PhotoImage(file="txt.gif")
    artName,art_date,prepBy, extra_info,artConcFilename=StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    art_date.set(today_date)
    # extra
    # extra_info.set("Testing database")
    # artConcFilename.set("C:/Users/surya/Desktop/ProjectData/MAPPI-DATdata/sampleFor1replicate/DnaConcentrationFile.txt")
    # prepBy.set("Surya")



    root=Toplevel()
    root.title(" ART Info Input window ")
    # if smallwid:
    root.geometry("%dx%d+%d+%d" % (500, 250, 500, 300))
    Streching([root],15)
    ttk.Label(root, text=" ART number/name ").grid(column=1, row=2, sticky=W)
    ttk.Entry(root, width=7, textvariable=artName).grid(column=2, row=2, sticky=(W, E))
    # date
    ttk.Label(root, text="date for preparation ").grid(column=1, row=3, sticky=W)
    ttk.Entry(root, width=7, textvariable=art_date).grid(column=2, row=3, sticky=(W, E))
    ttk.Label(root, text="  yyyy-mm-dd").grid(column=3, row=3, sticky=W)
    # prepared by
    ttk.Label(root, text="prepared by ").grid(column=1, row=4, sticky=W)
    ttk.Entry(root, width=7, textvariable=prepBy).grid(column=2, row=4, sticky=(W, E),columnspan=3)
    ## extra info
    ttk.Label(root, text="extra info. ").grid(column=1, row=5, sticky=W)
    ttk.Entry(root, width=7, textvariable=extra_info).grid(column=2, row=5, sticky=(W, E),columnspan=3)
    ## ask for the concentration file
    ttk.Label(root, text="Concentration File ").grid(column=1, row=6, sticky=W)
    ttk.Entry(root, width=7, textvariable=artConcFilename).grid(column=2, row=6, sticky=(W, E),columnspan=3)
    Button(root,text="Browse",command=(lambda: artConcFilename.set(askopenfilename())),relief=RAISED).grid(column=7,row=6,sticky=W)



    # buttons for save and close
    ttk.Button(root, text="Save", command=lambda:(addArt(artName,art_date,prepBy,extra_info,artConcFilename,root))).grid(column=1, row=7, sticky=W)
    ttk.Button(root, text="Close", command=root.destroy).grid(column=2, row=7, sticky=W)
######################################################################################################################
####################### art aliqot window ###############################################################


def artAliqotWindow():
    artName,art_date,prepBy,bigArtName,bigArtDate, extra_info=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    art_date.set(today_date)
    bigArtDate.set(today_date)
## testing
    # extra_info.set("Testing database")
    # prepBy.set("Surya")

    root=Toplevel()
    root.title(" ART Aliqot Info Input window ")
    # if smallwid:
    root.geometry("%dx%d+%d+%d" % (600, 250, 500, 300))
    Streching([root],20)
    ttk.Label(root, text=" ARTaliqot number/name ").grid(column=1, row=2, sticky=W)
    ttk.Entry(root, width=7, textvariable=artName).grid(column=2, row=2, sticky=(W, E))
    # date
    ttk.Label(root, text=" date for preparation ").grid(column=3, row=2, sticky=W)
    ttk.Entry(root, width=7, textvariable=art_date).grid(column=4, row=2, sticky=(W, E))
    ttk.Label(root, text="  yyyy-mm-dd").grid(column=4, row=3, sticky=W)
    # prepared by
    ttk.Label(root, text=" prepared by ").grid(column=1, row=3, sticky=W)
    ttk.Entry(root, width=7, textvariable=prepBy).grid(column=2, row=3, sticky=(W, E))
    ## art extra info
    ttk.Label(root, text=" extra info. ").grid(column=1, row=5, sticky=W)
    ttk.Entry(root, width=7, textvariable=extra_info).grid(column=2, row=5, sticky=(W, E),columnspan=3)
    ## art
    ttk.Label(root, text=" ART name ").grid(column=1, row=6, sticky=W)
    ttk.Entry(root, width=7, textvariable=bigArtName).grid(column=2, row=6, sticky=(W, E))
    ## art date
    ttk.Label(root, text=" ART date for preparation ").grid(column=3, row=6, sticky=W)
    ttk.Entry(root, width=7, textvariable=bigArtDate).grid(column=4, row=6, sticky=(W, E))
    ttk.Label(root, text="  yyyy-mm-dd").grid(column=4, row=7, sticky=W)



    # buttons for save and close
    ttk.Button(root, text="Save", command=lambda:(addArtaliqot(artName,art_date,prepBy,bigArtName,bigArtDate,extra_info,root))).grid(column=1, row=8, sticky=W)
    ttk.Button(root, text="Close", command=root.destroy).grid(column=2, row=8, sticky=W)

######################################################################################################################
####################### mixtures ###############################################################
date2Aliqot={}
global date2Aliqot

def AddSelectedaliqotes(dates,date2aliqot,curserSelection,aliqotList,finalBox,frame1):
    date2aliqot[finalBox.size()]=[aliqotList[curserSelection],dates]
    finalBox.insert(END,aliqotList[curserSelection])
    ttk.Label(frame1, text=" the selected items are: "+str(len(date2aliqot))).grid(column=6, row=2, sticky=W)
    # print date2aliqot

def deletebutton(cursonSelection,finalBox,date2Ali,frame1):
    finalAli_List=finalBox
    finalAli_List.delete(ANCHOR)
    # print cursonSelection
    del date2Ali[cursonSelection]
    # date2Ali = {key: value for key, value in date2Ali.items() if value != cursonSelection}
    for i in range(cursonSelection,finalBox.size()):
        date2Ali[i]=date2Ali.pop(i+1)
    ttk.Label(frame1, text=" the selected items are: "+str(len(date2Ali))).grid(column=6, row=2, sticky=W)
    # print date2Ali
    # print dates
    # if dates in date2Ali:
    #     if date2nameList[dates][finalBox.curselection()[0]] in date2Ali[dates]:
    #         date2Ali[dates].remove(date2nameList[dates][finalBox.curselection()[0]])
    #         print date2nameList[dates][finalBox.curselection()[0]]



def aliqotesNames(frame1,dates_index,date2name,dateList,date2Aliqot,root,finalBox,tplate,mix_date,prep_by,m_type,extra_info,haveArtInfo):
## list2
    aliqotBox  = Listbox(frame1, height=5,fg="blue")
    aliqotBox.grid(column=3, row=2, sticky=(W,E))

    value = dateList[int(dates_index)]
    for each in date2name[str(value)]:
        aliqotBox.insert(END,each)
    sbp = Scrollbar(frame1,orient=VERTICAL)
    sbp.grid(column=3, row=2, sticky=(E))
    sbp.configure(command=aliqotBox.yview)
    aliqotBox.configure(yscrollcommand=sbp.set)

    ## add and delete buttons
    ttk.Button(frame1, text="Add", command=lambda:(AddSelectedaliqotes(str(value),date2Aliqot,aliqotBox.curselection()[0],date2name[str(value)],finalBox,frame1))).grid(column=4, row=2, sticky=N)
    ttk.Button(frame1, text="Delete", command=lambda: (deletebutton(finalBox.curselection()[0],finalBox,date2Aliqot,frame1))).grid(column=4, row=2, sticky=S)

    ttk.Button(root, text="Save", command=lambda:(addMixture(finalBox,tplate.get(),mix_date.get(),prep_by.get(),m_type.get(),extra_info.get(),date2Aliqot,root,haveArtInfo.get()))).grid(column=1, row=10, sticky=W)

def createSaveButtonForMissingArt(root,tplate,mix_date,prep_by,m_type,extra_info):
    ttk.Button(root, text="Save", command=lambda:(addMixture([],tplate.get(),mix_date.get(),prep_by.get(),m_type.get(),extra_info.get(),{},root,True))).grid(column=1, row=10, sticky=W)


def mixtureWindow():
    mix_date,mixprep,tplate,type,extra_info,m_type=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    NoArtInfo=BooleanVar()
    mix_date.set(today_date)
    NoArtInfo.set(False)

    root=Toplevel()
    root.title(" Mixtures info Input window ")
    # if smallwid:
    root.geometry("%dx%d+%d+%d" % (1000, 400, 200, 100))
    Streching([root],20)
    ## making frames
    frame1 = Frame(root, borderwidth=5,relief=GROOVE)
    frame1.grid(column=1, row=6,columnspan=8,sticky=(N,S,W,E))
    Streching([frame1],8)

    # date
    ttk.Label(root, text="date for preparation ").grid(column=1, row=1, sticky=(W, E))
    ttk.Entry(root, width=7, textvariable=mix_date).grid(column=2, row=1, sticky=(W, E))
    ttk.Label(root, text="  yyyy-mm-dd").grid(column=3, row=1, sticky=W)

    # prepared by
    ttk.Label(root, text="prepared by ").grid(column=1, row=2, sticky=(W, E))
    ttk.Entry(root, width=7, textvariable=mixprep).grid(column=2, row=2, sticky=(W, E))
    ## t plate
    ttk.Label(root, text="  PlateName ").grid(column=3, row=2, sticky=W)
    ttk.Entry(root, width=7, textvariable=tplate).grid(column=4, row=2, sticky=(W, E))

    ## extra info
    ttk.Label(root, text="extra info. ").grid(column=1, row=3, sticky=W)
    ttk.Entry(root, width=7, textvariable=extra_info).grid(column=2, row=3, sticky=(W, E),columnspan=3)

    ## mixture type
    ttk.Label(root, text="mixture type ").grid(column=1, row=4, sticky=(W, E))
    ttk.Entry(root, width=7, textvariable=m_type).grid(column=2, row=4, sticky=(W, E))
    ttk.Label(root, text=" only A or B ").grid(column=3, row=4, sticky=W)

    ## to check if the art info is present or not
    Checkbutton(root, text="Art Info Not Present", variable=NoArtInfo, command=lambda:createSaveButtonForMissingArt(root,tplate,mix_date,mixprep,m_type,extra_info),
                onvalue=True,bg=background).grid(column=4,row=4, sticky=(W, E))

    ## select the 18 assays
    ttk.Label(root, text=" Select 18 assays for the 12 mixtures ").grid(column=2, row=5, sticky=W,columnspan=3)


    ## get all the recent dates
    date_List  = Listbox(frame1, height=5,fg="blue")
    date_List.grid(column=1, row=2, sticky=(W,E))
    aliqot_datesList,aliqotdates2nameDic=getRecentDatesforAliqotes(checkingART_aliqotid)
    for each in aliqot_datesList[0:10]:
        date_List.insert(END,each)
    sbp = Scrollbar(frame1,orient=VERTICAL)
    sbp.grid(column=1, row=2, sticky=(E))
    sbp.configure(command=date_List.yview)
    date_List.configure(yscrollcommand=sbp.set)
    date_List.bind('<Double-1>', (lambda event:(aliqotesNames(frame1,date_List.curselection()[0],
                                aliqotdates2nameDic,aliqot_datesList,date2Aliqot,root,finalAli_List,tplate,mix_date,mixprep,m_type,extra_info,NoArtInfo))))


## list3
    finalAli_List  = Listbox(frame1, height=5,fg="blue")
    finalAli_List.grid(column=5, row=2, sticky=(W,E))
    sbp = Scrollbar(frame1,orient=VERTICAL)
    sbp.grid(column=5, row=2, sticky=(E))
    sbp.configure(command=finalAli_List.yview)
    finalAli_List.configure(yscrollcommand=sbp.set)

    # buttons for save and close
    ttk.Button(root, text="Close", command=root.destroy).grid(column=2, row=10, sticky=W)



######################################################################################################################
####################### T-plate screening ###############################################################


def ScreeningWindow():
    tplate_start,tplate_end,tdate,prepBy,extra_info,MixT,MixDate,MixType=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()
    tdate.set(today_date)
    MixDate.set(today_date)
    # tplate_start.set(60)
    # tplate_end.set(65)
    # prepBy.set("surya")
    # extra_info.set("testing database")

    root=Toplevel()
    root.title(" Printing Details Input window ")
    # if smallwid:
    root.geometry("%dx%d+%d+%d" % (700, 300, 500, 300))
    Streching([root],20)
    # ttk.Label(root, text="____________________________________T plate Screening___________________________________").grid(column=1, row=1, sticky=W,columnspan=10)
    # Start
    ttk.Label(root, text="Start").grid(column=1, row=2, sticky=W)
    ttk.Entry(root, width=7, textvariable=tplate_start).grid(column=2, row=2, sticky=(W, E))
    # end
    ttk.Label(root, text="  End ").grid(column=3, row=2, sticky=W)
    ttk.Entry(root, width=7, textvariable=tplate_end).grid(column=4, row=2, sticky=(W, E),columnspan=2)

    # prepared by
    ttk.Label(root, text= " prepared by ").grid(column=1, row=3, sticky=W)
    ttk.Entry(root, width=7, textvariable=prepBy).grid(column=2, row=3, sticky=(W, E))
    # date
    ttk.Label(root, text=" Preparation Date ").grid(column=3, row=3, sticky=W)
    ttk.Entry(root, width=7, textvariable=tdate).grid(column=4, row=3, sticky=(W, E),columnspan=2)
    ttk.Label(root, text=" yyyy-mm-dd").grid(column=6, row=3, sticky=E)
    ## art extra info
    ttk.Label(root, text="extra info. ").grid(column=1, row=4, sticky=W)
    ttk.Entry(root, width=7, textvariable=extra_info).grid(column=2, row=4, sticky=(W, E),columnspan=4)

    ttk.Label(root, text="____________________________________Mixture Plate Info____________________________________").grid(column=1, row=5, sticky=W, columnspan=10)


    ## art
    ttk.Label(root, text=" Mixture plate Name ").grid(column=1, row=6, sticky=W)
    ttk.Entry(root, width=7, textvariable=MixT).grid(column=2, row=6, sticky=(W, E))
    ## art date
    ttk.Label(root, text=" Mixture Date ").grid(column=3, row=6, sticky=W)
    ttk.Entry(root, width=7, textvariable=MixDate).grid(column=4, row=6, sticky=(W, E),columnspan=2)
    ttk.Label(root, text="  yyyy-mm-dd").grid(column=6, row=6, sticky=E)

    ttk.Label(root, text="  Mixture Type").grid(column=3, row=7, sticky=W)
    ttk.Entry(root, width=7, textvariable=MixType).grid(column=4, row=7, sticky=(W, E))
    ttk.Label(root, text=" A or B ").grid(column=5, row=7, sticky=E)

    # buttons for save and close
    ttk.Button(root, text="Save", command=lambda:(addScreeningInfo(tplate_start,tplate_end,tdate,prepBy,extra_info,MixT,MixDate,MixType,root))).grid(column=1, row=8, sticky=W)
    ttk.Button(root, text="Close", command=root.destroy).grid(column=2, row=8, sticky=W)
