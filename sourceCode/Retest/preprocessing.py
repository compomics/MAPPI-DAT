__author__ = 'surya'

from GeneralMethods import DictionaryMethods
from MathsStats import Stats



## preprocess the analysis file
## merge control,analysis and retest files together

def mergeFiles(controlFormat,AnalysiOutputFile,Analysis2retestFile,folder_path,arrangement,outputfile):
    arrangement_new=arrangement.replace(",","\t")
    mergedout=open(folder_path+"/"+outputfile,"w")
    ln=["FileNAme\tUniqueName\tEntrenzNames\t",arrangement_new,"\tFIwithoutBait\tFIwithBait\tFIwrtPreyNull\tFIwrtBaitNull\tminFI\tstdFI\tcvFI\ttag\twellName\ttype\n"]
    mergedout.writelines(ln)
    wellName="A,B,C,D,E,F,G,H".split(",")

    connectorDic=DictionaryMethods.createDic(Analysis2retestFile,0,[1,2,3],header=True)

    analysisDic=DictionaryMethods.createDicOne(AnalysiOutputFile,9,12,header=True)
    uniqueList=DictionaryMethods.createList(AnalysiOutputFile,9,header=True)
    controlList=DictionaryMethods.createList(controlFormat,0,header=True)
    controlfile=DictionaryMethods.createDicOne(controlFormat,0,1,header=True)

    ## get controls
    emptybaitcontrol=""
    for eachfile in connectorDic:
        type=connectorDic[eachfile][0]
        if type=="control":
            start=0
            for i,eachlinec in enumerate(open(folder_path+"/"+eachfile)):
                if i>7:
                    break
                else:
                    if controlfile[controlList[start]]=="empty":
                        emptybaitcontrol=eachlinec
                        type="empty"
                    else:
                        type="control"
                    FIwithBait,FIwithoutBait,FIPreyNull,FIBaitNull,minFI,stdFC,cvFC,tag=calculateFI(eachlinec,arrangement,emptybaitcontrol)
                    ln=[eachfile,"\t",controlList[start],"\t",controlfile[controlList[start]],"\t",eachlinec.strip(),"\t",FIwithoutBait,"\t",FIwithBait,"\t",
                        FIPreyNull,"\t",FIBaitNull,"\t",minFI,"\t",stdFC,"\t",cvFC,"\t",tag,"\t",wellName[i],"\t",type,"\n"]

    #                print ln
                    mergedout.writelines(ln)
                    start+=1

## do it for analysis as well
    for eachfile in connectorDic:
        type=connectorDic[eachfile][0]
        if type=="analysis":
            astart=int(connectorDic[eachfile][1])-1
            # print(astart)
            print(eachfile)
            # print(len(uniqueList))
            for j,eachline in enumerate(open(folder_path+"/"+eachfile)):
                if j >7:
                    # print eachline
                    break
                else:
                    FIwithBait,FIwithoutBait,FIPreyNull,FIBaitNull,minFI,stdFC,cvFC,tag=calculateFI(eachline,arrangement,emptybaitcontrol)
                    ln=[eachfile,"\t",uniqueList[astart],"\t",analysisDic[uniqueList[astart]],"\t",eachline.strip(),"\t",FIwithoutBait,"\t",FIwithBait,"\t",
                        FIPreyNull,"\t",FIBaitNull,"\t",minFI,"\t",stdFC,"\t",cvFC,"\t",tag,"\t",wellName[j],"\tnormal\n"]
     #               print ln
                    mergedout.writelines(ln)
                    astart+=1
    mergedout.close()
    return folder_path+"/"+outputfile

## calculate the FI

def calculateFI(line,arragement,controlLine):
    arragementlist=arragement.split(",")
    controlList=controlLine.split("\t")
    valuelist=line.split("\t")
    ns,s,nsb,sb=[],[],[],[]
    Cns,Cs,Cnsb,Csb=[],[],[],[]
    for i in range(len(arragementlist)):
        if arragementlist[i]=="NS":
            ns.append(float(valuelist[i]))
            Cns.append(float(controlList[i]))
        elif arragementlist[i]=="S":
            s.append(float(valuelist[i]))
            Cs.append(float(controlList[i]))
        elif arragementlist[i]=="NSB+":
            nsb.append(float(valuelist[i]))
            Cnsb.append(float(controlList[i]))
        elif arragementlist[i]=="SB+":
            sb.append(float(valuelist[i]))
            Csb.append(float(controlList[i]))
        else:
            print(arragementlist[i]+" not found....")

    fcwithB=Stats.mean(sb)/Stats.mean(nsb)
    fcwithoutBait=Stats.mean(s)/Stats.mean(ns)
    fcCwithbait=Stats.mean(Csb)/Stats.mean(Cnsb)
    fcCwithoutbait=Stats.mean(Cs)/Stats.mean(Cns)

    FIwrtnullbait=fcwithB/fcwithoutBait
    FIwrtnullprey=fcwithB/fcCwithbait

    stdFC=Stats.pstdev((FIwrtnullbait,FIwrtnullprey))
    cvFC=stdFC/Stats.mean((FIwrtnullbait,FIwrtnullprey))
    # FIwrtnullBaitnullPrey=fcwithB/fcCwithoutbait

    minFC=min(FIwrtnullbait,FIwrtnullprey)


## get the tagging of the each interactio
    tag=""
    if fcwithB>9:
        if minFC>9:
            tag="positive"
        else:
            if fcwithoutBait>9:
                tag="aspecific"
            else:
                tag="notAnnotated"
    else:
        tag="negative"


    return str(round(fcwithB,2)),str(round(fcwithoutBait,2)),str(round(FIwrtnullprey,2)),str(round(FIwrtnullbait,2)),str(round(minFC,2)),str(round(stdFC,2)),str(round(cvFC,2)),tag
