_author_ ="surya"


""" this files contain mostly all the methods needed to process the file from XML to text file; assigning the protein
name to each interaction; merging all the files based on the different quantification values
"""

#################### Folder and file information ####################################
################ create a dic for linkage file containing the bait, file and annotation information  ####################

# pfile: linkageFile

def linkageDic(pFile):
    linkagedic={}
    plate2subfolder={}
    plate_tfileDic={}
    bait={}
    with open(pFile) as file:
        next(file)
        for lines in file:
            if lines.strip():
#                print lines
                splits =lines.split("\t")
                if splits[0].strip() not in bait:
                    bait[splits[0].strip()]=splits[2].split(",")
                else:
                    bait[splits[0].strip()]+=splits[2].split(",")
                linkagedic[splits[1].strip()]=[splits[0].strip(),splits[3].strip(),[]] ## filefolder=bait,proteinFile
                for plate in splits[2].split(","):
                    plate_tfileDic[plate]=splits[3].strip() # path to T file
                    linkagedic[splits[1].strip()][2].append(plate.strip("\""))
                    plate2subfolder[plate.strip("\"")]=splits[1].strip() # path to subfolder
                    # print fdic ## (plate:subfolder)
                    # print dic ## {subfolder: [bait,proteinfile,[plate1,plate2....]]}
    return linkagedic, plate2subfolder,plate_tfileDic,bait

## output: subFold bait    proteinannotatio [file1,file2...]

## create a main folder data_processing and than folder for each bait

def FolderCreationOnlyBait(link,pathList):
    #create folder for each of these keys
    path = link +"/MAPPIDAT_OutPut"

#    print path
    import os
    if not os.path.isdir(path):
        os.makedirs(path)
    for bait in pathList:
        baitpath=path+"/"+bait
        if not os.path.isdir(baitpath):
            os.makedirs(baitpath)
            dirList=[baitpath+"/Processing",baitpath+"/Analysis"]
            for each in dirList:
                if not os.path.isdir(each):
                        os.makedirs(each)
        OnlyControl=open(path+"/"+bait+"/Processing/AllPlatesOnlyControl.txt",'w')
        withoutControl=open(path+"/"+bait+"/Processing/AllPlatesWithoutControl.txt",'w')
        All=open(path+"/"+bait+"/Processing/AllPlatesWithControl.txt",'w')
        OnlyControl.write("UniqueId\ttype\tuniqueName\tEntrenzName\tPlateId\tSourcePlate\tSourceWell\tID\tBlock\tSpotRow\tSpotColumn\t"
                      "ParticleCount\tMeanArea_um2\tAreaFraction\tMeanGrayValueMean\tMeanIntegralIntensity\tGrayValueMean\tIntegralIntensity_um2\n")
        withoutControl.write("UniqueId\ttype\tuniqueName\tEntrenzName\tPlateId\tSourcePlate\tSourceWell\tID\tBlock\tSpotRow\tSpotColumn\t"
                      "ParticleCount\tMeanArea_um2\tAreaFraction\tMeanGrayValueMean\tMeanIntegralIntensity\tGrayValueMean\tIntegralIntensity_um2\n")
        All.write("UniqueId\ttype\tuniqueName\tEntrenzName\tPlateId\tSourcePlate\tSourceWell\tID\tBlock\tSpotRow\tSpotColumn\t"
                      "ParticleCount\tMeanArea_um2\tAreaFraction\tMeanGrayValueMean\tMeanIntegralIntensity\tGrayValueMean\tIntegralIntensity_um2\n")

    return path




### create a separate working space containing each bait in different folder

def FolderCreation(link,linkdic):
    #create folder for each of these keys
    path = link + "/" + "dataProcessing"
#    print path
    import os
    if not os.path.isdir(path):
        os.makedirs(path)
    for bait in linkdic:
        if not os.path.isdir(path+"\\"+linkdic[bait][0]+"\\"+bait):
                os.makedirs(path+"\\"+linkdic[bait][0]+"\\"+bait)
        open(path+"/"+linkdic[bait][0]+"/AllPlatesNewHits.txt",'w')
        open(path+"/"+linkdic[bait][0]+"/AllPlate_SdConAsp.txt",'w')
        open(path+"/"+linkdic[bait][0]+"/AllPlatesCon_New_MergedTogether.txt",'w')
        open(path+"/"+linkdic[bait][0]+"/QuartileThresholdForEachPlate.txt",'w')
        open(path+"/"+linkdic[bait][0]+"/AllPlateNewHits_ForSoftwareInput.txt",'w')
#        SoftwareInput.write("SourcePlate\tWell\tBlock1\tRow\tCol\tType\ttunique_name\tEntrenzID\tARTNumber\tRP/Rsum\tFC:(class1/class2)\tpfp\tP-Value\tFoldChange\tNS\tStim\tStim\tStim\tNA_mad\tS_mad\tPC_NS\tPC_S\tPC_S\tPC_S")

    return path

#### add protein name to each bait prey interaction and label them if they are A-specific or specific ###############
#####################################################################################################################

## create a dictionary containing each block+row+column and id and others as value
def proteinDic(file): ## file: each protein annotation file
    type=15
    impid=10
    name=12
    artname=8
    PDic={}
    with open(file) as ProteinFile:
        next(ProteinFile)
        for pline in ProteinFile:
            if pline !="\n":
                psplits=pline.split("\t")
                spID=psplits[1].strip()+"_"+psplits[2].strip()+"_"+psplits[3].strip()+"_"+psplits[4].strip()+"_"+psplits[5].strip()+"_"+psplits[6].strip()+"_"+psplits[7].strip()
                if psplits[2].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip() not in PDic:
                    PDic[psplits[2].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip()]=[spID,psplits[type].strip(),psplits[impid].strip(),psplits[name].strip(),psplits[artname].strip(),pline.strip()]
                if psplits[3].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip() not in PDic:
                    PDic[psplits[3].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip()]=[spID,psplits[type].strip(),psplits[impid].strip(),psplits[name].strip(),psplits[artname].strip(),pline.strip()]
                if psplits[4].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip() not in PDic:
                    PDic[psplits[4].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip()]=[spID,psplits[type].strip(),psplits[impid].strip(),psplits[name].strip(),psplits[artname].strip(),pline.strip()]
                if psplits[5].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip() not in PDic:
                    PDic[psplits[5].strip()+"\t"+psplits[6].strip()+"\t"+psplits[7].strip()]=[spID,psplits[type].strip(),psplits[impid].strip(),psplits[name].strip(),psplits[artname].strip(),pline.strip()]
    return PDic



## create an id to type of interaction dic:
def pID2Type(file,Apecific_file): ## each protein annotation file for respective plates as mentioned in the linkageFile
    type=15
    impid=10
    name=12
    artname=8
    id2type={}
    with open(file) as ProteinFile:
        next(ProteinFile)
        for pline in ProteinFile:
            if pline !="\n":
                psplits=pline.split("\t")
#                spID="_".join(psplits)
                spID=psplits[1].strip()+"_"+psplits[2].strip()+"_"+psplits[3].strip()+"_"+psplits[4].strip()+"_"+psplits[5].strip()+"_"+psplits[6].strip()+"_"+psplits[7].strip()
                if spID not in id2type and psplits[impid].strip() in Apecific_file:
                    id2type[spID]="A-specific\t"+psplits[impid].strip()+"\t"+psplits[name].strip()+"\t"+psplits[artname].strip()
                else:
                    id2type[spID]=psplits[type].strip()+"\t"+psplits[impid].strip()+"\t"+psplits[name].strip()+"\t"+psplits[artname].strip()
    return id2type


###############################################################################
## add files together which are for same interaction/folder

def AddReplicatesTogether(lin,list): ## link to the folder, list which contain all files for each folder
    w=open(lin+"/AllRepTogether.txt",'w')
    for entry in list:
        for line in open(lin+"/"+entry+"_withPName.txt"):
            ln=[line.strip(),"\n"]
            w.writelines(ln)
    w.close()
    return lin+"/AllRepTogether"


#####################################################################################################################
#### Merge control and test together for each parameter#######################
#####################################################################################################################
# id2type: dic which have each name as key and type and protein name as one value
# colDic: defines the col number fo reach quantification parameter
# plate file in txt version but with prey unique name

def MergeFiles(filename,colDic,nslist,slist):
    wellcolnum=6
    uniqueCol=2
    for im in colDic:
        write = open(filename +"_" +colDic[im]+".txt", "w")
        ln = ["Proteinid\tType\tunique_name\tprotein_name\tARTNumber\tSourcePlate"]+["\t","NS"]*(len(nslist))+["\t","Stim"]*(len(slist))+["\n"]
        write.writelines(ln)
        dic = {}
        with open(filename+".txt") as openFile:
            next(openFile)
            for line in openFile:
                spl = line.split("\t")
                key=spl[uniqueCol].strip("\" ")
                well=spl[wellcolnum].strip("\" ")
                value=float(spl[im].strip())
                if key not in dic:
                    dic[key]=[[],[],[spl[1].strip("\" "),spl[0].strip("\" "),spl[3].strip("\" "),spl[4].strip("\" ")],[spl[5].strip("\" ")]] # NS,S,[type,mergeId,entrezname,Artid],[sourcePlate]
                elif key in dic and spl[5].strip("\" ") not in dic[key][3]:
                    dic[key][3].append(spl[5].strip("\" "))
                if well in nslist:
                    dic[key][0].append(value)
                elif well in slist:
                    dic[key][1].append(value)
        for pro in dic:
            if len(dic[pro][0])!=len(nslist) or len(dic[pro][1]) !=len(slist):
                print dic[pro]
                print key,well,value
                print " number of replicates are not similar to define number of replicates.. please check again!"
                return False
                # print dic[pro]
            else:
                plateNames=";".join(dic[pro][3])
                ln = [dic[pro][2][1],dic[pro][2][0],str(pro)]+dic[pro][2][2:]+[plateNames]+[str(i) for i in dic[pro][0]]+[str(j) for j in dic[pro][1]]
                line2print="\t".join(ln)
                line2print+="\n"
                write.write(line2print)
        write.close()

#####################################################################################################################
################ Add unique protein id to each prey in the interaction######################################################
#####################################################################################################################

## it is not used right now but can be used later on....
def AddingProteinId(files):
    well = 0
    out = open(files + "_withId.txt", 'w')
    p = 1
    c = 0
    with open(files+".txt") as f:
        next(f)
        for line in f:
            if line != "\n":
                s = line.split("\t")
                if well == 0:
                    well = s[1].strip()
                elif s[1].strip() != well:
                    p = 1
                    c = 0
                    well = s[1].strip()
                if c == 3:
                    c = 0
                    p += 1
                    lnn = [str(p), "\t", line.strip(), "\n"]
                    out.writelines(lnn)
                    c += 1
                elif c < 3:
                    c += 1
                    lnn = [str(p), "\t", line.strip(), "\n"]
                    out.writelines(lnn)
    out.close()
    return (files)


#####################################################################################################################
################ Add protein name and type to each bait prey interaction######################################################
#####################################################################################################################
# it takes text file for each plate in text version with the annotation file as labelled in linkage file and return same
# file but with specific prey name

def AddProteinName(files,PDic,apecific_dic,MergeFileList):
    """
    add names to the plate files and than merge them with and without controls
    """
    controlList=["control+","SD+control"]
    OnlyControl=open(MergeFileList[0],'a')
    withoutControl=open(MergeFileList[1],'a')
    All=open(MergeFileList[2],'a')

    with open(files+".txt") as openFile:
        next(openFile)
        for line in openFile:
            splits=line.strip().split("\t")
            plateName=splits[0].strip()
            # if len(splits)==13:
            #     modline="\t".join(splits)
            # else:
            modline="\t".join(splits[:13])
            id=splits[3].strip()+"\t"+splits[4].strip()+"\t"+splits[5].strip()
            if id in PDic :#and PDic[id][1].strip() not in controlList:
                if PDic[id][2].strip() in apecific_dic:
                    wln=[PDic[id][0],"\t","A-specific","\t",PDic[id][2],"\t",PDic[id][3],"\t",PDic[id][4],"\t",modline+"\n"]
                else:
                    wln=[PDic[id][0],"\t",PDic[id][1],"\t",PDic[id][2],"\t",PDic[id][3],"\t",PDic[id][4],"\t",modline+"\n"]
                if wln[2] not in controlList:
                    withoutControl.writelines(wln)
                else:
                    OnlyControl.writelines(wln)
                All.writelines(wln)
    return files


########################################################################################################################
############################## create a A-specific list for experiment #################################################
########################################################################################################################

def GetAspecifics(file):
    dic={}
    with open(file) as Afile:
        next(Afile)
        for line in Afile:
            splits=line.split("\t")
            unique="ART"+splits[0].strip()
            dic[unique]=line.strip()
    return dic


