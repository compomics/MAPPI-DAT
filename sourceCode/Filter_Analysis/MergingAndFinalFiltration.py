__author__ = 'surya'

from Filter_Analysis import CalculatingPositives
import math
from GeneralMethods import DictionaryMethods

def separatecol_row(AllFilePath,cutOff,geneCount,nsrep,srep):
    count=[0,0,0] # NA,control+,SD+
    end=srep+nsrep+6
    start=6
    writes=open(AllFilePath+"_SelectedAnalyzed.txt","w")
    # writes=open(file+"_RankProd_All.txt","w")
    IntDic=DictionaryMethods.createDic(AllFilePath+"_IntegralIntensity.txt",2,range(start,end),header=True)
    ResiDic=DictionaryMethods.createDic(AllFilePath+"_Residuals.txt",2,range(start,end),header=True)
    PCDic=DictionaryMethods.createDic(AllFilePath+"_Particle_Count.txt",2,range(start,end),header=True)
    c=0
    if geneCount!=0:
        countCheck=True
    else:
        countCheck=False
    ln = ["SourcePlate\tWell\tBlock1\tBlock2\tBlock3\tBlock4\tRow\tCol\tType\tunique_name\tEntrenzID\tARTNumber\tFDR\tLog2FC\tQ-value\tP-Value\tFoldChange"]+\
         ["\tInt_NS"]*(nsrep)+["\tInt_S"]*(srep)+["\tResid_NS"]*(nsrep)+["\tResid_S"]*(srep)+\
                        ["\tPC_NS"]*(nsrep)+["\tPC_S"]*(srep)+["\n"]
    writes.writelines(ln)
    with open(AllFilePath+"_AllAnalyzed.txt") as filename:
            next(filename)
            for lines in filename:
                added=False
                splits=lines.split("\t")
                first=splits[0].strip().split("_")
                uniqueName=first[8].strip()
                # print splits[4].strip()
                # print lines.strip()
                # print float(splits[4].strip("" ))

                qval=float(splits[3].strip("" ))
                ln=[first[11].strip("\" "),"\t",first[0].strip("\""),"\t",first[1].strip(),"\t",first[2].strip(),"\t",first[3].strip(),"\t",first[4].strip(),"\t",
                first[5].strip(),"\t",first[6].strip(),"\t",first[7].strip(),"\t",first[8].strip(),"\t",first[9].strip(),"\t",first[10].strip("\""),"\t",splits[1].strip(),"\t",
                str(float(splits[2].strip())),"\t",splits[3].strip(),"\t",splits[4].strip(),"\t",str(math.pow(2,float(splits[2].strip()))),"\t",
                "\t".join(IntDic[uniqueName]),"\t","\t".join(ResiDic[uniqueName]),"\t","\t".join(PCDic[uniqueName]),"\n"]
                c+=1
#                print ln
                if countCheck:
                    if c<=geneCount:
                        writes.writelines(ln)
                        added=True
                else:
                    if qval<=float(cutOff):
                        writes.writelines(ln)
                        added=True
                if added:
                    if first[7].strip() in ["NA","NAc+","NAsd+"]:
                        count[0]+=1
                    elif first[7].strip()=="control+":
                        count[1]+=1
                    elif first[7].strip()=="SD+control":
                        count[2]+=1
    writes.close()
    return count,AllFilePath+"_SelectedAnalyzed.txt"

#FinalFilt("C:/Users/surya/Desktop/ProjectData/data/data8/dataProcessing/8628/T1-41/T1-41")

# create a main file in the main


def ChangeFourToOneWell(linkFiles,SoftwareHeaderNum,nsreplicate,sreplicate):
    plateNumber=0
    outputfile=open(linkFiles+"/AllPlateNewHits_ForSoftwareInput.txt","a")
    if SoftwareHeaderNum==0:
        linetowrite=(["SourcePlate\tWell\tBlock1\tRow\tCol\tType\tunique_name\tEntrenzID\tARTNumber\tFDR\tLog2FC\tQ-Value\tP-Value","\tFoldChange"]+["\t",
                        "Non-Stim"]*(nsreplicate)+["\t","Stim"]*(sreplicate)+["\tNS_Mad\tS_Mad"]+["\t","PC_NS"]*(nsreplicate)+["\t","PC_S"]*(sreplicate)+["\n"])
        outputfile.writelines(linetowrite)
    with open(linkFiles+"/Analyzed_NewHits.txt")as file:
        next(file)
        for line in file:
            splits=line.split("\t")
            plateNumber=len(splits[0].split(","))
            plates=splits[0].split(",")
            toAdd="\t".join(splits[6:len(splits)])
#            toAdd=splits[6].strip()+"\t"+splits[7].strip()+"\t"+splits[8].strip()+"\t"+splits[9].strip()+"\t"+splits[10].strip()+"\t"+splits[11].strip()+"\t"+splits[12].strip()+"\t"+\
#                   splits[13].strip()+"\t"+splits[14].strip()+"\t"+splits[15].strip()+"\t"+splits[16].strip()+"\t"+splits[17].strip()+"\t"+splits[18].strip()+"\t"+splits[19].strip()+"\t"+\
#                   splits[20].strip()+"\t"+splits[21].strip()+"\t"+splits[22].strip()+"\t"+splits[23].strip()+"\t"+splits[24].strip()+"\t"+splits[25].strip()+"\t"+splits[26].strip()+"\n"
            for plate in plates:
                id1=plate.strip()+"\tW1"+"\t"+splits[2].strip()
                outputfile.writelines([id1+"\t"+toAdd])
                id2=plate.strip()+"\tW2"+"\t"+splits[3].strip()
                outputfile.writelines([id2,"\t",toAdd])
                id3=plate.strip()+"\tW3"+"\t"+splits[4].strip()
                outputfile.writelines([id3,"\t",toAdd])
                id4=plate.strip()+"\tW4"+"\t"+splits[5].strip()
                outputfile.writelines([id4,"\t",toAdd])
    outputfile.close()
    SoftwareHeaderNum+=1
    return SoftwareHeaderNum

#################################################################################################################################
## create software input file

def CreateSoftwareInputFile(AllFilePath):
    plateNumber=0
    outputfile=open(AllFilePath+"_Analyzed_ForSoftwareInput.txt","w")
    AnalyzedOutputDic=DictionaryMethods.CreateDicWithAllColAsVal(AllFilePath+"_SelectedAnalyzed.txt",9,header=False)
    print "total analyzed are ", len(AnalyzedOutputDic)
    for line in open(AllFilePath+".txt"):
        splits=line.split("\t")
        if splits[0].strip("\" ")=="UniqueId":
                lnlist=splits[5:7]+splits[8:11]+AnalyzedOutputDic["unique_name"][8:]
                ln="\t".join(lnlist)
                outputfile.write(ln+"\n")
        else:
            uniqName=splits[2].strip("\" ")
            if uniqName in AnalyzedOutputDic:
                lnlist=splits[5:7]+splits[8:11]+AnalyzedOutputDic[uniqName][8:]
                ln="\t".join(lnlist)
                outputfile.write(ln+"\n")
    outputfile.close()


## create a new script which uses filtration of Mad file instead

def FinalFilt(All,lin,plateName,filcontrol,fil_opt,PCdic,PCpresent,pcthreshold,nsrep,srep):
    writeMerged=open(lin+"/AnalyzedResultMerged.txt",'w')
    writeSD=open(lin+"/Analyzed_SD_And_Control.txt",'w')
    writesF=open(lin+"/Analyzed_NewHits.txt",'w')
    lnMerged=[]
    filtration="-"
    PC_values=[]
    plate_name=""
    for lines in open(All):
        if lines!="\n":
            splits=lines.split("\t")
            spID=splits[0].strip()+"_"+splits[1].strip()+"_"+splits[2].strip()+"_"+splits[3].strip()+"_"+splits[4].strip()+"_"+splits[5].strip()+"_"+splits[6].strip()
#            spID="_".join(splits)
            if splits[0]=="Well":
                ln=["PlateName","\t",lines.strip()]+["\t","PC_NS"]*(nsrep)+["\t","PC_S"]*(srep)+["\tthreshold_type\n"]
                plate_name="PlateName"
                filtration="threshold_type"
                PC_values=["\t","PC_NS"]*(nsrep)+["\t","PC_S"]*(srep)

                ## write all the files
                writesF.writelines(ln)
                writeSD.writelines(ln)
#                writeMerged.writelines(lnMerged)
            elif splits[7] in ["NA","NAc+","NAsd+"]:
                if fil_opt and PCpresent:
                    if spID not in filcontrol:
                        if spID in pcthreshold:
                            ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","New","\n"] ## not in quartile as well PC filtration
                            writesF.writelines(ln)
                            filtration="-"
#                            print(PCdic[spID])
                        else:
                            ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","PC threshold","\n"] ## filtered through PC only
                            writesF.writelines(ln)
                            filtration="PC threshold"
#                            print(PCdic[spID])
                    elif spID not in pcthreshold:
                        ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","PC and Quartile threshold","\n"] ## if marked for both quartile as well PC filtration
                        writesF.writelines(ln)
#                        print(PCdic[spID])
                        filtration="PC and Quartile threshold"
                    else:
                        ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","Quartile threshold","\n"] ## filtered only by quartile filtration
                        writesF.writelines(ln)
#                        print(PCdic[spID])
                        filtration="Quartile threshold"
                elif fil_opt and not PCpresent:
                    if spID not in filcontrol:
                            ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","New","\n"]
                            writesF.writelines(ln)
                            filtration="-"
#                            print(PCdic[spID])
                    else:
                        ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","Quartile threshold","\n"]
                        writesF.writelines(ln)
                        filtration="Quartile threshold"
#                        print(PCdic[spID])
                elif not fil_opt and PCpresent:
                        if spID in pcthreshold:
                            ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","New","\n"]
                            writesF.writelines(ln)
                            filtration="-"
#                            print(PCdic[spID])
                        else:
                            ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","PC threshold","\n"]
                            writesF.writelines(ln)
#                            print(PCdic[spID])
                            filtration="PC threshold"
                else:
                        ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","New","\n"]
#                        print(PCdic[spID])
                        writesF.writelines(ln)
                PC_values=PCdic[spID]
                plate_name=plateName
                                ## to get the different arrangement of the columns for the MergedFile
            else:
                ln=[plateName,"\t",lines.strip(),"\t",PCdic[spID],"\t","Control","\n"]
                writeSD.writelines(ln)
                filtration="Control"
                PC_values=PCdic[spID]
                plate_name=plateName
#                writeMerged.writelines(ln)
            ##############################################################################
            ## creating a merged file with different arrangement of the columns
            lnMerged=[plate_name]
            for eachindex in [1,2,3,4,5,6,7]:
                lnMerged+=["\t",splits[eachindex].strip()]
            lnMerged+=["\t",filtration]
            for eachindex_1 in [8,10,0,9]:
                lnMerged+=["\t",splits[eachindex_1].strip()]
            for eachindex_2 in range(13,len(splits)-2):
                lnMerged+=["\t",splits[eachindex_2].strip()]
            if PC_values[0]!="\t":
                lnMerged+=["\t"]
            lnMerged+=PC_values
            lnMerged+=["\t",splits[len(splits)-2].strip(),"\t",splits[len(splits)-1].strip(),"\n"]## to add the mad for s and ns
#            print(lnMerged)
            writeMerged.writelines(lnMerged)

    writesF.close()
    writeSD.close()
    writeMerged.close()
    return All


#########################################################################################################################

######################## if asked than apply filtration for quartile and PC filtration and separate column ##################################
## create a new script which uses filtration of Mad file instead

def ApplyFiltrationAddRawData(AllFilePath,cutOff,geneCount,nsrep,srep,quartilOutlierList,PCfilteredOutliersList):
    Poscount=[0,0,0] # NA,control+,SD+
    end=srep+nsrep+6
    start=6
    writes=open(AllFilePath+"_SelectedAnalyzed.txt","w")
    # writes=open(file+"_RankProd_All.txt","w")
    IntDic=DictionaryMethods.createDic(AllFilePath+"_IntegralIntensity.txt",2,range(start,end),header=True)
    ResiDic=DictionaryMethods.createDic(AllFilePath+"_Residuals.txt",2,range(start,end),header=True)
    PCDic=DictionaryMethods.createDic(AllFilePath+"_Particle_Count.txt",2,range(start,end),header=True)
    c=0
    if geneCount!=0:
        countCheck=True
    else:
        countCheck=False
    ln = ["SourcePlate\tWell\tBlock1\tBlock2\tBlock3\tBlock4\tRow\tCol\tType\tunique_name\tEntrenzID\tARTNumber\tLog2FC\tQ-value\tP-Value\tFoldChange"]+\
         ["\tInt_NS"]*(nsrep)+["\tInt_S"]*(srep)+["\tResid_NS"]*(nsrep)+["\tResid_S"]*(srep)+\
                        ["\tPC_NS"]*(nsrep)+["\tPC_S"]*(srep)+["\tThresholdType\n"]
    writes.writelines(ln)
    with open(AllFilePath+"_AllAnalyzed.txt") as filename:
            next(filename)
            for lines in filename:
                added=False
                splits=lines.split("\t")
                first=splits[0].strip().split("_")
                uniqueName=first[8].strip()
                thresholdType=checkQuartilePCFil(quartilOutlierList,PCfilteredOutliersList,uniqueName)
                qval=float(splits[2].strip("" ))
                ln=[first[11].strip("\" "),"\t",first[0].strip("\""),"\t",first[1].strip(),"\t",first[2].strip(),"\t",first[3].strip(),"\t",first[4].strip(),"\t",
                first[5].strip(),"\t",first[6].strip(),"\t",first[7].strip(),"\t",first[8].strip(),"\t",first[9].strip(),"\t",first[10].strip("\""),"\t",str(splits[1].strip()),"\t",
                str(splits[2].strip()),"\t",splits[3].strip(),"\t",str(math.pow(2,float(splits[1].strip()))),"\t",
                "\t".join(IntDic[uniqueName]),"\t","\t".join(ResiDic[uniqueName]),"\t","\t".join(PCDic[uniqueName]),"\t",str(thresholdType),"\n"]
                c+=1
#                print ln
                if countCheck:
                    if c<=geneCount:
                        writes.writelines(ln)
                        added=True
                else:
                    if qval<=float(cutOff):
                        writes.writelines(ln)
                        added=True
                if added:
                    if first[7].strip() in ["NA","NAc+","NAsd+"]:
                        Poscount[0]+=1
                    elif first[7].strip()=="control+":
                        Poscount[1]+=1
                    elif first[7].strip()=="SD+control":
                        Poscount[2]+=1
    writes.close()
    return Poscount,AllFilePath+"_SelectedAnalyzed.txt"

#######################################################################################################################

def checkQuartilePCFil(quartilOutlierList,PCfilteredOutliers,uniqueName):
    thresholdType=""
    if uniqueName in PCfilteredOutliers and uniqueName in quartilOutlierList:
        thresholdType="PC and Quartile Outlier"
    elif uniqueName in PCfilteredOutliers and uniqueName not in quartilOutlierList:
        thresholdType="PC Outlier"
    elif uniqueName not in PCfilteredOutliers and uniqueName in quartilOutlierList:
        thresholdType="Quartile Outlier"
    else:
        thresholdType="New"
    return thresholdType

#######################################################################################################################

## merging all SD file and all filtered output the SDs from the

def merge(file,wellNum,sdfile):
    sd=open(sdfile,"a")
    for line in open(file):
        splits=line.split("\t")
        if splits[0]=="PlateName" and wellNum ==0 and line!="\n":
            sd.write(line)
        elif splits[0]!="PlateName" and line !="\n":
            sd.write(line)
    sd.close()




def MergingAllPlatesToOneOutput(wellNum,sdfile,allfile,lin,merged):
    merge(lin+"/Analyzed_SD_And_Control.txt",wellNum,sdfile)
    merge(lin+"/Analyzed_NewHits.txt",wellNum,allfile)
    merge(lin+"/AnalyzedResultMerged.txt",wellNum,merged)
    wellNum+=1
    return wellNum


#############################################################
## merging all statistics file from quartile
def MergingQuartileFiles(lin,MergeFile):
    merge_Stats=open(MergeFile,"a")
    for line in open(lin+"/AllRepTogether_Statistics.txt"):
        merge_Stats.write(line)
    merge_Stats.close()


# #############################################################################################