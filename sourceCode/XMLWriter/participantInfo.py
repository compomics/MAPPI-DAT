__author__ = 'surya'

import xml.etree.cElementTree as ET

def addParticipantInfo(intL_int_element,prot,entrezName):
    #participant-interactor-names
    names=ET.SubElement(intL_int_element, "names")
    ET.SubElement(names, "shortLabel").text=prot
    ET.SubElement(names, "fullName").text=entrezName
    # ET.SubElement(names, "alias",type="uniqueName").text=uniqueName
    #participant-interactor-interactortype
    interactor_type=ET.SubElement(intL_int_element, "interactorType")
    # participant-interactor-interactortype-names
    int_names=ET.SubElement(interactor_type, "names")
    ET.SubElement(int_names, "shortLabel").text="protein"
    ET.SubElement(int_names, "fullName").text="protein"
    # participant-interactor-interactortype-xref
    xref = ET.SubElement(interactor_type, "xref")
    primaryref = ET.SubElement(xref, "primaryRef")
    if entrezName=="not available":
        primaryref.set("db", "unknown")
        primaryref.set("id", "unknown")
    else:
        primaryref.set("db", "unknown")
        primaryref.set("id",entrezName)

