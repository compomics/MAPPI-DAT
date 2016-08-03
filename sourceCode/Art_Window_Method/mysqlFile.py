__author__ = 'surya'

from Tkinter import *
import mysql.connector
from tkMessageBox import *
from Mysql_queries import MySqlConnection
import ttk
####################################################################
## check for mysql
cnx=""
try:
    cnx= MySqlConnection.connectSql()
except Exception:
    print("Database is not connected")
    pass


## submitting art value to the database

def IO_prob(problem):
    showerror("Error", problem)

## inserting only
artConc_query=(""" insert into art_conc (row_col_name,concentration,ratio,ref_artid) values (%s,%s,%s,%s) """)
art_query=("""insert into art_main (art_name,art_date,prepared_by,extra_info) values (%s,%s,%s,%s)""")
art_aliqot_query=("""insert into art_info (ali_name,ali_date,prepared_by,extra_info,ref_artid) values (%s,%s,%s,%s,%s)""")
aliqot2mix_query=("""insert into aliqot2mix (ref_aliqotid,ref_mixid) values (%s,%s)""")
mixture_query=("""insert into mixtureinfo (mix_date,Madeby,m_type,extra_info,mixplate_name,No_art_Info) values (%s,%s,%s,%s,%s,%s)""")
tplate_query=("""insert into plates (p_name,printingDate,prepared_by,ref_mixinfoid,extra_info) values (%s,%s,%s,%s,%s) """)

## checking entries

checkingARTid="""SELECT art_id,art_name,art_date from art_main"""
checkingART_aliqotid= """SELECT ali_id,ali_name,ali_date from art_info"""
checkingMix="""SELECT mix_id,mixplate_name,mix_date,m_type from mixtureinfo """

def getAlldatafromDB(Query,three=False):
    name_date2id={}
    cursor3 = cnx.cursor()
    cursor3.execute(Query)
    if three:
        for (first,second,third,fourth) in cursor3:
            # print first,second,third,str(fourth)
            if second+"_"+str(third)+"_"+fourth not in name_date2id:
                name_date2id[second+"_"+str(third)+"_"+fourth]=first
    else:
        for (first,second,third) in cursor3:
            if second+"_"+str(third) not in name_date2id:
                name_date2id[second+"_"+str(third)]=first
    cursor3.close()
    return name_date2id

## get all the dic for all values in the database
art_name_date_2_id_dic=getAlldatafromDB(checkingARTid)
artAliqot_name_date_2_id_dic=getAlldatafromDB(checkingART_aliqotid)
mix_name_date2id_dic=getAlldatafromDB(checkingMix,three=True)


def addArt(aName,aDate,aPrep,extra_info,artConcFileName,root):
    if aName.get()=="" or aDate.get()=="" or aPrep.get()=="" :
        IO_prob("Please fill all the required field with valid input...")
    elif aName.get()+"_"+aDate.get() in art_name_date_2_id_dic:
        IO_prob(" ART name with same date exist. Dublicate entries are not allowed....")
    else:
        cursor1 = cnx.cursor()
        cursor1.execute(art_query,(aName.get(),aDate.get(),aPrep.get(),extra_info.get()))
        refid=cursor1.lastrowid
        art_name_date_2_id_dic[aName.get()+"_"+aDate.get()]=refid
        with open(artConcFileName.get()) as concFile:
            next(concFile)
            for line in concFile:
                splits=line.split("\t")
                name=splits[0].strip()
                comc=float(splits[6].strip())
                ratio=float(splits[5].strip())
                cursor1.execute(artConc_query,(name,comc,ratio,refid))
        print "added...."
        ttk.Label(root, text="finished adding your entry..").grid(column=3, row=8)
        cnx.commit()


def addArtaliqot(aName,aDate,aPrep,artName,artDate,extra_info,root):
    cursor1 = cnx.cursor()
    if aName.get()=="" or aDate.get()=="" or aPrep.get()=="" or artName=="" or artDate=="":
        IO_prob("Please fill all the required field with valid input...")
    elif aName.get()+"_"+str(aDate.get()) in artAliqot_name_date_2_id_dic:
        IO_prob(" ART name with same date exist. Dublicate entries are not allowed....")
    elif artName.get()+"_"+str(artDate.get()) not in art_name_date_2_id_dic:
        IO_prob(" ART name and date does not exist in the database, please check or insert ART entries  in the database ....")
    else:
        ref_artid=art_name_date_2_id_dic[artName.get()+"_"+str(artDate.get())]
        cursor1.execute(art_aliqot_query,(aName.get(),aDate.get(),aPrep.get(),extra_info.get(),ref_artid))
        artAliqot_name_date_2_id_dic[aName.get()+"_"+str(aDate.get())]=cursor1.lastrowid
        print "added...."
        ttk.Label(root, text="finished adding your entry..").grid(column=3, row=8)
        cnx.commit()



def addMixture(listbox,tplate,mix_date,prep_by,m_type,extra_info,date2Aliqot,root,NoArtInfo):
    if NoArtInfo:
        noArt="True"
    else:
        noArt="False"
    if tplate=="" or mix_date=="" or prep_by=="" or m_type=="":
        IO_prob("Please fill all the required field with valid input...")
    elif tplate+"_"+mix_date in mix_name_date2id_dic:
        IO_prob("plate with same name and date already exist..")
    elif not NoArtInfo and len(listbox.get(0,END))!=18:
        # print "i am stuck here at No art one...."
            IO_prob(" Please select 18 ART plates...")
        # print date2Aliqot
    else:
        cursor1=cnx.cursor()
        cursor1.execute(mixture_query,(mix_date,prep_by,m_type,extra_info,tplate,noArt))
        # print "i came here"
        mix_id=cursor1.lastrowid
        mix_name_date2id_dic[tplate+"_"+mix_date]=mix_id
        # cursor1.execute(tplateSmall_query,(tplate,mix_id))
        if not NoArtInfo:
            for art_aliqot in date2Aliqot:
                if date2Aliqot[art_aliqot][0]+"_"+date2Aliqot[art_aliqot][1] in artAliqot_name_date_2_id_dic:
                    aliqot_id=artAliqot_name_date_2_id_dic[date2Aliqot[art_aliqot][0]+"_"+date2Aliqot[art_aliqot][1]]
                    cursor1.execute(aliqot2mix_query,(aliqot_id,mix_id))
                else:
                    IO_prob("aliqot cannot be found with the same name and date")
        cnx.commit()
        ttk.Label(root, text="finished adding your entry..").grid(column=3, row=9)
    #     print art_aliqot


def getRecentDatesforAliqotes(query):
    dates2names={}
    dates=[]
    cursor3 = cnx.cursor()
    cursor3.execute(query)
    for (first,second,third) in cursor3:
        if str(third) not in dates2names:
            dates2names[str(third)]=[second]
            if third not in dates:
                dates.append(third)
        else:
            dates2names[str(third)].append(second)
    cursor3.close()
    dates.sort(reverse=True)
    return dates,dates2names

## if there is a proble with user than prompt a window saying the problem
def addScreeningInfo(tplate_start,tplate_end,tdate,prepBy,extra_info,MixT,MixDate,MixType,root):
    if tplate_start.get()=="" or tplate_end.get()==""or tdate.get()=="" or prepBy.get()=="" or MixT.get()=="" or MixDate.get()=="" or MixType.get()=="":
        IO_prob("Please fill all the required field with valid input...")
    # elif aName.get()+"_"+aDate.get() in art_name_date_2_id_dic:
    #     IO_prob(" ART name with same date exist. Dublicate entries are not allowed....")
    elif MixT.get()+"_"+str(MixDate.get())+"_"+MixType.get() not in mix_name_date2id_dic:
        IO_prob(" please enter valid plate name and date.. this is not found in database")
    else:
        ref_mix_id=mix_name_date2id_dic[MixT.get()+"_"+str(MixDate.get())+"_"+MixType.get()]
        cursor1 = cnx.cursor()
        for each in range(int(tplate_start.get()),int(tplate_end.get())+1):
            platename=MixT.get()+"-"+str(each)
            cursor1.execute(tplate_query,(platename,tdate.get(),prepBy.get(),ref_mix_id,extra_info.get()))
            print "added...."
            ttk.Label(root, text="finished adding your entry..").grid(column=3, row=9)
        cnx.commit()

    # print tplate_start.get(),tplate_end.get(),tdate.get(),prepBy.get(),extra_info.get(),MixT.get(),MixDate.get()

