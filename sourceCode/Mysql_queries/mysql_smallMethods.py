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

