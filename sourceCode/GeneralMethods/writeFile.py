__author__ = 'surya'

def writeFromList(list2write,filename):
    wr=open(filename,"w")
    for eachVal in list2write:
        wr.write(eachVal+"\n")
    wr.close()