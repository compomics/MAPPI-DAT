__author__ = 'surya'

## how many relicate are found in the particular experiment

def replicateNumber(exp,epgrp,project,cnx):
    import mysql.connector
    count=0
    rep_list=[]
    cursor1 = cnx.cursor()
    cursor1.execute("""select c.NSreplicate+c.Sreplicate,c.NSreplicate, c.Sreplicate from exp_condition c
                       inner join experiments e on e.ref_conditionid=c.condition_id
                       inner join experiment_group g on g.expgrp_id=e.ref_expgrpid
                       inner join project p on p.project_id = g.ref_projid
                      where e.e_name= %s and g.e_name=%s and p.p_name=%s""",(exp,epgrp,project))
    for out in cursor1:
        for ent in out:
            rep_list.append(ent)
    cnx.commit()
    cursor1.close()
    return rep_list

## how many possible hits are found including the controls.
def HowManyPositivesIncluding(exp,epgrp,project,cnx):
    import mysql.connector
    count=0
    rep_list=[]
    cursor1 = cnx.cursor()
    cursor1.execute("""select (select count(*) from possiblehit h
                        inner join interactors i on i.idInteractors=h.ref_interactorid
                        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                        inner join experiments e on e.ref_expgrpid=g.expgrp_id
                        inner join project pr on pr.project_id = g.ref_projid
                        where e.e_name= %s and g.e_name=%s and pr.p_name=%s),
                        (select count(*) from possiblehit h
                        inner join interactors i on i.idInteractors=h.ref_interactorid
                        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                        inner join experiments e on e.ref_expgrpid=g.expgrp_id
                        inner join project pr on pr.project_id = g.ref_projid
                        where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s ),
                        (select count(*) from possiblehit h
                        inner join interactors i on i.idInteractors=h.ref_interactorid
                        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                        inner join experiments e on e.ref_expgrpid=g.expgrp_id
                        inner join project pr on pr.project_id = g.ref_projid
                        where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s) ,
                        (select count(*) from possiblehit h
                        inner join interactors i on i.idInteractors=h.ref_interactorid
                        inner join experiment_group g on g.expgrp_id=i.ref_expgrpid
                        inner join experiments e on e.ref_expgrpid=g.expgrp_id
                        inner join project pr on pr.project_id = g.ref_projid
                        where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s);""",(exp,epgrp,project,exp,epgrp,project,"sd+control",exp,epgrp,project,"control+",exp,epgrp,project,"NA"))
    for out in cursor1:
        for ent in out:
            rep_list.append(ent)

    cnx.commit()
    cursor1.close()
    return rep_list


#...................................................................................................
def PositivesFound(exp,epgrp,project,cnx):
    import mysql.connector
    rep_list=[]
    cursor1 = cnx.cursor()
    cursor1.execute("""select count(*) from possiblehit h
                        inner join analysis_parameters a on a.analysis_id=h.ref_analysis_parameterid
                        inner join experiments e on e.experiment_id=a.ref_expid
                        inner join experiment_group g on e.ref_expgrpid=g.expgrp_id
                        inner join interactors i on i.idInteractors=h.ref_interactorid
                        inner join project pr on pr.project_id = g.ref_projid
                        where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and
                         (i.inttype= "NAsd+" or i.inttype= "NAc+" or i.inttype= "NA");""",
                            (exp,epgrp,project))
    natotal=0
    for out in cursor1:
        for ent in out:
            natotal=natotal+ent
#    print(natotal)
    rep_list.append(natotal)

    cursor1.execute(""" select count(*) from possiblehit h
                        inner join analysis_parameters a on a.analysis_id=h.ref_analysis_parameterid
                        inner join experiments e on e.experiment_id=a.ref_expid
                        inner join experiment_group g on e.ref_expgrpid=g.expgrp_id
                        inner join interactors i on i.idInteractors=h.ref_interactorid
                        inner join project pr on pr.project_id = g.ref_projid
                        where e.e_name=  %s and g.e_name= %s and pr.p_name= %s and i.inttype= %s""",(exp,epgrp,project,"A-specific"))
    for (a,) in cursor1:
        rep_list.append(a)

#    print rep_list
    cnx.commit()
    cursor1.close()
    return rep_list
