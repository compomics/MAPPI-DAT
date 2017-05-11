__author__ = 'surya'


from Mysql_queries import Project_Query,MySqlConnection,GetExistingDataFromDatabase,mysql_smallMethods
import os
from Error_handle import ErrorHandling
import Retest_treatmentDataInput,Retest_NormalDataInput

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




def reTestInput(project,expgrp,experiments,cnx,reason,ReTestOutputList,DnaControlConcFile,DnaConcFile,arrnagement,
                retestName,submissionDate,retest_date,doneby,treatment,threshold,kissExperiment):
    experimentsList=experiments.split(",")
    arrnagementList=arrnagement.split(",")

## get all the query statement
    Allexperiments = ("""select e.experiment_id,e.e_name from experiments e
                          inner join experiment_group g on g.expgrp_id=e.ref_expgrpid
                          inner join project p on p.project_id=g.ref_projid
                          where p.p_name=%s and g.e_name=%s""")
    AllpreyId=(""" select p.prey_id,p.p_name from prey p""")
    AllcontrolsId=(""" select p.control_id,p.uniq_name from retest_controls p""")
    # prey_input=("""insert into prey (p_name,entrenz_name) values (%s,%s)""")

    exprelation_input=(""" insert into experiments_has_retest (ref_expid,ref_retestid) values (%s,%s) """)
    retest_input = ("""insert into retest (reason,r_name,submission_date,retest_date,done_by,treatment,threshold,kiss)
                            values (%s,%s,%s,%s,%s,%s,%s,%s)""")
    retest_files_input=(""" insert into retest_files (file_name,ref_retest,file_type) values (%s,%s,%s) """)
    retest_eachcell_input=(""" insert into retest_eachcell_intensity (wellName,well_type,ref_fileid,ref_condid,
                            ref_retest_analyid,intensity) values (%s,%s,%s,%s,%s,%s)""")
    retest_conditions_input=(""" insert into retest_conditions (dna_conc,dnaOD_260_280ratio,well_name) values (%s,%s,%s) """)
    retestPos_input=("""insert into retest_analysis_output (FC_baitNull,FC_preyNull,tag,type,ref_preyid) values (%s,%s,%s,%s,%s) """)
    retestPosCon_input=("""insert into retest_analysis_output (FC_baitNull,FC_preyNull,tag,type,ref_conid) values (%s,%s,%s,%s,%s) """)
    retestPosTreatment_input=("""insert into retest_analysis_output (FC_baitNull,FC_preyNull,tag,type,ref_preyid,
                              FC_baitNullT,FC_preyNullT,tagT)
                                values (%s,%s,%s,%s,%s,%s,%s,%s) """)
    retestPosTreatmentControl_input=("""insert into retest_analysis_output (FC_baitNull,FC_preyNull,tag,type,ref_conid,
                              FC_baitNullT,FC_preyNullT,tagT)
                                values (%s,%s,%s,%s,%s,%s,%s,%s) """)
    ## analysis output with method inside
    retest_pos_withmethod_input=("""insert into retest_analysis_output (FC_baitNull,FC_preyNull,tag,type,ref_preyid,ref_methodid)
                                values (%s,%s,%s,%s,%s,%s) """)
    method_input=(""" insert into retest_method (method_name) values (%s)""")
    retestcontrol_input=(""" insert into retest_controls (uniq_name,full_name) values (%s,%s)""")

# check if the connection available

    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()
    print("starting database.......... ")

    cursor1 = cnx.cursor()

## get all prey name and id
    preyIdNameDic=GetExistingDataFromDatabase.getAlldata_fromDatabase(AllpreyId,cnx)
    ControlName2IdDic=GetExistingDataFromDatabase.getAlldata_fromDatabase(AllcontrolsId,cnx)


    ## to get the id for the experiments for the project,expgrp
    expName2IdDic=GetExistingDataFromDatabase.getAlldata_fromDatabase(Allexperiments,cnx,query_val=(project,expgrp))

    #check if the name of the exp given are in the database, else end
    expPresent=list(set(experimentsList).intersection(expName2IdDic.keys()))
    if len(expPresent)==len(experimentsList):
        print "started adding data in the database"

        # ## insert retest parameters
        cursor1.execute(retest_input,(reason,retestName,submissionDate,retest_date,doneby,treatment,threshold,kissExperiment))
        retest_id= cursor1.lastrowid

    ## add the experiments and retest relations
        for eachexp in experimentsList:
            cursor1.execute(exprelation_input,(expName2IdDic[eachexp],retest_id))

    ## parse concentration file for control as well for normal data and add the data in the database
        controlConcWellName2IdDic=parseconcFile_enterindb(DnaControlConcFile,cnx,retest_conditions_input)
        DnaConcWellName2IdDic=parseconcFile_enterindb(DnaConcFile,cnx,retest_conditions_input)

    ## parse output file and add the data in reteste_positives
        fileDic={} # there is nothing in the file
        j=0
        for line in ReTestOutputList:
            splits=line.split("\t")
            filename=splits[0].strip()
            uniqueId=splits[1].strip()
            entrezid=splits[2].strip()
            type = splits[- 1].strip()
            if type not in ["empty","control"]:
                if uniqueId not in preyIdNameDic:
                    ErrorHandling.IO_prob(
                        "Protein " + uniqueId + " not present in the database, cannot add data in database")
                    break
                else:
                    preyId=preyIdNameDic[uniqueId]
            else:
                # check and only insert else just get id
                control_present,preyId,ControlName2IdDic=mysql_smallMethods.CheckPresenese_Insert(retestcontrol_input,
                                                            (uniqueId,entrezid),uniqueId,ControlName2IdDic,cnx)
            if treatment:
                ## enter the file in the database
                fileList=filename.split("_")
                if fileList[0]!=fileList[1]:
                    ## for without bait file
                    filePresent, fileid, fileDic = mysql_smallMethods.CheckPresenese_Insert(retest_files_input,
                                                            (fileList[0], retest_id,"WithoutBait"),fileList[0], fileDic, cnx)
                    # for with bait file
                    filePresent, fileid, fileDic = mysql_smallMethods.CheckPresenese_Insert(retest_files_input,
                                                            (fileList[1], retest_id,"WithBait"),fileList[1], fileDic, cnx)

                else:
                    # for with bait file
                    filePresent, fileid, fileDic = mysql_smallMethods.CheckPresenese_Insert(retest_files_input,
                                                            (fileList[1], retest_id,"WithWOTBoth"),fileList[1], fileDic, cnx)

                Retest_treatmentDataInput.EnterIntensityAndAnalysisDataTreatment(fileDic,splits,preyId,cnx,
                        retestPosTreatment_input,controlConcWellName2IdDic,DnaConcWellName2IdDic,retest_eachcell_input,
                                                                                 retestPosTreatmentControl_input)

            else:
                filePresent, fileid, fileDic = mysql_smallMethods.CheckPresenese_Insert(retest_files_input,
                                                                        (filename, retest_id,"Both"),
                                                                        filename, fileDic, cnx)
                Retest_NormalDataInput.EnterIntensityAndAnalysisData(fileid,splits,arrnagement,preyId,cnx,retestPos_input,
                                                    controlConcWellName2IdDic,DnaConcWellName2IdDic,retest_eachcell_input,
                                                                     retestPosCon_input,kissExperiment)
        print "Done !!!!"
    else:
        ErrorHandling.IO_prob("All experiments "+experiments+" entered are not present in the database, cannot add data in database")

    cursor1.close()
    cnx.commit()
    if cnx.is_connected:
        cnx.close()

