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
art_input=("""insert into art (a_name,) values (%s,)""")
artwell_query=(""" insert into art_well (w_name) values (%s,%s,%s) """)
artwellinfo_query=("""insert into art_well_info (conc,ratio,ref_artwellid) values (%s,%s,%s)""")
art2wellinfo_query=("""insert into art2well_info (ref_artwellid,ref_artinfoid) values (%s,%s)""")
art_well_relation=("""insert into artwell_has_art (refwellid,ref_artid) values (%s,%s)""")
art_info_query=("""insert into art_info (art_date,prepared_by,extra_info) values (%s,%s,%s)""")
art_aliqot_query=("""insert into art_aliquot (ali_name,ali_date,prepared_by,extra_info,ref_artinfoid) values (%s,%s,%s,%s,%s)""")
aliqot2mix_query=("""insert into aliqot2mix (ref_aliqotid,ref_mixid) values (%s,%s)""")
mixture_query=("""insert into mixtureinfo (mix_date,Madeby,m_type,extra_info,mixplate_name,No_art_Info) values (%s,%s,%s,%s,%s,%s)""")
tplate_query=("""insert into plates (p_name,printingDate,prepared_by,extra_info,ref_mixinfoid) values (%s,%s,%s,%s,%s) """)

## checking entries
artname2id="""select a_name,art_id from art"""
artwellname2id="""select w_name,well_id from art_well"""

checkingARTid="""SELECT i.art_id,a.a_name,i.art_date from art a
                  inner join art_info i on i.ref_artid=a.art_id"""
checkingART_aliqotid= """SELECT ali_id,ali_name,ali_date from art_aliquot """
checkingMix="""SELECT mix_id,mix_date,mixplate_name,m_type from mixtureinfo """

def getAlldatafromDB(Query,four=False,two=False):
    name_date2id={}
    cursor3 = cnx.cursor()
    cursor3.execute(Query)
    if four:
        for (first,second,third,fourth) in cursor3:
            # print first,second,third,str(fourth)
            if third+"_"+fourth+"_"+str(second) not in name_date2id:
                name_date2id[third+"_"+str(second)+"_"+fourth]=first
    elif two:
        for (name,id)in cursor3:
            if name not in name_date2id:
                name_date2id[name]=id
    else:
        for (first,second,third) in cursor3:
            if second+"_"+str(third) not in name_date2id:
                name_date2id[second+"_"+str(third)]=first
    cursor3.close()
    return name_date2id

## get all the dic for all values in the database
art_name_date_2_id_dic=getAlldatafromDB(checkingARTid) #key=name_date
artAliqot_name_date_2_id_dic=getAlldatafromDB(checkingART_aliqotid) #key=(art*_ali*)_date
mix_name_date2id_dic=getAlldatafromDB(checkingMix,four=True) #key=name_date_type
artname2idDic=getAlldatafromDB(artname2id,two=True)
artwellname2idDic=getAlldatafromDB(artwellname2id,two=True)

def addArt(aName,aDate,aPrep,extra_info,artConcFileName,root):
    if aName.get()=="" or aDate.get()=="" or aPrep.get()=="" :
        IO_prob("Please fill all the required field with valid input...")
    elif aName.get()+"_"+aDate.get() in art_name_date_2_id_dic:
        IO_prob(" ART name with same date exist. Dublicate entries are not allowed....")
    else:
        cursor1 = cnx.cursor()
        # first add the data in the art main and in the art info
        if aName not in artname2idDic:
            cursor1.execute(art_input, (aName.get(),))
            ref_artid=cursor1.lastrowid
        else:
            ref_artid=artname2idDic[aName]
        cursor1.execute(art_info_query,(aDate.get(),aPrep.get(),extra_info.get()))
        ref_artinfoid=cursor1.lastrowid
        art_name_date_2_id_dic[aName.get()+"_"+aDate.get()]=ref_artid
        with open(artConcFileName.get()) as concFile:
            next(concFile)
            for line in concFile:
                splits=line.split("\t")
                wellName=splits[0].strip()
                conc=float(splits[6].strip())
                ratio=float(splits[5].strip())
                if wellName not in artwellname2idDic:
                    cursor1.execute(artwell_query,(wellName,))
                    ref_artwellid=cursor1.lastrowid
                else:
                    ref_artwellid=artwellname2idDic[wellName]
                cursor1.execute(artwellinfo_query,(conc,ratio))
                refartwellinfoid=cursor1.lastrowid
                #for each well add the relation with art
                cursor1.execute(art_well_relation,(ref_artwellid,ref_artid))
                #for each well info add the realtion with art info
                cursor1.execute(artwellinfo_query,(ref_artwellid,ref_artinfoid))
        print "added...."
        ttk.Label(root, text="finished adding your entry..").grid(column=3, row=8)
        cnx.commit()


def addArtaliqot(aliName,aliDate,aliPrep,artName,artDate,extra_info,root):
    cursor1 = cnx.cursor()
    if aliName.get()=="" or aliDate.get()=="" or aliPrep.get()=="" or artName=="" or artDate=="":
        IO_prob("Please fill all the required field with valid input...")
    elif aliName.get()+"_"+str(aliDate.get()) in artAliqot_name_date_2_id_dic:
        IO_prob(" ART name with same date exist. Dublicate entries are not allowed....")
    elif artName.get()+"_"+str(artDate.get()) not in art_name_date_2_id_dic:
        IO_prob(" ART name and date does not exist in the database, please check or insert ART entries  in the database ....")
    else:
        ref_artinfoid=art_name_date_2_id_dic[artName.get()+"_"+str(artDate.get())]
        cursor1.execute(art_aliqot_query,(artName.get()+"_"+aliName.get(),aliDate.get(),aliPrep.get(),extra_info.get(),ref_artinfoid))
        artAliqot_name_date_2_id_dic[artName.get()+"_"+aliName.get()+"_"+str(aliDate.get())]=cursor1.lastrowid
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
    elif tplate+"_"+mix_date+"_"+m_type in mix_name_date2id_dic:
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
        mix_name_date2id_dic[tplate+"_"+mix_date+"_"+m_type]=mix_id
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
            cursor1.execute(tplate_query,(platename,tdate.get(),prepBy.get(),extra_info.get(),ref_mix_id))
            print "added...."
            ttk.Label(root, text="finished adding your entry..").grid(column=3, row=9)
        cnx.commit()

    # print tplate_start.get(),tplate_end.get(),tdate.get(),prepBy.get(),extra_info.get(),MixT.get(),MixDate.get()

