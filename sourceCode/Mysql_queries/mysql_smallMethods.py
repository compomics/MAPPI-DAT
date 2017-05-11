__author__ = 'surya'

from Mysql_queries import MySqlConnection

def OnlyInsert(query,value,cnx,commit=False):
    if not cnx.is_connected():
        cnx = MySqlConnection.connectSql()
    cursor1=cnx.cursor()
    cursor1.execute(query, value)
    checkid = cursor1.lastrowid
    if commit:
        cnx.commit()
    cursor1.close()
    return checkid

def UpdateTable(query,value,cnx):
    if not cnx.is_connected():
        cnx = MySqlConnection.connectSql()
    cursor1=cnx.cursor()
    cursor1.execute(query, value)
    cnx.commit()
    cursor1.close()


def CheckPresenese_Insert(query,value,checkname,dic,cnx,onlyInsert=False): ## only insert means it will not check the presence
    present=False
    cursor1=cnx.cursor()
    if onlyInsert:
        cursor1.execute(query,value)
        checkid= cursor1.lastrowid
        dic[checkname]=checkid
    else:
        if checkname not in dic:
            # print "adding the file..",checkname
            cursor1.execute(query,value)
            checkid= cursor1.lastrowid
            dic[checkname]=checkid
        else:
            present=True
            checkid=dic[checkname]
    cnx.commit()
    cursor1.close()
    return present,checkid,dic

def checkPresenceAndAddMoreInfoInTable(query1,query2,value1,value2,checkname,dic,cnx):
    if not cnx.is_connected():
        cnx = MySqlConnection.connectSql()
    cursor1 = cnx.cursor()
    if checkname not in dic:
        cursor1.execute(query1,value1)
        checkid= cursor1.lastrowid
        dic[checkname]=checkid
    else:
        cursor1.execute(query2,value2)
        checkid= cursor1.lastrowid
        dic[checkname]=checkid
    cursor1.close()
    return checkid,dic
