

########################################################################################################################
######################### diable other buttons #########################################################################
########################################################################################################################

def disable_checkbox(checkbox1,checkbox2=0,treatment=0,treatment_opp=0,host_box=False):
    if host_box:
        checkbox1.configure(state='disabled')
        if checkbox2!=0:
            checkbox2.configure(state='disable')
        if treatment!=0:
            treatment.configure(state='normal')
        if treatment_opp!=0:
            treatment_opp.configure(state='disable')
    else:
        checkbox1.configure(state='normal')
        if checkbox2!=0:
            checkbox2.configure(state='normal')
        if treatment!=0:
            treatment.configure(state='disable')
        if treatment_opp!=0:
            treatment_opp.configure(state='disable')

## disable other boxes

def disableForReprocessing(Aspecific,IncludeAspecific,host_box=False):
    if host_box:
#        linkageFile.configure(state='disabled')
        Aspecific.configure(state='disabled')
        IncludeAspecific.configure(state='disabled')
        # ProcessAllPara.configure(state='disabled')
#        submit2db.configure(state='disabled')
    else:
#       linkageFile.configure(state='normal')
        Aspecific.configure(state='normal')
        IncludeAspecific.configure(state='normal')
        # ProcessAllPara.configure(state='normal')
#        submit2db.configure(state='normal')
