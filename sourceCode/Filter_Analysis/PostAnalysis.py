__author__ = 'surya'

from Filter_Analysis import CalculatingPositives



## create a dictionary for the positives

def posDictionary(filName):
    posDic={}
    with open(filName) as posFil:
        next(posFil)
        for line in posFil:
            if line !="\n":
                psplits=line.split("\t")
#                spID="_".join(psplits)
                spID=psplits[0].strip()+"_"+psplits[1].strip()+"_"+psplits[2].strip()+"_"+psplits[3].strip()+"_"+psplits[4].strip()+"_"+psplits[5].strip()+"_"+psplits[6].strip()
                if spID not in posDic:
                    posDic[spID]=[line.strip()]
#    print posDic
    return posDic




def gettingPositivesMad(filName,link,nslist,slist):
    posDic=posDictionary(filName)
    c=0.6745
    writes=open(link+"/AllWith_MAD.txt",'w')
    ln = ["Well\tBlock1\tBlock2\tBlock3\tBlock4\tRow\tCol\tType\tunique_name\tEntrenzID\tARTNumber\tFDR\t"
          "Log2FC\tQ-value\tP-Value\tFoldChange"]+["\t","NS"]*(len(nslist))+["\t","Stim"]*(len(slist))+["\t","NA_mad","\t","S_mad","\n"]
    writes.writelines(ln)
    ## 2. look for the entries in the IntIntensity.txt files
    with open(link+"/AllRepTogether_IntegralIntensity.txt") as intint:
            next(intint)
            if posDic !={}:
                for line in intint:
                    splits=line.split("\t")
                    NS=[]
                    NSt=[]
                    St=[]
                    S=[]
    #            print splits[0].strip()
                    if splits[0].strip() in posDic:
                        for i in range(5,5+len(nslist)):
                            NS.append(float(splits[i].strip()))
                            NSt.append(splits[i].strip()+"\t")
                        for j in range(5+len(nslist),5+len(nslist)+len(slist)):
                            S.append(float(splits[j].strip()))
                            St.append(splits[j].strip()+"\t")
                    ## 3. find MAD/mean ABs Dev for each of the the entries
                        Smad= CalculatingPositives.MAD(S,c)
                        NSmad= CalculatingPositives.MAD(NS,c)
                        ln=posDic[splits[0].strip()]+["\t"]+NSt+St+[str(NSmad),"\t",str(Smad),"\n"]
                        writes.writelines(ln)
    return link+"/AllWith_MAD.txt"






