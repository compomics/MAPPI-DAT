__author__ = 'surya'
#from Error_handle import ErrorHandling
import os
from tkMessageBox import *
from Mysql_queries import GetExistingDataFromDatabase, mysql_smallMethods,MySqlConnection



def IO_prob(problem):
    showerror("Error", problem)



def input_mysql(Tplate2Path,plate2subfolder,ns, s,p_name, preason, eg_name, bait_name, e_name,e_date,expReason,Scanningdate,mbubait_code,
                BaitvectorType,stimuluType, stimulusconc, protocolType,treatmentType,TreatmentConc,Treatementdate,treatment_starttime,
                treatment_endtime,aspeficDic,cnx,mappit,maspit,kiss,treatment,fusion_cpd,fusion_cps_conc,
                moleculeExtraInfo,linkageDic,plate_tfileDic,BaitTransfectDate,path):


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

    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()
    proj_present = False
    expgrp_present = False

    nslist = ns.split(",")
    nsreplicate = len(nslist)
    slist = s.split(",")
    sreplicate = len(slist)

    artwell_withName_input = ("""insert into art_well (w_name,well1id,well2id,well3id,well4id) values (%s,%s,%s,%s,%s)""")
    artwell_wOTName_input = ("""UPDATE art_well set well1id=%s,well2id=%s,well3id=%s,well4id=%s where well_id=%s""")

    art_input = ("""insert into art (a_name) values (%s)""")

    art2well_input = ("""insert into artwell_has_art (ref_wellid,ref_artid) values (%s,%s)""")

    mixture_input = ("""insert into mixture (mixture_name) values (%s)""")

    preannotaiont_input = ("""insert into preyannotationt (p_name) values (%s)""")

    tplaterelation_input = ("""insert into tplaterelation (ref_panid,ref_experimentid) values (%s,%s)""")

    project_input = ("""insert into project (p_name,description) values (%s,%s)""")

    experimentGrp_input = ("""insert into experiment_group (e_name,ref_projid) values (%s,%s)""")

    #        prey_input= ("""insert into prey (sequence,homology,weight,p_name,ref_panid,entrenz_name) values (%s,%s,%s,%s,%s,%s)""")
    prey_input = ("""insert into prey (p_name,ref_panid,entrenz_name,plate_nr,ref_artid,ref_mixtureid,ref_artwellid)
                    values (%s,%s,%s,%s,%s,%s,%s)""")

    bait_input = ("""insert into bait (b_name) values (%s)""")

    molecule_input = ("""insert into molecule (fusion_cpd_type,fusion_cpd_conc,extra_info) values (%s,%s,%s)""")

    interactors_inp = ("""insert into interactors (ref_expgrpid,ref_preyid,inttype) values (%s,%s,%s)""")

    expcondition = (
        """insert into exp_condition (stimulus_type,stimulus_conc,Scanning_date,mbu_bait_code,NSreplicate,Sreplicate,
            bait_vector_type,protocol_version,treatment_type,treatment_con,treatment_date,start_treatment,end_treatment,
            input_date,BaitTransfectDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
    expcondition_wottreatment = (
        """insert into exp_condition (stimulus_type,stimulus_conc,Scanning_date,mbu_bait_code,NSreplicate,Sreplicate,
            bait_vector_type,protocol_version,input_date,BaitTransfectDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

    exp2plate=("""insert into exp_has_plates (ref_expid,ref_plateid) values (%s,%s)""")
    experiments_input = (
        """insert into experiments (e_name,description, e_quality,ref_expgrpid,ref_conditionid,experiment_type) values (%s,%s,%s,%s,%s,%s)""")

    wells_input = ("""insert into well (w_name,stimulus_type,ref_platid) values (%s,%s,%s)""")

    spots_input = ("""insert into spots (row,col,block,ref_wellid,ref_interactorid) values (%s,%s,%s,%s,%s)""")

    quantificationVal_input = (
        """insert into quantificationval (pc,meanarea,grayvalmean,meangrayvalmean,meanintint,area_fraction,intint,ref_spotid)
        values (%s,%s,%s,%s,%s,%s,%s,%s)""")

    Aspecific_input=("""insert into aspecifics (ref_preyid,ref_experimentid) values (%s,%s)""")


#####################################################################################################################
######################## get all the data from database ############################################################

    projectDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT project_id,p_name FROM project""",cnx)
    expgrpDic={}
    preAnnotationDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT pan_id,p_name from preyannotationt""",cnx)
    mixtureDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT mixture_id,mixture_name from mixture""",cnx)
    artDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT art_id,a_name from art""",cnx)
    artWellDic=GetExistingDataFromDatabase.get2colmergedata_fromDatabase("""SELECT w.well_id,w.w_name,a.a_name from art_well w
                                                                      inner join artwell_has_art r on r.ref_wellid=w.well_id
                                                                      inner join art a on a.art_id =r.ref_artid
                                                                      """,cnx) # key= wellName_ArtName
    preyDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT prey_id,p_name FROM prey""",cnx)
    platDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT plate_id,p_name From plates """, cnx)
#    tplate2mixture=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT ref_mixtureid,ref_panid From mixture_relation_tplate """, cnx,append=True)
    # platDic={}
    plat_wellDic={} ## {plat:{well:wellid}}
    # quartileIdList=[] ##
    tplat_expDic={}
    tplat_mixture={}

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
        econ =mysql_smallMethods.OnlyInsert(expcondition, (stimuluType,stimulusconc,Scanningdate,mbubait_code, nsreplicate,sreplicate,BaitvectorType,protocolType,treatmentType,TreatmentConc,
                                       Treatementdate,treatment_starttime,treatment_endtime,e_date,BaitTransfectDate),cnx)
    else:
        econ = mysql_smallMethods.OnlyInsert(expcondition_wottreatment,
            (stimuluType,stimulusconc,Scanningdate,mbubait_code, nsreplicate,sreplicate,
             BaitvectorType,protocolType,e_date,BaitTransfectDate),cnx)


    ## insert the new experiment taking the foreign key value from group and condition
    ref_expid  = mysql_smallMethods.OnlyInsert(experiments_input, (e_name, expReason, 0, expgrp, econ, exp_type),cnx)
    cnx.commit()
    ## Now check if the project and experiment group already exist than do not insert the prey again....
    if not (proj_present and expgrp_present):
        ## also insert the new bait entry for the project
        ## open file for bait
        baitid=mysql_smallMethods.OnlyInsert(bait_input,(bait_name,),cnx)
                ## open file for the molecule
        if maspit:
            molid=mysql_smallMethods.OnlyInsert(molecule_input, (fusion_cpd,fusion_cps_conc,moleculeExtraInfo))
            ## update the foreign key linking to bait and molecule
            mysql_smallMethods.UpdateTable(""" UPDATE experiment_group set ref_baitid= %s , ref_molid=%s where expgrp_id=%s""",
                            (baitid, molid, expgrp),cnx)
        else:
            mysql_smallMethods.UpdateTable(""" UPDATE experiment_group set ref_baitid= %s where expgrp_id=%s""",
                                           (baitid, expgrp),cnx)
        ### adding the prey entry
        print "started with adding protein information...."
#        mixture_dic={}
        print "total proteins Aspecific found are ",len(aspeficDic)
        cnx.commit()
        for entry in Tplate2Path: ## this is the dic {Tfilename=path of t file}
            TPsplit = entry.split(".")
## start adding the t-files only if it is not already present in the database
            # if TPsplit[0].strip() not in preAnnotationDic: # start with the T file only if the T-plate is not in the database else all the schema is same
                # tplate is not present add the t-plate in the db
            tplatePresent, ref_tplateid, preAnnotationDic = mysql_smallMethods.CheckPresenese_Insert(preannotaiont_input,
                                                                                             (TPsplit[0],),TPsplit[0],preAnnotationDic, cnx)
            # cursor5.execute(preannotaiont_input,(TPsplit[0],))
            # tplate=cursor5.lastrowid
            preAnnotationDic[TPsplit[0].strip()]=ref_tplateid
            print "doing file: ", entry
            # go through each line and add unique name in prey

            with open(Tplate2Path[entry]) as pfile:
                next(pfile)
                for line in pfile:
                    psplits = line.strip().split("\t")
                    ## add mixtures ## this uses the mixture information from each of the protein in protein file dic[M1]=mix_id
                    mixPresent,ref_mixtureid,mixtureDic= mysql_smallMethods.CheckPresenese_Insert(mixture_input, (psplits[-1].strip(),),psplits[-1].strip(),mixtureDic,cnx)
                    ## add art names if does not exist
                    artName="ART" + psplits[0].strip()
                    artpresent,ref_artid,artDic= mysql_smallMethods.CheckPresenese_Insert(art_input, (artName,),artName,artDic,cnx)
                    ## add the art well names
                    artwellName=psplits[1].strip()
                    if artwellName+"_"+artName not in artWellDic:
                        ref_artwellid =mysql_smallMethods.OnlyInsert(artwell_withName_input,
                        (artwellName,psplits[2].strip(),psplits[3].strip(),psplits[4].strip(),psplits[5].strip()),cnx)
                        art2wellId=mysql_smallMethods.OnlyInsert(art2well_input,(ref_artwellid,ref_artid),cnx)
                        artWellDic[artwellName + "_" + artName]=ref_artwellid
                    else:
                        ref_artwellid=artWellDic[artwellName+"_"+artName]
                        art2wellWOTid=mysql_smallMethods.OnlyInsert(artwell_wOTName_input,
                            (psplits[2].strip(),psplits[3].strip(),psplits[4].strip(),psplits[5].strip(),ref_artwellid),cnx)
                    ## add the prey name
                    prpresent,protein,preyDic= mysql_smallMethods.CheckPresenese_Insert(prey_input,
                        (psplits[10].strip(), ref_tplateid, psplits[12].strip(),psplits[8].strip(),ref_artid,ref_mixtureid,ref_artwellid),
                                                        psplits[10].strip(),preyDic,cnx)

                    ## add interactors entry
                    if psplits[10].strip() in aspeficDic:
                        type="A-specific"
                    else:
                        type=psplits[15].strip()
                    interactorId=mysql_smallMethods.OnlyInsert(interactors_inp, (expgrp, protein,type),cnx)

            ## add the realtion between the tplate and exp only if it does not exist
            if ref_tplateid not in tplat_expDic:
                tplatId=mysql_smallMethods.OnlyInsert(tplaterelation_input, (ref_tplateid, ref_expid),cnx)
                tplat_expDic[ref_tplateid] = ref_expid
            cnx.commit()

    print "started adding A-specifics"

    # aspecDic={}
    for apec in aspeficDic:
        if apec in preyDic:
            apecId=mysql_smallMethods.OnlyInsert(Aspecific_input,(preyDic[apec],ref_expid),cnx)

    welldic = {'W1': 1, 'W2': 2, 'W3': 3, 'W4': 4}
    print "started processing each plate..", len(plate2subfolder)

    ### get all the interactor id for all the prey for this exp,egroup, project
    getAllPrey2InteractorId="""select i.idinteractors,p.p_name from interactors i
        inner join prey p on p.prey_id=i.ref_preyid
        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
        inner join project j on j.project_id=g.ref_projid
        inner join experiments e on g.expgrp_id=e.ref_expgrpid
        where g.expgrp_id=%s and e.experiment_id=%s and j.project_id=%s"""

    prey_interactorDic=GetExistingDataFromDatabase.getAlldata_fromDatabase(getAllPrey2InteractorId,cnx,query_val=(expgrp, ref_expid, project))

    print len(prey_interactorDic)
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
            mysql_smallMethods.UpdateTable(""" UPDATE plates set ref_panid= %s where p_name=%s""", (tplatNameid,pl),cnx)
            ref_plateid=platDic[pl]
            exp2plateId=mysql_smallMethods.OnlyInsert(exp2plate,(ref_expid,ref_plateid),cnx)
        print pl, " updated in the database...."
        plat_wellDic[pl]={}
        for ns_w in nslist: ## add the well for on stimulated
            plat_wellDic[pl][ns_w]=mysql_smallMethods.OnlyInsert(wells_input, (ns_w, "Non-Stimulating",platDic[pl]),cnx)
        for s_w in slist: ## add the well for stimulated
            plat_wellDic[pl][s_w] =mysql_smallMethods.OnlyInsert(wells_input, (s_w, "Stimulating",platDic[pl]),cnx)

       ## now start adding the spots, quantification val
        for w in plate2well2lineDic[pl]:
            for eachLine in plate2well2lineDic[pl][w]:
                splits = eachLine.split("\t")
                spl = splits[0].split("_")
                uniquename=splits[2].strip()
                platename=splits[5].strip()

                if uniquename in prey_interactorDic:
                    interid=prey_interactorDic[splits[2].strip()]
                    spots =mysql_smallMethods.OnlyInsert(spots_input,
                        (spl[5].strip(), spl[6].strip(), spl[welldic[w]].strip(), plat_wellDic[platename][w], interid),cnx)
                    quatId=mysql_smallMethods.OnlyInsert(quantificationVal_input,
                                    (float(splits[11].strip()), float(splits[12].strip()), float(splits[13].strip()),
                                     float(splits[14].strip()), float(splits[15].strip()), float(splits[16].strip()),
                                     float(splits[17].strip()), spots),cnx)
        cnx.commit()
    """" add new tables in the database: well,quartile threshold, analysis paramater"""
                ## insert the plates corresponding for each of the subfolder

    if cnx.is_connected():
        cnx.close()
    return ref_expid, expgrp, project,platDic

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
            posshitid=mysql_smallMethods.OnlyInsert(possiblehitinput,
                        (prey_interactors[uniqueName], float(splits[15].strip()), float(splits[13].strip()),
                         float(splits[14].strip()),analysisid,filtrationType),cnx)
            for eachplate in plates.split(";"):
                if eachplate in platDic:
                    platId=mysql_smallMethods.OnlyInsert(plate_possiblehit_input,(platDic[eachplate],posshitid),cnx) ## add the relation between the plate and the possible hits
                else:
                    print("plate is not found",eachplate)
    cnx.commit()
    if cnx.is_connected():
        cnx.close()
#    print "analysis done for ",plates


########################################################################################################################################
