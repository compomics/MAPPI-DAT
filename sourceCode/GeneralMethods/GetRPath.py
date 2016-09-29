## get the name path name for R

def RPathname():
    with open("Parameter.txt") as paraFile:
        next(paraFile)
        for line in paraFile:
#            print line
            splits=line.split("=")
            if splits[0].strip()== "Rpath":
                val=splits[1].strip()
    return val
