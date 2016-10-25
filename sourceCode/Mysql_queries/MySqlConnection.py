__author__ = 'surya'


import mysql.connector

def connectSql():
    allpara=[""]*4
    c=0
    for line in open("Parameter.txt"):
        if line!="\n":
            splits=line.split("=")
            if splits[0].strip()=="user":
                allpara[0]=splits[1].strip()
                c += 1
            elif splits[0].strip()=="database":
                allpara[1] = splits[1].strip()
                c += 1
            elif splits[0].strip()=="password":
                allpara[2] = splits[1].strip()
                c += 1
            elif splits[0].strip()=="host":
                allpara[3] = splits[1].strip()
                c += 1
    # print allpara
    if c==4:
        cnx = mysql.connector.connect(user=allpara[0], database=allpara[1], password=allpara[2],host=allpara[3])
    else:
        print "check parameters"
        print "Database not connected!!"
        cnx=""
    return cnx


def ReturnCnxForMySql(cnx):
    cursor1 = cnx.cursor()
    return cursor1


