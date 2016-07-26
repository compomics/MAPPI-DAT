__author__ = 'surya'


def getAlldata_fromDatabase(Query,cnx,query_val='Null',append=False):
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