__author__ = 'surya'

import xml.etree.cElementTree as ET

def writeExpInfo(expList_element,index):
    # <entrySet><entry><experimentList<experimentDescription/>
    expDesc_element = ET.SubElement(expList_element, "experimentDescription")
    expDesc_element.set("id", str(index))
    index+=1
    # <entrySet><entry><experimentList><experimentDescription><names/>
    expName_element = ET.SubElement(expDesc_element, "names")
    # <entrySet><entry><experimentList><experimentDescription><names><fullName/>
    ET.SubElement(expName_element, "fullName").text = "Proteome-scale Binary Interactomics in Human Cells."


    # <entrySet><entry><experimentList><experimentDescription><bibref/>
    expbib_element = ET.SubElement(expDesc_element, "bibref")
    # <entrySet><entry><experimentList><experimentDescription><bibref><xref/>
    exp_bib_ref_element = ET.SubElement(expbib_element, "xref")
    # <entrySet><entry><experimentList><experimentDescription><bibref><xref><primaryRef/>
    exp_bib_xref_pri_element = ET.SubElement(exp_bib_ref_element, "primaryRef")
    exp_bib_xref_pri_element.set("db", "pubmed")
    exp_bib_xref_pri_element.set("id", "27803151")
    # <entrySet><entry><experimentList><experimentDescription><bibref><attributeList/>
    exp_bib_attrL = ET.SubElement(expbib_element, "attributeList")
    # <entrySet><entry><experimentList><experimentDescription><bibref><attributeList><attribute/>
    exp_bib_attr = ET.SubElement(exp_bib_attrL, "attribute")
    exp_bib_attr.set("name","publication title")
    exp_bib_attr.set("nameAc", "MI:1091")
    exp_bib_attr.text = "Proteome-scale Binary Interactomics in Human Cells."


    # <entrySet><entry><experimentList><experimentDescription><interactionDetectionMethod/>
    exp_int_element = ET.SubElement(expDesc_element, "interactionDetectionMethod")
    # <entrySet><entry><experimentList><experimentDescription><interactionDetectionMethod><names/>
    exp_int_names = ET.SubElement(exp_int_element, "names")
    # <entrySet><entry><experimentList><experimentDescription><interactionDetectionMethod><names>shortLabel</>
    ET.SubElement(exp_int_names, "shortLabel").text = "mappit"
    ET.SubElement(exp_int_names, "fullName").text = "mappit"
    # <entrySet><entry><experimentList><experimentDescription><interactionDetectionMethod><xref/>
    exp_int_xref = ET.SubElement(exp_int_element, "xref")
    # <entrySet><entry><experimentList><experimentDescription><interactionDetectionMethod><xref><primaryRef/>
    exp_int_xref_pref = ET.SubElement(exp_int_xref, "primaryRef")
    exp_int_xref_pref.set("db", "psi-mi")
    exp_int_xref_pref.set("id", "MI:0231")
    exp_int_xref_pref.set("refType","identity")
    exp_int_xref_pref.set("refTypeAc","MI:0356")
    return index