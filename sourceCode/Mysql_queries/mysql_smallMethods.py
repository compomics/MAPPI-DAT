__author__ = 'surya'

def CheckPresenese_Insert(query,value,checkname,dic,cnx,onlyInsert=False): ## only insert means it will not check the presence
    present=False
    cursor1=cnx.cursor()
    if onlyInsert:
        cursor1.execute(query,value)
        checkid= cursor1.lastrowid
        dic[checkname]=checkid
    else:
        if checkname not in dic:
            cursor1.execute(query,value)
            checkid= cursor1.lastrowid
            dic[checkname]=checkid
        else:
            present=True
            checkid=dic[checkname]
    return present,checkid,dic

def checkPresenceAndAddMoreInfoInTable(query1,query2,value1,value2,checkname,dic,cnx):
    cursor1 = cnx.cursor()
    if checkname not in dic:
        cursor1.execute(query1,value1)
        checkid= cursor1.lastrowid
        dic[checkname]=checkid
    else:
        cursor1.execute(query2,value2)
        checkid= cursor1.lastrowid
        dic[checkname]=checkid
    return checkid,dic
