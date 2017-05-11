__author__ = 'surya'

from GeneralMethods import DictionaryMethods
from MathsStats import Stats



## preprocess the analysis file
def parseRawFile(Analysis2retestFile, folder_path):
    dic = {}
    with open(Analysis2retestFile) as connectFile:
        next(connectFile)
        for line in connectFile:
            splits = line.split("\t")
            FileName = splits[0].strip()
            if FileName not in dic:
                outList = []
                with open(folder_path+"/"+FileName) as openedFile:
                    next(openedFile)  # escaping header
                    next(openedFile)  # escaping col number
                    for line in openedFile:
                        splits = line.strip().split("\t")
                        line2append = "\t".join(splits[1:])  # escaping row notations
                        outList.append(line2append)
                        if splits[0] == "H":
                            break
                dic[FileName]=outList
    return dic


## merge control,analysis and retest files together

def mergeFiles(controlFormat,AnalysiOutputFile,Analysis2retestFile,folder_path,arrangement,threshold,outputfile):
    arrangement_new=arrangement.replace(",","\t")
    mergedout=open(folder_path+"/"+outputfile,"w")
    mainList=[]
    ln=["FileNAme\tUniqueName\tEntrenzNames\t",arrangement_new,"\tFCwithoutBait\tFCwithBait\tFIwrtPreyNull\tFIwrtBaitNull\t"
                                            "minFI\tstdFI\tcvFI\ttag\twellName\ttype\n"]
    mergedout.writelines(ln)
    # wellName="A,B,C,D,E,F,G,H".split(",")

    # connectorDic=DictionaryMethods.createDic(Analysis2retestFile,0,[1,2,3],header=True) ## filename:[type,start,end]
    connectorDic={}
    analysisDic=DictionaryMethods.createDic(AnalysiOutputFile,0,[1,2],header=True)#uniqueName:[entrezname,WellName]
    uniqueList=DictionaryMethods.createList(AnalysiOutputFile,0,header=True)#uniqueName
    controlList=DictionaryMethods.createList(controlFormat,0,header=True)#uniqueName
    controlfile=DictionaryMethods.createDic(controlFormat,0,[1,2],header=True)#uniqueName:[Names,wellName]
    EachFile2LineDic=parseRawFile(Analysis2retestFile, folder_path)
    ## get controls
    emptybaitcontrol=""
    with open(Analysis2retestFile) as connectFile:
        next(connectFile)
        for line in connectFile:
            splits=line.split("\t")
            eachfile=splits[0].strip()
            type=splits[1].strip()
            if type=="control":
                lineStart=int(splits[4].strip())-1
                lineEnd=int(splits[5].strip())
                start=0
                for i in range(lineStart, lineEnd):
                    eachlinec = EachFile2LineDic[eachfile][i]
                    if controlfile[controlList[start]][0] == "empty":
                        emptybaitcontrol = eachlinec
                        type = "empty"
                    else:
                        type = "control"
                    FIwithBait,FIwithoutBait,FIPreyNull,FIBaitNull,minFI,stdFC,cvFC,tag=calculateFI(eachlinec,arrangement,
                                                                                                    emptybaitcontrol,threshold)
                    ln=[eachfile,controlList[start],controlfile[controlList[start]][0],eachlinec.strip(),
                        FIwithoutBait,FIwithBait,FIPreyNull,FIBaitNull,minFI,stdFC,cvFC,tag,
                        controlfile[controlList[start]][1],type]
                    toadd="\t".join(ln)
                    mainList.append(toadd)
                    mergedout.writelines(toadd+"\n")
                    start+=1
            else:
                connectorDic[eachfile]=splits[1:6]

    ## do it for analysis as well
        for eachfile in connectorDic:
            type=connectorDic[eachfile][0]
            if type=="analysis":
                astart=int(connectorDic[eachfile][1])-1
                # print(astart)
                print(eachfile)
                # print connectorDic[eachfile]
                lineStart = int(connectorDic[eachfile][3])-1
                lineEnd = int(connectorDic[eachfile][4])
                # print(len(uniqueList))
                for i in range(lineStart, lineEnd):
                    eachline = EachFile2LineDic[eachfile][i]
                    FIwithBait,FIwithoutBait,FIPreyNull,FIBaitNull,minFI,stdFC,cvFC,tag=calculateFI(eachline,arrangement,
                                                                                                    emptybaitcontrol,threshold)

                    ln = [eachfile,uniqueList[astart],analysisDic[uniqueList[astart]][0], eachline.strip(),
                          FIwithoutBait, FIwithBait, FIPreyNull, FIBaitNull, minFI, stdFC, cvFC, tag,
                          analysisDic[uniqueList[astart]][1],"analysis"]
                    toadd = "\t".join(ln)
                    mainList.append(toadd)
                    mergedout.writelines(toadd + "\n")
                    astart+=1
    mergedout.close()
    print "done analysis!"
    return mainList

## calculate the FI

def calculateFI(line,arragement,emptyBaitLine,threshold):
    arragementlist=arragement.split(",")
    controlList=emptyBaitLine.split("\t")# emptyBaitline
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
    fcwithoutBait=Stats.mean(s)/Stats.mean(ns) #without bait
    fcCwithbait=Stats.mean(Csb)/Stats.mean(Cnsb) #without prey
    fcCwithoutbait=Stats.mean(Cs)/Stats.mean(Cns) #empty; no bait and prey

    FIwrtnullbait=fcwithB/fcwithoutBait
    FIwrtnullprey=fcwithB/fcCwithbait

    stdFC=Stats.pstdev((FIwrtnullbait,FIwrtnullprey))
    cvFC=stdFC/Stats.mean((FIwrtnullbait,FIwrtnullprey))
    # FIwrtnullBaitnullPrey=fcwithB/fcCwithoutbait

    minFC=min(FIwrtnullbait,FIwrtnullprey)


## get the tagging of the each interactio
    if minFC>threshold:
        tag="positive"
    else:
        if (fcwithoutBait/fcCwithoutbait)>threshold:
            tag="aspecific"
        else:
            tag="negative"
    # else:
    #     tag="negative"


    return str(round(fcwithB,2)),str(round(fcwithoutBait,2)),str(round(FIwrtnullprey,2)),\
           str(round(FIwrtnullbait,2)),str(round(minFC,2)),str(round(stdFC,2)),str(round(cvFC,2)),tag
