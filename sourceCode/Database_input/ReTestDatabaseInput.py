__author__ = 'surya'


from Mysql_queries import Project_Query,MySqlConnection,GetExistingDataFromDatabase,mysql_smallMethods
import os

def parseconcFile_enterindb(DnaControlFile,cnx,query):
    cursor1=cnx.cursor()
    control_wellNameIdDic={}
    with open(DnaControlFile) as dnacontrol:
        next(dnacontrol)
        for eachConControl in dnacontrol:
            Csplits=eachConControl.split("\t")
            cursor1.execute(query, (Csplits[4].strip(),Csplits[3].strip(),Csplits[0].strip()))
            wellid=cursor1.lastrowid
            control_wellNameIdDic[Csplits[0].strip()]=wellid
    return control_wellNameIdDic



def reTestInput(project,expgrp,experiments,cnx,reason,ReTestOutputFile,DnaControlFile,DnaConcFile,arrnagement,retestName,submissionDate,retest_date,doneby):
    experimentsList=experiments.split(",")
    arrnagementList=arrnagement.split(",")

## get all the query statement
    Allexperiments = ("""select e.experiment_id,e.e_name from experiments e
                          inner join experiment_group g on g.expgrp_id=e.ref_expgrpid
                          inner join project p on p.project_id=g.ref_projid
                          where p.p_name=%s and g.e_name=%s""")
    AllpreyId=(""" select p.prey_id,p.p_name from prey p""")
    prey_input=("""insert into prey (p_name,entrenz_name) values (%s,%s)""")

    exprelation_input=(""" insert into experiments_has_retest (ref_expid,ref_retestid) values (%s,%s) """)
    retest_input = ("""insert into retest (reason,r_name,submission_date,retest_date,done_by) values (%s,%s,%s,%s,%s)""")
    retest_files_input=(""" insert into retest_files (file_name,ref_retest) values (%s,%s) """)
    retest_eachcell_input=(""" insert into retest_eachcell_intensity (row,col,well_type,ref_fileid,ref_condid,ref_retest_analyid,intensity) values (%s,%s,%s,%s,%s,%s,%s)""")
    retest_conditions_input=(""" insert into retest_conditions (dna_conc,dnaOD_260_280ratio,well_name) values (%s,%s,%s) """)
    retestPos_input=("""insert into retest_analysis_output (FI_baitNull,FI_preyNull,tag,type,ref_preyid) values (%s,%s,%s,%s,%s) """)
    ## analysis output with method inside
    retest_pos_withmethod_input=("""insert into retest_analysis_output (FI_baitNull,FI_preyNull,tag,type,ref_preyid,ref_methodid) values (%s,%s,%s,%s,%s,%s) """)
    method_input=(""" insert into retest_method (method_name) values (%s)""")

# check if the connection available

    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()
    print("starting database.......... ")

    cursor1 = cnx.cursor()

    ## row and column
    alp_num={"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
    # colList=range(1,13)


## get all prey name and id
    preyIdNameDic=GetExistingDataFromDatabase.getAlldata_fromDatabase(AllpreyId,cnx)


    ## to get the id for the experiments for the project,expgrp
    expIdNameDic=GetExistingDataFromDatabase.getAlldata_fromDatabase(Allexperiments,cnx,query_val=(project,expgrp))
#
# ## insert retest parameters

    cursor1.execute(retest_input,(reason,retestName,submissionDate,retest_date,doneby))
    retest_id= cursor1.lastrowid

## add the experiments and retest relations
    for eachexp in expIdNameDic:
        cursor1.execute(exprelation_input,(expIdNameDic[eachexp],retest_id))

## parse concentration file for control as well for normal data

    controlConcDic=parseconcFile_enterindb(DnaControlFile,cnx,retest_conditions_input)
    normalDnaConc=parseconcFile_enterindb(DnaConcFile,cnx,retest_conditions_input)

## parse output file and add the dta in reteste_positives
    retestDatawellId={}
    retestControlDatawellId={}
    fileDic={}
    j=0
    with open(ReTestOutputFile) as retestFile:
        next(retestFile)
        for line in retestFile:
            splits=line.split("\t")
            filename=splits[0].strip()
            FIbaitNull=splits[len(splits)-7].strip()
            FIpreyNull=splits[len(splits)-8].strip()
            uniqueId=splits[1].strip()
            entrezid=splits[2].strip()
            type=splits[len(splits)-1].strip()
            wellname=splits[len(splits)-2].strip()
            tag=splits[len(splits)-3].strip()
            prey_present,preyId,preyIdNameDic=mysql_smallMethods.CheckPresenese_Insert(prey_input,(uniqueId,entrezid),uniqueId,preyIdNameDic,cnx)
            ## add the analysis output
            cursor1.execute(retestPos_input,(FIbaitNull,FIpreyNull,tag,type,preyId))
            retestposId=cursor1.lastrowid
            ## enter the file in the database
            filePresent,fileid,fileDic=mysql_smallMethods.CheckPresenese_Insert(retest_files_input,(filename,retest_id),filename,fileDic,cnx)
            for i in range(3,(len(splits)-10)):
                intensity=splits[i].strip()
                well_type=arrnagementList[i-3]
                row=alp_num[wellname]
                col=i-2
                wellnaemNum=wellname+str((i-2))
                if type=="control" or type=="empty":
                    if wellnaemNum in controlConcDic:
                        cursor1.execute(retest_eachcell_input,(row,col,well_type,fileid,controlConcDic[wellnaemNum],retestposId,intensity))
                    else:
                        print wellnaemNum," not found in the database"

                elif type=="normal":
                    if wellnaemNum in normalDnaConc:
                        cursor1.execute(retest_eachcell_input,(row,col,well_type,fileid,normalDnaConc[wellnaemNum],retestposId,intensity))
                    else:
                        print wellnaemNum," not found in the database"

    cursor1.close()
    cnx.commit()
    print "Done !!!!"

