__author__ = 'surya'

import xml.etree.cElementTree as ET
from datetime import datetime
import experimentInfo, participantInfo


def makePSIMIXMLFile(NewHitFile,exportPathFile,baitName):
#<entrySet/>
    root = ET.Element("entrySet")
    root.set("minorVersion","0")
    root.set("version","0")
    root.set("level","3")
    root.set("xsi:schemaLocation", "http://psi.hupo.org/mi/mif300 http://psidev.cvs.sourceforge.net/viewvc/psidev/psi/mi/rel30/src/MIF300.xsd")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns", "http://psi.hupo.org/mi/mif300")


    tree = ET.ElementTree(root)

    index=1
    for InteractionLine in NewHitFile:
        protDic={baitName:"not available",InteractionLine[0]:InteractionLine[2]}#Bait:"notavailbaleName, UniqueName:EntrezName
        qvalue=InteractionLine[4]
        # <entrySet><entry/>
        entry_element = ET.SubElement(root, "entry")
        # <entrySet><entry><experimentList/>
        expList_element = ET.SubElement(entry_element, "experimentList")
        ## check if the experiment is already annotated else do it and assign an id
        index=experimentInfo.writeExpInfo(expList_element,index)

        ############################################################################################
        # <entrySet><entry><interactionList/>
        interactnList_element=ET.SubElement(entry_element, "interactionList")
        # <entrySet><entry><interactionList-interaction
        interaction_element=ET.SubElement(interactnList_element, "interaction")
        interaction_element.set("id",str(index))
        index+=1
        # <entrySet><entry><interactionList-interaction-experimentList
        int_expL_element = ET.SubElement(interaction_element, "experimentList")
        # <entrySet><entry><interactionList-interaction-experimentList-experimentRef
        ET.SubElement(int_expL_element, "experimentRef").text="1"
        # <entrySet><entry><interactionList-interaction-participantList
        int_partL = ET.SubElement(interaction_element, "participantList")
        # <entrySet><entry><interactionList-interaction-participantList-participant
        for prot in protDic:
            int_part_element = ET.SubElement(int_partL, "participant")
            int_part_element.set("id",str(index))
            index+=1
                # if prot not in ProteinName2IdDic:
                #     ProteinName2IdDic[prot]=index
            int_part_int = ET.SubElement(int_part_element, "interactor")
            int_part_int.set("id",str(index))
            index += 1
            #run method
            participantInfo.addParticipantInfo(int_part_int,prot,protDic[prot])
            # else:
            #     ET.SubElement(int_part_element, "interactorRef").text=str(ProteinName2IdDic[prot])
        int_confList= ET.SubElement(interaction_element, "confidenceList")
        int_confL_conf=ET.SubElement(int_confList, "confidence")
        conf_unit=ET.SubElement(int_confL_conf, "unit")
        conf_unit_names=ET.SubElement(conf_unit, "names")
        ET.SubElement(conf_unit_names, "shortLabel").text="Rank Based p-value"
        ET.SubElement(conf_unit_names, "fullName").text="MAPPI-DAT based analysis score"
        ET.SubElement(int_confL_conf, "value").text=str(qvalue)
    ## write the file

    tree.write(exportPathFile, encoding='utf-8', xml_declaration=True)
