
from Mysql_queries import questions_query, Project_Query
import os


def exportProcessedData(exp,egroup,project,cnx,Mainpath):
    print "preparing your raw data.."
    #first create a folder
    path=Mainpath+"/MAPPI_DAT_RawData"
    if not os.path.isdir(path):
        os.makedirs(path)
    TFilePath=path+"/TFiles"
    if not os.path.isdir(TFilePath):
        os.makedirs(TFilePath)
    ## create all the files
    processedFile=open(path+"/RawDataPre_Processed.txt","w")
    linkageFile=open(path+"/linkageFile.txt","w")

    ## get the processed File
    processedFile.write("UniqueId\ttype\tuniqueName\tEntrenzName\tPlateId\tSourcePlate\tSourceWell\t"
                        "ID\tBlock\tSpotRow\tSpotColumn\tParticleCount\tMeanArea_um2\tgrayvaluemean\tMeanGrayValueMean"
                        "\tMeanIntegralIntensity\tAreaFraction\tIntegralIntensity_um2\n")
    AllPlateRawData = []
    # AllPlates = Project_Query.Select_values(Project_Query.platesNames, cnx, arg=True,
    #                                         argument=(exp, egroup, project))
    # for eachPlate in AllPlates:
    AllPlateRawData = Project_Query.Select_values(Project_Query.getAllRawData, cnx, arg=True,
                                                       argument=(exp, egroup, project))
    print "finished getting data from database...."
    id = 1
    for lineList in AllPlateRawData:
        col1 = "_".join(lineList[0:5] + lineList[12:14])
        exporline = "\t".join([col1] + lineList[5:11] + ["id_" + str(id)] + lineList[11:]) + "\n"
        id += 1
        processedFile.write(exporline)
    processedFile.close()
    print "finished writing preProcessed file"
    ## get the linkage file
    linkageFile.write("bait\tsubfolder\tfile\tproteinFile\n")
    AllLinkageData=Project_Query.Select_values(Project_Query.LinkageFileOut,cnx,arg=True,argument=(exp, egroup, project))
    for lineList in AllLinkageData:
        tfileWrite=open(TFilePath+"/"+lineList[1]+".txt","w")
        tfileWrite.write("ART\tWell\tWell1\tWell2\tWell3\tWell4\tRow\tCol\tPlate_nr\twell\tUnique_ID\tentrezGeneName\tentrezGene\tsynonyms\tid\tnames\tMix\n")
        TFileData=Project_Query.Select_values(Project_Query.TFileOut,cnx,arg=True,argument=(exp, egroup, project,lineList[1].strip()))
        id=0
        for protList in TFileData:
            protList[0]=protList[0][3:]
            protList=protList[0:13]+[protList[12],str(id)]+protList[13:]
            id+=1
            tfileWrite.write("\t".join(protList)+"\n")
        print "finished writing ",lineList[1]," T-file"
        exporline="\t".join([lineList[0],lineList[2].split("-")[0],lineList[2],TFilePath+"/"+lineList[1]+".txt"])+"\n"
        linkageFile.write(exporline)
    linkageFile.close()
    print "Done!!"


