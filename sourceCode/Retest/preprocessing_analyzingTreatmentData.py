__author__ = 'surya'

from GeneralMethods import DictionaryMethods
from MathsStats import Stats

## get Screening intensity from file by removing header and other lines

def parseRawFileAsList(fileName):
    outList=[]
    with open(fileName) as openedFile:
        next(openedFile)#escaping header
        next(openedFile)#escaping col number
        for line in openedFile:
            splits=line.strip().split("\t")
            line2append="\t".join(splits[1:])#escaping row notations
            outList.append(line2append)
            if splits[0]=="H":
                break
    # print len(outList)
    return outList

## merge the with and without bait files

def mergeBaitFiles(Analysis2retestFile,folder_path):
    dic={}
    with open(Analysis2retestFile) as connectFile:
        next(connectFile)
        for line in connectFile:
            splits = line.split("\t")
            WithBaitFile = splits[0].strip()
            if WithBaitFile not in dic:
                dic[WithBaitFile] = []
                WithoutBaitFile = splits[-3].strip()
                if WithBaitFile!=WithoutBaitFile:
                    BaitList = parseRawFileAsList(folder_path+ "/" +WithBaitFile)  # whole line
                    WOTBaitList = parseRawFileAsList(folder_path+ "/" +WithoutBaitFile)  # whole line
                    for index in range(len(WOTBaitList)):
                        dic[WithBaitFile].append(BaitList[index]+"\t"+WOTBaitList[index])
                else: ## in case the controls are in the same file
                    start=int(splits[-2].strip())-1
                    end=int(splits[-1].strip())
                    fileList=parseRawFileAsList(folder_path+ "/" +WithBaitFile)
                    wotBaitLines=fileList[start:end]+fileList[start:end]
                    for index in range(len(fileList)):
                        dic[WithBaitFile].append(fileList[index] + "\t" + wotBaitLines[index])
                if len(dic[WithBaitFile])!=8:
                    print "one of the file ",WithBaitFile, WithoutBaitFile,"have less number of rows check"
    return dic

## merge control,analysis and retest files together

def mergeFilesBaitNdWotBaitFiles(controlFormat,AnalysiOutputFile,Analysis2retestFile,folder_path,arrangement,
                                 WotTreatmentFile,TreatmentFile,SummaryFile,threshold):
    mainList=[]
    treatmentFile=open(folder_path+"/"+TreatmentFile,"w")
    lnT = "FileNames\tUniqueName\tEntrenzNames\tNS\tNS\tNS\tST\tST\tST\tNSB+\tNSB+\tNSB+\tSB+T\tSB+T\tSB+T" \
          "\tFCwithoutBait\tFCwithBait\tFIwrtPreyNull\tFIwrtBaitNull\tminFI\tstdFI\tcvFI\ttag\twellName\ttype\n"

    treatmentFile.writelines(lnT)
    wottreatmentFile=open(folder_path+"/"+WotTreatmentFile,"w")
    ln = "FileNames\tUniqueName\tEntrenzNames\tNS\tNS\tNS\tS\tS\tS\tNSB+\tNSB+\tNSB+\tSB+\tSB+\tSB+" \
       "\tFCwithoutBait\tFCwithBait\tFIwrtPreyNull\tFIwrtBaitNull\tminFI\tstdFI\tcvFI\ttag\twellName\ttype\n"
    wottreatmentFile.write(ln)
    summaryFile=open(folder_path+"/"+SummaryFile,"w")
    lnS = "FileNames\tUniqueName\tEntrenzNames\tNS\tNS\tNS\tS\tS\tS\tST\tST\tST" \
          "\tNSB+\tNSB+\tNSB+\tSB+\tSB+\tSB+\tSB+T\tSB+T\tSB+T" \
          "\tminFI\tTminFI\ttag\ttagT\twellName\ttype\n"
    summaryFile.write(lnS)

    # wellName="A,B,C,D,E,F,G,H".split(",")

    # connectorDic=DictionaryMethods.createDic(Analysis2retestFile,0,[1,2,3],header=True) ## filename:[type,start,end]
    analysisDic=DictionaryMethods.createDic(AnalysiOutputFile,0,[1,2],header=True)#uniqueName:[entrezname,WellName]
    uniqueList=DictionaryMethods.createList(AnalysiOutputFile,0,header=True)#uniqueName
    controlList=DictionaryMethods.createList(controlFormat,0,header=True)#uniqueName
    controlfile=DictionaryMethods.createDic(controlFormat,0,[1,2],header=True)#uniqueName:[Names,wellName]
    ## merge bait and without bait file
    File2MergedLinesDic=mergeBaitFiles(Analysis2retestFile, folder_path)# merge both file with "with bait and wot bait" format
    # print File2MergedLinesDic
    arrangementWithB = arrangement.replace("S","SB+")  # "N,NS,NS,NS,S,S,S,ST,ST,ST,N,N"
    arrangement_new=arrangementWithB+","+arrangement
    NewArrang=arrangement_new.replace(",","\t")


    connectorDic={}
    ## get controls
    emptybaitcontrol=""
    with open(Analysis2retestFile) as connectFile:
        next(connectFile)
        for line in connectFile:
            splits=line.strip().split("\t")
            eachfile=splits[0].strip()
            type=splits[1].strip()
            wotBaitFile=splits[-3].strip()
            if type == "control":
                lineStart = int(splits[4].strip()) - 1
                lineEnd = int(splits[5].strip())
                start = 0
                for i in range(lineStart,lineEnd):
                    eachlinec=File2MergedLinesDic[eachfile][i]
                    # print eachlinec
                    if controlfile[controlList[start]][0] == "empty":
                        emptybaitcontrol = eachlinec
                        type = "empty"
                    else:
                        type = "control"
                    nonTreatmentList, TreatmentList,ns,s,st,nsb,sb,sbt = calculateTreatedFI(eachlinec, NewArrang, emptybaitcontrol,threshold)
                    ln = [wotBaitFile+"_"+eachfile, controlList[start], controlfile[controlList[start]][0]]+ns+s+nsb+sb+nonTreatmentList+\
                         [controlfile[controlList[start]][1], type]
                    wottreatmentFile.write("\t".join(ln)+"\n")
                    lnT = [wotBaitFile+"_"+eachfile, controlList[start], controlfile[controlList[start]][0]]+ns+st+nsb+sbt+TreatmentList+\
                          [controlfile[controlList[start]][1], type]
                    treatmentFile.write("\t".join(lnT)+"\n")
                    lnS = [wotBaitFile+"_"+eachfile, controlList[start], controlfile[controlList[start]][0]] +ns+s+st+nsb+sb+sbt+ \
                          [nonTreatmentList[4],TreatmentList[4],
                            nonTreatmentList[7],TreatmentList[7]]+ [controlfile[controlList[start]][1], type]
                    summaryFile.write("\t".join(lnS) + "\n")
                    lntoadd= [wotBaitFile + "_" + eachfile, controlList[start],
                         controlfile[controlList[start]][0]] + ns + s + st + nsb + sb + sbt + \
                        [nonTreatmentList[0],TreatmentList[0],nonTreatmentList[1],TreatmentList[1],nonTreatmentList[4], TreatmentList[4],
                         nonTreatmentList[7], TreatmentList[7]] + [controlfile[controlList[start]][1], type]
                    toadd="\t".join(lntoadd)
                    mainList.append(toadd)
                    start += 1
            else:
                connectorDic[eachfile] = splits[1:]

## do it for analysis as well
    for eachfile in connectorDic:
        type = connectorDic[eachfile][0]
        wotBaitFileName = connectorDic[eachfile][-3]
        if type == "analysis":
            astart = int(connectorDic[eachfile][1]) - 1
            # print(astart)
            print eachfile,wotBaitFileName
            # print connectorDic[eachfile]
            lineStart = int(connectorDic[eachfile][3]) - 1
            lineEnd = int(connectorDic[eachfile][4])
            # print(len(uniqueList))
            for i in range(lineStart, lineEnd):
                eachline = File2MergedLinesDic[eachfile][i]
                nonTreatmentList, TreatmentList, ns, s, st, nsb, sb, sbt = calculateTreatedFI(eachline, NewArrang,
                                                                                                emptybaitcontrol,threshold)
                ln = [wotBaitFileName+"_"+eachfile, uniqueList[astart],analysisDic[uniqueList[astart]][0]] + ns + s + nsb + sb + \
                                                        nonTreatmentList+ [analysisDic[uniqueList[astart]][1],type]
                wottreatmentFile.write("\t".join(ln) + "\n")
                lnT = [wotBaitFileName+"_"+eachfile, uniqueList[astart],analysisDic[uniqueList[astart]][0]] + ns + st + nsb + sbt + \
                                                        TreatmentList+ [analysisDic[uniqueList[astart]][1], type]
                treatmentFile.write("\t".join(lnT) + "\n")
                lnS=[wotBaitFileName+"_"+eachfile, uniqueList[astart],analysisDic[uniqueList[astart]][0]]+ns+s+st+nsb+sb+sbt+\
                    [nonTreatmentList[4],TreatmentList[4],nonTreatmentList[7],TreatmentList[7]]+\
                    [analysisDic[uniqueList[astart]][1], type]
                summaryFile.write("\t".join(lnS) + "\n")
                lntoadd=[wotBaitFileName+"_"+eachfile, uniqueList[astart],analysisDic[uniqueList[astart]][0]]+ns+s+st+nsb+sb+sbt+\
                    [nonTreatmentList[0], TreatmentList[0], nonTreatmentList[1], TreatmentList[1],
                     nonTreatmentList[4],TreatmentList[4],nonTreatmentList[7],TreatmentList[7]]+\
                    [analysisDic[uniqueList[astart]][1], type]

                toadd = "\t".join(lntoadd)
                mainList.append(toadd)
                astart+=1
    wottreatmentFile.close()
    treatmentFile.close()
    summaryFile.close()
    return mainList

## calculate the FI

def calculateTreatedFI(line,arragement,controlLine,threshold):
    # print line
    # print controlLine
    arragementlist=arragement.split("\t")
    # print arragement
    controlList=controlLine.split("\t")
    valuelist=line.split("\t")
    ns,s,nsb,sb,sbt,st=[],[],[],[],[],[]
    nsP,sP,nsbP,sbP,sbtP,stP=[],[],[],[],[],[]
    Cns,Cs,Cnsb,Csb=[],[],[],[]
    for i in range(len(arragementlist)):
        if arragementlist[i]=="NS":
            ns.append(float(valuelist[i]))
            nsP.append(valuelist[i])
            Cns.append(float(controlList[i]))
        elif arragementlist[i]=="S":
            s.append(float(valuelist[i]))
            sP.append(valuelist[i])
            Cs.append(float(controlList[i]))
        elif arragementlist[i]=="NSB+":
            nsb.append(float(valuelist[i]))
            nsbP.append(valuelist[i])
            Cnsb.append(float(controlList[i]))
        elif arragementlist[i]=="SB+":
            sb.append(float(valuelist[i]))
            sbP.append(valuelist[i])
            Csb.append(float(controlList[i]))
        elif arragementlist[i]=="SB+T":
            sbt.append(float(valuelist[i]))
            sbtP.append(valuelist[i])
        elif arragementlist[i]=="ST":
            st.append(float(valuelist[i]))
            stP.append(valuelist[i])
        elif arragementlist[i]=="X":
            pass
        else:
            print(arragementlist[i]+" not found....")

    fcwithB=Stats.mean(sb)/Stats.mean(nsb)
    fcwithBT=Stats.mean(sbt)/Stats.mean(nsb) #treatment
    fcwithoutBait=Stats.mean(s)/Stats.mean(ns)
    fcwithoutBaitT=Stats.mean(st)/Stats.mean(ns)
    fcCwithbait=Stats.mean(Csb)/Stats.mean(Cnsb)
    fcCwithoutbait=Stats.mean(Cs)/Stats.mean(Cns)

    FIwrtnullbait=fcwithB/fcwithoutBait
    FIwrtnullprey=fcwithB/fcCwithbait
    ## for treatment pair
    FIwrtnullbaitT=fcwithBT/fcwithoutBaitT#treatment
    FIwrtnullpreyT=fcwithBT/fcCwithbait#treatment

    stdFC=Stats.pstdev((FIwrtnullbait,FIwrtnullprey))
    cvFC=stdFC/Stats.mean((FIwrtnullbait,FIwrtnullprey))
    minFC=min(FIwrtnullbait,FIwrtnullprey)
    #for treatment
    stdFCT=Stats.pstdev((FIwrtnullbaitT,FIwrtnullpreyT))
    cvFCT=stdFCT/Stats.mean((FIwrtnullbaitT,FIwrtnullpreyT))
    minFCT = min(FIwrtnullbaitT, FIwrtnullpreyT)

## get the tagging of the each interactio
    tag=""
    if minFC>threshold:
        tag="positive"
    else:
        if (fcwithoutBait/fcCwithoutbait)>threshold:
            tag="aspecific"
        else:
            tag="negative"
    ## with treatment
    tagT=""
    if minFCT>threshold:
        tagT="positive"
    else:
        if (fcwithoutBaitT/fcCwithoutbait)>threshold:
            tagT="aspecific"
        else:
            tagT="negative"
    nonTreatmentList=[str(round(fcwithoutBait,2)),str(round(fcwithB,2)),str(round(FIwrtnullprey,2)),str(round(FIwrtnullbait,2)),\
           str(round(minFC,2)),str(round(stdFC,2)),str(round(cvFC,2)),tag]
    TreatmentList=[str(round(fcwithoutBaitT,2)),str(round(fcwithBT,2)),str(round(FIwrtnullpreyT,2)),str(round(FIwrtnullbaitT,2)),\
           str(round(minFCT,2)),str(round(stdFCT,2)),str(round(cvFCT,2)),tagT]
    return nonTreatmentList,TreatmentList,nsP,sP,stP,nsbP,sbP,sbtP
