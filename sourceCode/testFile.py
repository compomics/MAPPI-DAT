__author__ = 'surya'

import os
def RPathname():
    with open("Parameter.txt") as paraFile:
        next(paraFile)
        for line in paraFile:
#            print line
            splits=line.split("=")
            if splits[0].strip()== "Rpath":
                val=splits[1].strip()
    return val

Rpath= RPathname()

fileRP = Rpath + " testingRwithPython.R "  # +" cutoff="+str(cut)+" gene="+str(gen)+\

os.system(fileRP)
