__author__ = 'surya'

from Mysql_queries import MySqlConnection


def getAlldata_fromDatabase(Query,cnx,query_val='Null',append=False):
    if not cnx.is_connected():
        cnx = MySqlConnection.connectSql()
    dic={}
    cursor3 = cnx.cursor()
    if query_val!="Null":
        cursor3.execute(Query,query_val)
    else:
        cursor3.execute(Query)
    for (id,name) in cursor3:
        if name not in dic:
            if append:
                dic[name]=[id]
            else:
                dic[name]=id
        else:
            if append:
                dic[name].append(id)
    cursor3.close()
    return dic



def get2colmergedata_fromDatabase(Query,cnx,query_val='Null',append=False):
    if not cnx.is_connected():
        cnx = MySqlConnection.connectSql()

    dic={}
    cursor3 = cnx.cursor()
    if query_val!="Null":
        cursor3.execute(Query,query_val)
    else:
        cursor3.execute(Query)
    for (id,name,other) in cursor3:
        if name not in dic:
            if append:
                dic[name+"_"+other]=[id]
            else:
                dic[name+"_"+other]=id
        else:
            if append:
                dic[name+"_"+other].append(id)
    cursor3.close()
    return dic

def getdatafromDB(Query,cnx,four=False,two=False):
    if not cnx.is_connected():
        cnx = MySqlConnection.connectSql()

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