__author__ = 'surya'


import mysql.connector

def connectSql():
    allpara=[]
    c=0
    with open("Parameter.txt") as paraFile:
        next(paraFile)
        for line in paraFile:
            c+=1
            if c<5: ## only use parameter till the line number five
                splits=line.split("=")
                if splits[1].strip()!="":
                    allpara.append(splits[1].strip())
                else:
                    print "One of the parameter is missing !!"

    if len(allpara)==4:
        cnx = mysql.connector.connect(user=allpara[0], database=allpara[1], password=allpara[2],host=allpara[3])
    else:
        print "check parameters"
        print "Database not connected!!"
        cnx=""
    return cnx




def ReturnCnxForMySql(cnx):
    cursor1 = cnx.cursor()
    return cursor1


