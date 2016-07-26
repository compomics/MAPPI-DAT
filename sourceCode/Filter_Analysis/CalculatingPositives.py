__author__ = 'surya'

## find median for a integer list

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

## uses median method and return median absolute deviation for the list and a constant that is universal

def MAD(lists,c):
    mad=[]
    for i in lists:
        mad.append(abs(i - median(lists)))
    return median(mad)/c

###### calculate percentile
def percentile(N, percent, key=lambda x:x):
    import math
    import functools
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1


## using percentile it finds threshold for all replicates separately and return list of all threshold for each replicate

def threshold(link,i):
    thresh=0.0
    indList=[]
    with open(link+"_IntegralIntensity.txt") as files:
            next(files)
            for line in files:
                splits = line.split("\t")
                indList.append(float(splits[i].strip()))
    indList.sort()
    thresh=percentile(indList,.75)+1.5*(percentile(indList,.75)-percentile(indList,.25))
    return thresh

"""thresh contain threshold for
    NS  S1  S2  S3 """

def calculatingPos(intFile,nsrep,srep,plateList,quartileOutDic):
    start=5
    Teslist = range(start,len(nsrep)+len(srep)+start) # shows the column number for each replicate
    control=[0]*(len(nsrep)+len(srep))
    sd=[0]*(len(nsrep)+len(srep))
    na=[0]*(len(nsrep)+len(srep))
    filteration=[]
    for i in Teslist:
        filt=threshold(intFile,i)
        filteration.append(filt)
        with open(intFile+"_IntegralIntensity.txt") as files:
            next(files)
            for line in files:
                splits = line.split("\t")
                if float(splits[i].strip()) >= filt:
#                    print splits[1].strip()
                    if splits[1].strip()=='control+':
                        control[i-5]+=1
                    elif splits[1].strip() =='SD+control':
                        sd[i-5]+=1
                    elif splits[1].strip() in ["NA","NAc+","NAsd+"]:
                        na[i-5]+=1
    write=open(intFile+"_Statistics.txt",'w')
    nameFolder=intFile.split("/")[-2]
    ln=["Statistics for ", nameFolder,"the files\nplate\twell\tControl+\tSD+\tNA\tthreshold\n"]
    write.writelines(ln)
    bothrep=nsrep+srep
    divide_by=len(plateList)
    plateListmerged=[]
    for i in range(len(plateList)):
        plateListmerged+=[plateList[i]]*(len(nsrep)/divide_by)
    for j in range(len(plateList)):
        plateListmerged+=[plateList[j]]*(len(srep)/divide_by)
    index=0
    for i in range(len(nsrep)+len(srep)):
        ln=[plateListmerged[index],"\t",bothrep[index],"\t",str(control[i]),"\t",str(sd[i]),"\t",str(na[i]),"\t",str(filteration[i]),"\n"]
        write.writelines(ln)
        if plateListmerged[index] not in quartileOutDic:
            quartileOutDic[plateListmerged[index]]={bothrep[index]:filteration[i]}
        else:
            quartileOutDic[plateListmerged[index]][bothrep[index]]=filteration[i]
        index+=1
    # print quartileOutDic
    return quartileOutDic


########################################################################################
def filter(file, filt, ind):
        with open(file) as files:
            next(files)
            filterList = []
            for line in files:
                splits = line.split("\t")
                if float(splits[ind].strip()) >= filt:
                    filterList.append(splits[2].strip())
        return filterList

## a quartile based filtration.... after the main filtration also check with the quartile filtration
## if the entry have value above the 3Q+1.5IQR in NS in atleast n-1 entries than remove them in from the final filtration

def analysis_quartile(link,nslist,slist,nsnames,snames):
    filtered={}
    checkname={}
    final=[]
    input=link+"_IntegralIntensity.txt"
    # threshold_dic={}
    allrep=nsnames+snames
    index=0
    for i in range(6,nslist+slist+6):
        quart=threshold(link,i)
        # threshold_dic[index]=[quart,allrep[index]]
        index+=1
        filtered[i]=filter(input,quart,i)
    for j in range(6,nslist+6):
        for name in filtered[j]:
            if name not in checkname:
                checkname[name]=1
            elif name in checkname:
                checkname[name]+=1
    for entry in checkname:
        if checkname[entry]>=nslist-nslist/2:
            final.append(entry)
    return final


####################################################################################################
## apply PC count filtration only on S on each of the replicate and if more than 50% is smaller than threshold than neglect that

def PCfiltration(link,nslist,slist,PCthreshold):
    dic={}
    pcfilter=[]
    input=link+"_Particle_Count.txt"
    with open(input) as files:
        next(files)
        for line in files:
            PCvalue=""
            splits = line.split("\t")
            nsaverage=0
            nscount=0
            totalnsaverage=0
            for eachNS in range(5,5+nslist):
                nsaverage=nsaverage+float(splits[eachNS].strip())
#                print float(splits[eachNS].strip())
                nscount+=1
                PCvalue=PCvalue+splits[eachNS].strip()+"\t"
            totalnsaverage=nsaverage/nscount
            saverage=0
            scount=0
            totalsaverage=0
            scountthreshold=0
            for eachs in range(5+nslist,5+nslist+slist):
                saverage+=float(splits[eachs].strip())
                PCvalue=PCvalue+splits[eachs].strip()+"\t"
#                print float(splits[eachs].strip()), PCthreshold
                if float(splits[eachs].strip())>=float(PCthreshold):
                    scountthreshold+=1
                scount+=1
#            print scountthreshold

            totalsaverage=saverage/scount
#            print scountthreshold,totalsaverage,totalnsaverage
            if totalsaverage >= totalnsaverage and scountthreshold >(slist/2):
                pcfilter.append(splits[2].strip())
            dic[splits[2].strip()]=PCvalue.strip()
    return dic,pcfilter


                #indList.append(float(splits[i].strip()))


###################################################################################################################
################### check for the particle count filtration######################################################
## apply PC count filtration only on S on each of the replicate and if more than 50% is smaller than threshold than neglect that

def PCLabelledOutLiers(link,nscount,scount,PCthreshold):
    pcfilterOutliers=[]
    input=link+"_Particle_Count.txt"
    with open(input) as files:
        next(files)
        for line in files:
            splits = line.split("\t")
            # calculate the median
            nsList=[float(splits[ind].strip()) for ind in range(6,6+nscount)]
            NSMedian=median(nsList)
            #calculate median for stimulated
            scountthreshold=0
            sList=[]
            for eachs in range(6+nscount,6+nscount+scount):
                sList.append(float(splits[eachs].strip()))
                if float(splits[eachs].strip())>=float(PCthreshold):
                    scountthreshold+=1
            SMEdian=median(sList)
            #check if condition satissfy
            if SMEdian < NSMedian or scountthreshold <=(scount/2):
                pcfilterOutliers.append(splits[2].strip())
    return pcfilterOutliers
