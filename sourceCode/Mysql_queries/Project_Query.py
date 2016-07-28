__author__ = 'surya'

import MySqlConnection
## mini query
####################### PROJECT ################################
projectInfo="""select p.p_name,(select count(g.e_name) from experiment_group g
                inner join project p on g.ref_projid=p.project_id
                where p.p_name=%s),
                (select count(e.e_name) from experiments e
                inner join experiment_group g on e.ref_expgrpid=g.expgrp_id
                inner join project p on g.ref_projid=p.project_id
                where p.p_name=%s)
                 ,p.description from project p where p.p_name=%s;"""
projectAll="""select p_name from project;"""
Exp_gropAll="""select ex.e_name from experiment_group ex
                inner join project p on p.project_id=ex.ref_projid
                where p.p_name=%s"""
ExpAll="""select e.e_name from experiments e
                inner join experiment_group ex on e.ref_expgrpid=ex.expgrp_id
                inner join project p on p.project_id=ex.ref_projid
                where p.p_name=%s and ex.e_name=%s"""
ExpAllInfo="""select e.e_name,e.experiment_type,e.description from experiments as e
                inner join experiment_group ex on e.ref_expgrpid=ex.expgrp_id
                inner join project p on p.project_id=ex.ref_projid
                where p.p_name=%s and ex.e_name=%s and e.e_name=%s"""
conditionInfo="""select c.Stimulus_type,c.Stimulus_conc,c.BaitTransfectDate,c.protocol_version,c.input_date from exp_condition c
                inner join experiments e on e.ref_conditionid=c.condition_id
                inner join experiment_group ex on e.ref_expgrpid=ex.expgrp_id
                inner join project p on p.project_id=ex.ref_projid
                where p.p_name=%s and ex.e_name=%s and e.e_name=%s"""

conditionInfowithTreatment="""select c.Stimulus_type,c.Stimulus_conc,c.BaitTransfectDate,c.protocol_version,c.input_date,c.treatment_type,c.treatment_con,c.treatment_date from exp_condition c
                inner join experiments e on e.ref_conditionid=c.condition_id
                inner join experiment_group ex on e.ref_expgrpid=ex.expgrp_id
                inner join project p on p.project_id=ex.ref_projid
                where p.p_name=%s and ex.e_name=%s and e.e_name=%s"""

plates=""" select l.p_name from plates l
            inner join experiments e on e.experiment_id=l.ref_expid
            inner join experiment_group g on e.ref_expgrpid=g.expgrp_id
            inner join project p on g.ref_projid=p.project_id
            where p.p_name=%s and g.e_name=%s and e.e_name=%s"""

Stimulating_intInt="""select q.IntInt from quantificationval q
                    inner join spots s on s.spot_id=q.ref_spotid
                    inner join well w on w.well_id=s.ref_wellid
                    inner join plates l on l.plate_id=w.ref_platid
                    inner join experiments e on e.experiment_id=l.ref_expid
                    inner join experiment_group g on e.ref_expgrpid=g.expgrp_id
                    inner join project p on g.ref_projid=p.project_id
                    where p.p_name=%s and g.e_name=%s and e.e_name=%s and l.p_name=%s and w.Stimulus_type=%s;"""

bait="""select b.b_name,c.mbu_bait_code,c.bait_vector_type from bait b
        inner join experiment_group g on g.ref_baitid=b.bait_id
        inner join experiments e on e.ref_expgrpid=g.expgrp_id
        inner join exp_condition c on c.condition_id=e.ref_conditionid
        inner join project p on g.ref_projid=p.project_id
        where p.p_name=%s and g.e_name=%s and e.e_name=%s"""

molecule="""select m.fusion_cpd_type,m.fusion_cpd_conc from molecule m
        inner join experiment_group g on g.ref_molid=m.mol_id
        inner join experiments e on e.ref_expgrpid=g.expgrp_id
        inner join project p on g.ref_projid=p.project_id
        where p.p_name=%s and g.e_name=%s and e.e_name=%s"""

All_interactor="""select count(*),(select count(*) from bait b
        inner join experiment_group g on g.ref_baitid=b.bait_id
        inner join experiments e on e.ref_expgrpid=g.expgrp_id
        inner join project p on g.ref_projid=p.project_id
        where p.p_name=%s and g.e_name=%s and e.e_name=%s),
        (select count(*) from molecule m
        inner join experiment_group g on g.ref_molid=m.mol_id
        inner join experiments e on e.ref_expgrpid=g.expgrp_id
        inner join project p on g.ref_projid=p.project_id
        where p.p_name=%s and g.e_name=%s and e.e_name=%s)
         from interactors i
        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
        inner join experiments e on e.ref_expgrpid=g.expgrp_id
        inner join project p on g.ref_projid=p.project_id
        where p.p_name=%s and g.e_name=%s and e.e_name=%s """

# all_positives="""select p.p_name,i.inttype,h.FC_class,h.pfp,h.p_value,h.ns_mad,h.s_mad,h.filtration_label from possiblehit h
#             inner join interactors i on i.idInteractors=h.ref_interactorid
#             inner join prey p on p.prey_id=i.ref_preyid
#             inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
#             inner join experiments e on g.expgrp_id=e.ref_expgrpid
#             inner join project pr on pr.project_id = g.ref_projid
#             where e.e_name=  %s and g.e_name= %s and pr.p_name= %s"""

select_positives="""select p.p_name,i.inttype,p.entrenz_name,h.fc,h.q_val,h.p_value,h.filtrationLabel from possiblehit h
                    inner join analysis_parameters a on a.analysis_id=h.ref_analysis_parameterid
                    inner join experiments e on e.experiment_id=a.ref_expid
                    inner join experiment_group g on e.ref_expgrpid=g.expgrp_id
                    inner join interactors i on i.idInteractors=h.ref_interactorid
                    inner join prey p on p.prey_id=i.ref_preyid
                    inner join project pr on pr.project_id = g.ref_projid
                    where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s """

# dummies_inserted="""select p.p_name,i.inttype from interactors i
#                     inner join prey p on p.prey_id=i.ref_preyid
#                     inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
#                     inner join experiments e on e.ref_expgrpid= g.expgrp_id
#                     inner join project pr on pr.project_id = g.ref_projid
#                     where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s"""

NotFound    =    """select p.p_name,i.inttype,p.entrenz_name from interactors i
                    inner join prey p on p.prey_id=i.ref_preyid
                    inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                    inner join experiments e on e.ref_expgrpid= g.expgrp_id
                    inner join project pr on pr.project_id = g.ref_projid
                    where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s  and i.idInteractors not in
                    (select i.idInteractors from possiblehit h
                    inner join interactors i on i.idInteractors=h.ref_interactorid
                    inner join prey p on p.prey_id=i.ref_preyid
                    inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                    inner join experiments e on e.ref_expgrpid= g.expgrp_id
                    inner join project pr on pr.project_id = g.ref_projid
                    where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s) """

# Found   =        """select count(*) from possiblehit h
#                     inner join interactors i on i.idInteractors=h.ref_interactorid
#                     inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
#                     inner join experiments e on e.ref_expgrpid= g.expgrp_id
#                     inner join project pr on pr.project_id = g.ref_projid
#                     where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s """

AllPrey=         """select p.p_name,i.inttype,p.entrenz_name from interactors i
                    inner join prey p on p.prey_id=i.ref_preyid
                    inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                    inner join experiments e on e.ref_expgrpid= g.expgrp_id
                    inner join project pr on pr.project_id = g.ref_projid
                    where e.e_name=  %s and g.e_name= %s and pr.p_name= %s"""

Parameter_Analysis=""" select a.q_val_threshold,a.particle_count_filtration,a.quartile_filtration from analysis_parameters a
                      inner join experiments e on a.ref_expid=e.experiment_id
                      inner join experiment_group g on g.expgrp_id=e.ref_expgrpid
                      inner join project pr on pr.project_id = g.ref_projid
                      where e.e_name=  %s and g.e_name= %s and pr.p_name= %s"""

GetAllRetest=       """ select r.r_name,r.reason,r.submission_date,r.retest_date,r.done_by from retest r
                        inner join experiments_has_retest c on c.ref_retestid=r.restest_id
                        inner join experiments e on e.experiment_id=c.ref_expid
                        inner join experiment_group g on g.expgrp_id=e.ref_expgrpid
                        inner join project p on p.project_id=g.ref_projid
                        where p.p_name=%s and g.e_name=%s and e.e_name=%s"""

GetAllRetestData= """select f.file_name,i.row,i.col,i.well_type,i.intensity, y.p_name,y.entrenz_name,o.FI_baitNull,o.FI_preyNull,o.tag,o.type from prey y
                        inner join retest_analysis_output o on o.ref_preyid=y.prey_id
                        inner join retest_eachcell_intensity i on i.ref_retest_analyid = o.pos_id
                        inner join retest_files f on f.file_id=i.ref_fileid
                        inner join retest r on r.restest_id=f.ref_retest
                        inner join experiments_has_retest c on c.ref_retestid=r.restest_id
                        inner join experiments e on e.experiment_id=c.ref_expid
                        inner join experiment_group g on g.expgrp_id=e.ref_expgrpid
                        inner join project p on p.project_id=g.ref_projid
                        where p.p_name=%s and g.e_name=%s and e.e_name=%s and r.r_name=%s"""

checkTreatment   = """ """

Plates=         """ """
Art=            """ """
ArtWell =       """ """
TNames =        """ """
Mixture =       """ """



###########################
## select more than one and return as a list
def Select_all(Query,cnx,argument="Null",arg=False,int=False):
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()

    count=0
    small=""
    rep_list=[]
    cursor1 = cnx.cursor()
    if arg:
        cursor1.execute(Query,argument)
    else:
        cursor1.execute(Query)
    for ent in cursor1:
        for val in ent:
            if int:
                rep_list.append(float(val))
            else:
                rep_list.append(str(val))
    cnx.commit()
    cursor1.close()
    return rep_list


def Select_values(Query,cnx,argument="Null",arg=False):
    if not cnx.is_connected():
        cnx=MySqlConnection.connectSql()
#    import mysql.connector
    count=0
    small=[]
    rep_list=[]
    cursor1 = cnx.cursor()
    if arg:
        cursor1.execute(Query,argument)
    else:
        cursor1.execute(Query)
    for ent in cursor1:
#        print ent
        small=[]
        for val in ent:
            small.append(str(val))
        rep_list.append(small)
    cnx.commit()
    cursor1.close()
    return rep_list

