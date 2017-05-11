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

def mergeFilesForKissData(controlFormat,AnalysiOutputFile,Analysis2retestFile,folder_path,arrangement,threshold,outputfile):
    arrangement_new=arrangement.replace(",","\t")
    mergedout=open(folder_path+"/"+outputfile,"w")
    mainList=[]
    ln=["FileNAme\tUniqueName\tEntrenzNames\t",arrangement_new,"\tFCPreyNull\tFCBaitNull\tminFI\ttag\twellName\ttype\n"]
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
                    FIwithBait,FIwithoutBait,minFI,tag=calculateFI(eachlinec,arrangement,emptybaitcontrol,threshold)
                    ln=[eachfile,controlList[start],controlfile[controlList[start]][0],eachlinec.strip(),
                        FIwithoutBait,FIwithBait,minFI,tag,controlfile[controlList[start]][1],type]
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
                    FIwithBait,FIwithoutBait,minFI,tag=calculateFI(eachline,arrangement,emptybaitcontrol,threshold)

                    ln = [eachfile,uniqueList[astart],analysisDic[uniqueList[astart]][0], eachline.strip(),
                          FIwithoutBait, FIwithBait, minFI, tag,analysisDic[uniqueList[astart]][1],"analysis"]
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
    WotB,B=[],[]
    CWotB,CB=[],[]
    for i in range(len(arragementlist)):
        if arragementlist[i]=="B-":
            WotB.append(float(valuelist[i]))
            CWotB.append(float(controlList[i]))
        elif arragementlist[i]=="B+":
            B.append(float(valuelist[i]))
            CB.append(float(controlList[i]))
        else:
            print(arragementlist[i]+" not found....")

    fcBaitNull=Stats.mean(B)/Stats.mean(WotB)#without bait
    fcPreyNull=Stats.mean(B)/Stats.mean(CB) #without prey
    fcPreyNullBaitNull=Stats.mean(WotB)/Stats.mean(CWotB)
    minFC=min(fcBaitNull,fcPreyNull)


## get the tagging of the each interactio
    tag=""
    # if fcwithB>9:
    if minFC>threshold:
        tag="positive"
    else:
        if fcPreyNullBaitNull>threshold:
            tag="aspecific"
        else:
            tag="negative"
    # else:
    #     tag="negative"


    return str(round(fcPreyNull,2)),str(round(fcBaitNull,2)),str(round(minFC,2)),tag
