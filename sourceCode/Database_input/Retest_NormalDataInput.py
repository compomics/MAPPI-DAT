__author__ = 'surya'

from Mysql_queries import MySqlConnection

def EnterIntensityAndAnalysisData(fileId,lineList,arrangement,preyId,cnx,retestPos_input,controlConcDic,
                                  normalDnaConc,retest_eachcell_input,retestPosCon_input,kiss):
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()

    cursor1 = cnx.cursor()
    type = lineList[len(lineList) - 1].strip()  # last column always
    wellName = lineList[len(lineList) - 2].strip()  # second last always
    tag = lineList[len(lineList) - 3].strip()  # third last
    arrangementList=arrangement.split(",")
    FC_baitNull=lineList[3+len(arrangementList)].strip()
    FC_PreyNull=lineList[3+len(arrangementList)+1].strip()
    ## add the analysis output
    if type in ["control","empty"]:
        cursor1.execute(retestPosCon_input, (FC_baitNull, FC_PreyNull, tag, type, preyId))
        retestposId = cursor1.lastrowid
    else:
        cursor1.execute(retestPos_input, (FC_baitNull,FC_PreyNull,tag,type,preyId))
        retestposId = cursor1.lastrowid
    for i in range(3, (len(arrangementList)+3)):
        intensity = lineList[i].strip()
        well_type = arrangementList[i - 3]
        if type == "control" or type == "empty":
            if wellName in controlConcDic:
                cursor1.execute(retest_eachcell_input,(wellName,well_type,fileId,controlConcDic[wellName], retestposId, intensity))
            else:
                print wellName, " not found in the database"

        elif type == "analysis":
            if wellName in normalDnaConc:
                cursor1.execute(retest_eachcell_input,
                                (wellName,well_type,fileId,normalDnaConc[wellName], retestposId, intensity))
            else:
                print wellName, " not found in the database"
    cursor1.close()
    cnx.commit()

