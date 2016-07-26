__author__ = 'surya'
#from Error_handle import ErrorHandling
import os

from Mysql_queries import MySqlConnection,GetExistingDataFromDatabase, mysql_smallMethods


def input_mysql(Tplate2Path,plate2subfolder,ns, s,p_name, preason, eg_name, bait_name, e_name,e_date,expReason,Scanningdate,mbubait_code,
                BaitvectorType,stimuluType, stimulusconc, protocolType,treatmentType,TreatmentConc,Treatementdate,treatment_starttime,
                treatment_endtime,aspeficDic,cnx,mappit,maspit,kiss,treatment,fusion_cpd,fusion_cps_conc,
                moleculeExtraInfo,linkageDic,plate_tfileDic,BaitTransfectDate,path):
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()


    print("starting database.......... ")
    """
    Pannotation= protein files in a dictionary where the name with .txt as key and values is the path (T1.txt=c://users/surya/desktop/project/t1.txt)
    platefile: dic which contain name of plate as key and value as the path of the plate
    ns: list of the well names which are NS
    s: list of the well names which are Stimulating

    p_name= project name
    preason= description about the project
    eg_name= experimnet group name
    bait_name= name of the bait used in the experiment
    e_name=experiment name
    e_date = experiment date
    expReason=aim or description of the experiment
    transfect_date=
    mbubait_code=
    BaitvectorType=
    stimulus type= epo or leptin
    stimulus conc= concentration of the stimulus used
    protocoloType= type of the protocol used in the experiment
    treatment type=
    treatment conc=
    treatment time=
    aspecificdic=
    platinfodic=
    cnx=

    """

    ## loggin in into the mymysql sever
    cursor1 = cnx.cursor()
    cursor2 = cnx.cursor()
    cursor3 = cnx.cursor()
    cursor4 = cnx.cursor()
    cursor5 = cnx.cursor()
    cursor6 = cnx.cursor()
    cursor7 = cnx.cursor()
    cursor8 = cnx.cursor()
    proj_present = False
    expgrp_present = False

    nslist = ns.split(",")
    nsreplicate = len(nslist)
    slist = s.split(",")
    sreplicate = len(slist)

    artwell_input = ("""insert into art_well (w_name,ref_artid) values (%s,%s)""")

    art_input = ("""insert into art (a_name) values (%s)""")

    artrelation_input = ("""insert into art_relation (ref_mixtureid,ref_artid) values (%s,%s)""")

    mixture_input = ("""insert into mixture (m_name,ref_panid) values (%s,%s)""")
    # mixtureInfo_input = ("""insert into mixtureinfo (mix_date,Madeby,m_type,extra_info,mixplate_name) values (%s,%s,%s,%s,%s) """)

    preannotaiont_input = ("""insert into preyannotationt (p_name) values (%s)""")

    tplaterelation_input = ("""insert into tplaterelation (ref_panid,ref_experimentid) values (%s,%s)""")

    project_input = ("""insert into project (p_name,description) values (%s,%s)""")

    experimentGrp_input = ("""insert into experiment_group (e_name,ref_projid) values (%s,%s)""")

    #        prey_input= ("""insert into prey (sequence,homology,weight,p_name,ref_panid,entrenz_name) values (%s,%s,%s,%s,%s,%s)""")
    prey_input = ("""insert into prey (p_name,ref_panid,entrenz_name) values (%s,%s,%s)""")

    bait_input = (
        """insert into bait (b_name) values (%s)""")

    molecule_input = (
        """insert into molecule (fusion_cpd_type,fusion_cpd_conc,extra_info) values (%s,%s,%s)""")

    interactors_inp = ("""insert into interactors (ref_expgrpid,ref_preyid,inttype) values (%s,%s,%s)""")

    expcondition = (
        """insert into exp_condition (stimulus_type,stimulus_conc,Scanning_date,mbu_bait_code,NSreplicate,Sreplicate,
            bait_vector_type,protocol_version,treatment_type,treatment_con,treatment_date,start_treatment,end_treatment,input_date,BaitTransfectDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
    expcondition_wottreatment = (
        """insert into exp_condition (stimulus_type,stimulus_conc,Scanning_date,mbu_bait_code,NSreplicate,Sreplicate,
            bait_vector_type,protocol_version,input_date,BaitTransfectDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")


    experiments_input = (
        """insert into experiments (e_name,description, e_quality,ref_expgrpid,ref_conditionid,experiment_type) values (%s,%s,%s,%s,%s,%s)""")

    wells_input = ("""insert into well (w_name,stimulus_type,ref_platid) values (%s,%s,%s)""")

    spots_input = ("""insert into spots (row,col,block,ref_wellid,ref_interactorid) values (%s,%s,%s,%s,%s)""")

    quantificationVal_input = (
        """insert into quantificationval (pc,meanarea,grayvalmean,meangrayvalmean,meanintint,area_fraction,intint,ref_spotid) values (%s,%s,%s,%s,%s,%s,%s,%s)""")

    Aspecific_input=("""insert into aspecifics (ref_preyid,ref_experimentid) values (%s,%s)""")


#####################################################################################################################
######################## get all the data from database ############################################################

    projectDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT project_id,p_name FROM project""",cnx)
    expgrpDic={}
    preAnnotationDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT pan_id,p_name from preyannotationt""",cnx)
    mixtureDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT mixture_id,m_name from mixture""",cnx)
    artDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT art_id,a_name from art""",cnx)
    artWellDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT well_id,w_name from art_well """,cnx)
    preyDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT prey_id,p_name FROM prey""",cnx)
    platDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT plate_id,p_name From plates """, cnx)
    # platDic={}
    plat_wellDic={} ## {plat:{well:wellid}}
    # quartileIdList=[] ##
    tplat_expDic={}

#####################################################################################################################

    ## get the name of the experiment used in the analysis
    exp_type=""
    if mappit:
        exp_type="mappit"
    elif maspit:
        exp_type="maspit"
    elif kiss:
        exp_type="kiss"



    ## check if project already present
    proj_present,project,projectDic= mysql_smallMethods.CheckPresenese_Insert(project_input,(p_name,preason),p_name,projectDic,cnx)

    insertValOnly=False

    if proj_present:
        expgrpDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT expgrp_id,e_name FROM experiment_group
                                                                inner join project p on p.project_id=ref_projid
                                                                where p.p_name=%s""",cnx,query_val=(p_name,)) ## check the exp group for the particular project
    else:
        insertValOnly=True
    expgrp_present,expgrp,expgrpDic= mysql_smallMethods.CheckPresenese_Insert(experimentGrp_input,(eg_name, project),eg_name,expgrpDic,cnx,insertValOnly)



 ## insert the entries for the experiment condition
    ## check if the treatment is asked

    if treatment:
        cursor7.execute(expcondition, (stimuluType,stimulusconc,Scanningdate,mbubait_code, nsreplicate,sreplicate,BaitvectorType,protocolType,treatmentType,TreatmentConc,
                                       Treatementdate,treatment_starttime,treatment_endtime,e_date,BaitTransfectDate))
        econ = cursor7.lastrowid
    else:
        cursor7.execute(expcondition_wottreatment, (stimuluType,stimulusconc,Scanningdate,mbubait_code, nsreplicate,sreplicate,BaitvectorType,protocolType,e_date,BaitTransfectDate))
        econ = cursor7.lastrowid


    ## insert the new experiment taking the foreign key value from group and condition
    cursor8.execute(experiments_input, (e_name, expReason, 0, expgrp, econ, exp_type))
    exp = cursor8.lastrowid
    cnx.commit()

    ## Now check if the project and experiment group already exist than do not insert the prey again....
    if not (proj_present and expgrp_present):
        ## also insert the new bait entry for the project
        ## open file for bait
        cursor2.execute(bait_input, (bait_name,))
        baitid = cursor2.lastrowid
                ## open file for the molecule
        if maspit:
            cursor3.execute(molecule_input, (fusion_cpd,fusion_cps_conc,moleculeExtraInfo))
            molid = cursor3.lastrowid
            ## update the foreign key linking to bait and molecule
            cursor3.execute(""" UPDATE experiment_group set ref_baitid= %s , ref_molid=%s where expgrp_id=%s""",
                            (baitid, molid, expgrp))
        else:
            cursor3.execute(""" UPDATE experiment_group set ref_baitid= %s where expgrp_id=%s""", (baitid, expgrp))
        cnx.commit()
        ### adding the prey entry
        print "started with adding protein information...."
#        mixture_dic={}
        print "total proteins Aspecific found are ",len(aspeficDic)
        for entry in Tplate2Path: ## this is the dic {Tfilename=path of t file}
            TPsplit = entry.split(".")
            print "doing file: ", entry
            with open(Tplate2Path[entry]) as pfile:
                next(pfile)
                for line in pfile:
                    psplits = line.split("\t")
                    ## check if the plate is already present
                    t_present,tplate,preAnnotationDic= mysql_smallMethods.CheckPresenese_Insert(preannotaiont_input,(TPsplit[0],),TPsplit[0],preAnnotationDic,cnx) ## this adds the protein annotation file name like t1.... T12

                    ## add mixtures ## this uses the mixture information from each of the protein in protein file dic[M1]=mix_id
                    mixPresent,mixture,mixtureDic= mysql_smallMethods.CheckPresenese_Insert(mixture_input, (psplits[18].strip(), tplate),psplits[18].strip(),mixtureDic,cnx)

                    ## add art names
                    artpresent,art,artDic= mysql_smallMethods.CheckPresenese_Insert(art_input, ("ART" + psplits[0].strip(),),"ART" + psplits[0].strip(),artDic,cnx)

                    ## add the art well names
                    artwellpresent,artwell,artWellDic= mysql_smallMethods.CheckPresenese_Insert(artwell_input, (psplits[1].strip(), art),psplits[1].strip(),artWellDic,cnx)

                    ## add the relations
                    cursor5.execute(artrelation_input, (mixture, art))
                    ## add the realtion between the tplate and exp only if it does not exist
                    if tplate not in tplat_expDic:
                        cursor5.execute(tplaterelation_input, (tplate, exp))
                        tplat_expDic[tplate]=exp

                    ## add the prey name
                    prpresent,protein,preyDic= mysql_smallMethods.CheckPresenese_Insert(prey_input, (psplits[10].strip(), tplate, psplits[12].strip()),psplits[10].strip(),preyDic,cnx)

                    ## add interactors entry
                    if psplits[10].strip() in aspeficDic:
                        type="A-specific"
                    else:
                        type=psplits[15].strip()
                    cursor5.execute(interactors_inp, (expgrp, protein,type))
        cnx.commit()

    print "started adding A-specifics"

    # aspecDic={}
    for apec in aspeficDic:
        if apec in preyDic:
            cursor4.execute(Aspecific_input,(preyDic[apec],exp))

    welldic = {'W1': 1, 'W2': 2, 'W3': 3, 'W4': 4}
    print "started processing each plate..", len(plate2subfolder)

    ### get all the interactor id for all the prey for this exp,egroup, project
    cursor3.execute("""select i.idinteractors,p.p_name from interactors i
        inner join prey p on p.prey_id=i.ref_preyid
        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
        inner join project j on j.project_id=g.ref_projid
        inner join experiments e on g.expgrp_id=e.ref_expgrpid
        where g.expgrp_id=%s and e.experiment_id=%s and j.project_id=%s""",  (expgrp, exp, project))
    prey_interactorDic={}
    for (interactorid,preyname) in cursor3:
        prey_interactorDic[preyname]=interactorid
    print len(prey_interactorDic)
    cnx.commit()
    #############################################################################################


    plate2well2lineDic={}
## add data in plate and than well
    for pl in plate2subfolder: ## for each plate in the platfile (subfolders)
    ## parse the all raw data file
        if len(plate2well2lineDic)==0:
            plate2well2lineDic = parseRawDataFile(path+"/"+linkageDic[plate2subfolder[pl]][0]+"/Processing/AllPlatesWithControl.txt") ## input: path+baitNam+plate; process the all processed file
        tplatName=os.path.basename(linkageDic[plate2subfolder[pl]][1]).split(".")[0] ## name of t plate without .txt
        # plates_involved=linkageDic[plate2subfolder[pl]][2] ## it is a list of plates that are used in the experiment for one type of analysis
        if tplatName in preAnnotationDic:
            tplatNameid=preAnnotationDic[tplatName] # ref_panid
        if pl not in platDic:
            print "plate is not present in the database..."
        else:
            cursor2.execute(""" UPDATE plates set ref_panid= %s , ref_expid=%s where p_name=%s""", (tplatNameid,exp,pl))
        print pl, " updated in the database...."
        plat_wellDic[pl]={}
        for ns_w in nslist: ## add the well for on stimulated
            cursor1.execute(wells_input, (ns_w, "Non-Stimulating",platDic[pl]))
            plat_wellDic[pl][ns_w]=cursor1.lastrowid
        for s_w in slist: ## add the well for stimulated
            cursor1.execute(wells_input, (s_w, "Stimulating",platDic[pl]))
            plat_wellDic[pl][s_w]=cursor1.lastrowid

       ## now start adding the spots, quantification val
        for w in plate2well2lineDic[pl]:
            for eachLine in plate2well2lineDic[pl][w]:
                splits = eachLine.split("\t")
                spl = splits[0].split("_")
                uniquename=splits[2].strip()
                platename=splits[5].strip()

                if uniquename in prey_interactorDic:
                    interid=prey_interactorDic[splits[2].strip()]
                    cursor2.execute(spots_input, (spl[5].strip(), spl[6].strip(), spl[welldic[w]].strip(), plat_wellDic[platename][w], interid))
                    spots = cursor2.lastrowid
                    cursor4.execute(quantificationVal_input,
                                    (float(splits[11].strip()), float(splits[12].strip()), float(splits[13].strip()),
                                     float(splits[14].strip()), float(splits[15].strip()), float(splits[16].strip()),
                                     float(splits[17].strip()), spots))

    """" add new tables in the database: well,quartile threshold, analysis paramater"""
                ## insert the plates corresponding for each of the subfolder

    cursor1.close()
    cursor2.close()
    cursor3.close()
    cursor4.close()
    cursor5.close()
    cursor6.close()
    cursor7.close()
    cursor8.close()
    cnx.commit()
    return exp, expgrp, project,platDic

############################################################################################################

def processfile(file):
    dic = {}
    for line in open(file):
        splits = line.split("\t")
        if splits[6].strip() in dic:
            dic[splits[6].strip()].append(line)
        else:
            dic[splits[6].strip()] = [line]
    return dic

########################################################################################################
def parseRawDataFile(fileName):
    plate2well2line={}
    with open(fileName) as openFile:
        next(openFile)
        for line in openFile:
            splits=line.split("\t")
            well=splits[6].strip()
            plate=splits[5].strip()
            if plate not in plate2well2line:
                plate2well2line[plate]={well:[line.strip()]}
            else:
                if well not in plate2well2line[plate]:
                    plate2well2line[plate][well]=[line.strip()]
                else:
                    plate2well2line[plate][well].append(line.strip())
    return plate2well2line
#########################################################################################################

def parseAnalysisFile(file1):
    import os
    print "parsing analysis file"
    dic = {}
    if os.stat(file1).st_size != 0:
        with open(file1) as afile:
            next(afile)
            for line in afile:
                if line != "\n":
                    splits = line.split("\t")
#                    plate= splits[0].split(",")[0]
                    plate= splits[0].strip()
#                    print plate
                    if plate.strip() not in dic:
                        dic[plate.strip()] = [line.strip()]
                    else:
                        dic[plate.strip()].append(line.strip())
    return dic

#######################################################################################################################
################## insertion of the analysis data ####################################################################
#######################################################################################################################

def analysis_mysql(exp, expgrp,project, merged_file,cnx,pfp,pcfil,quartfil,platDic,prey_interactors,analysisid):
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()

    cursor1 = cnx.cursor()
    cursor2 = cnx.cursor()

## queries ############################################
    plate_possiblehit_input=(""" insert into plates_has_possiblehit (ref_plateid,ref_possiblehitid) values (%s,%s)""")


    possiblehitinput = ("""insert into possiblehit (ref_interactorid,fc,q_val,p_value,
                    ref_analysis_parameterid,filtrationLabel) values (%s,%s,%s,%s,%s,%s)""")  ## wot bait


    ## than add the possible hits with the value and link it to the analysis parameter and the interactors
    with open(merged_file) as mergeOpened:
        next(mergeOpened)
        for lines in mergeOpened:
            splits = lines.split("\t")
            uniqueName=splits[9].strip()
            filtrationType=splits[-1].strip()
            plates=splits[0].strip()

## the entries in teh possible hits
            cursor2.execute(possiblehitinput, (prey_interactors[uniqueName], float(splits[15].strip()), float(splits[13].strip()), float(splits[14].strip()),analysisid,filtrationType))
            posshitid=cursor2.lastrowid
            for eachplate in plates.split(";"):
                if eachplate in platDic:
                    cursor2.execute(plate_possiblehit_input,(platDic[eachplate],posshitid)) ## add the relation between the plate and the possible hits
                else:
                    print("plate is not found",eachplate)
#    print "analysis done for ",plates
    cnx.commit()
    cursor1.close()
    cursor2.close()
#    cnx.close()


########################################################################################################################################
