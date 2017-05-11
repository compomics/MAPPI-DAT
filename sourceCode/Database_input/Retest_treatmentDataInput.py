__author__ = 'surya'

from Mysql_queries import MySqlConnection


def checkAndInsertEachCellIntensity(wellName,well_type,controlConcDic,normalDnaConc,cnx,
                                    retest_eachcell_input,fileId,retestposId,intensity,type):
    cursor1 = cnx.cursor()
    if type == "control" or type == "empty":
        if wellName in controlConcDic:
            cursor1.execute(retest_eachcell_input,
                            (wellName, well_type, fileId, controlConcDic[wellName], retestposId,
                             intensity))
        else:
            print wellName, " not found in control the database"

    elif type == "analysis":
        if wellName in normalDnaConc:
            cursor1.execute(retest_eachcell_input,
                            (wellName, well_type, fileId, normalDnaConc[wellName], retestposId,
                             intensity))
        else:
            print wellName, " not found in normal the database"
    cursor1.close()


def EnterIntensityAndAnalysisDataTreatment(fileIdDic, lineList,preyId, cnx, retestPosT_input, controlConcDic,
                                  normalDnaConc, retest_eachcell_input,retestPosConT_input):
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()

    arrangementList="NS\tNS\tNS\tS\tS\tS\tST\tST\tST\tNSB+\tNSB+\tNSB+\tSB+\tSB+\tSB+\tSB+T\tSB+T\tSB+T".split("\t")
    cursor1 = cnx.cursor()
    fileNameList=lineList[0].strip().split("_")
    type = lineList[-1].strip()  # last column always
    wellName = lineList[-2].strip()  # second last always
    tagT = lineList[-3].strip()  # third last
    tag = lineList[-4].strip()  # fourth last
    FI_baitNull = lineList[3 + len(arrangementList)].strip()
    FI_baitNullT = lineList[4 + len(arrangementList)].strip()
    FI_PreyNull = lineList[5 + len(arrangementList)].strip()
    FI_PreyNullT = lineList[6 + len(arrangementList)].strip()
    ## add the analysis output
    if type in ["control","empty"]:
        cursor1.execute(retestPosConT_input, (FI_baitNull, FI_PreyNull, tag, type, preyId,
                                           FI_baitNullT, FI_PreyNullT, tagT))
        retestposId = cursor1.lastrowid
    else:
        cursor1.execute(retestPosT_input, (FI_baitNull,FI_PreyNull,tag,type,preyId,
                                  FI_baitNullT,FI_PreyNullT,tagT))
        retestposId = cursor1.lastrowid
    cursor1.close()
    ## first check if both files are same or not
    if fileNameList[0]==fileNameList[1]:
        for i in range(3, len(arrangementList)+ 3):
            intensity = lineList[i].strip()
            well_type = arrangementList[i - 3]
            checkAndInsertEachCellIntensity(wellName,well_type,controlConcDic,normalDnaConc,cnx,retest_eachcell_input,
                                            fileIdDic[fileNameList[0]],retestposId,intensity,type)
    else:
    ## first enter the data and relate it to the without bait file
        End1=(len(arrangementList)/2)+3
        for i in range(3,  End1):
            intensity = lineList[i].strip()
            well_type = arrangementList[i - 3]
            checkAndInsertEachCellIntensity(wellName, well_type, controlConcDic, normalDnaConc, cnx,
                                            retest_eachcell_input,
                                            fileIdDic[fileNameList[0]], retestposId, intensity,type)
        ## then enter the data and relate it to the with bait file
        for i in range(End1,len(arrangementList)+ 3):
            intensity = lineList[i].strip()
            well_type = arrangementList[i - 3]
            checkAndInsertEachCellIntensity(wellName, well_type, controlConcDic, normalDnaConc, cnx,
                                            retest_eachcell_input,
                                            fileIdDic[fileNameList[1]], retestposId, intensity,type)
    cnx.commit()

