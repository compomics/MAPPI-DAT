__author__ = 'surya'


def createDic(file1,key,val_list,header):
    dic={}
    with open(file1) as filename:
        if header:
            next(filename)
        for line in filename:
            if line!="\n":
                splits=line.split("\t")
                name=splits[key].strip()
                if name not in dic and name!="":
                    dic[name]=[]
                    for index in val_list:
                        dic[name].append(splits[index].strip())
                    # else:
                #     print name,"is a duplicate entry"
        return dic

## for only one key adn one val
def createDicOne(file1,key,val,header):
    dic={}
    list=[]
    with open(file1) as filename:
        if header:
            next(filename)
        for line in filename:
            if line!="\n":
                splits=line.split("\t")
                name=splits[key].strip()
                value=splits[val].strip()
                if name not in dic and name!="":
                    dic[name]=value
    return dic


def createList(file1,index,header,lineList=False):
    list=[]
    with open(file1) as filename:
        if header:
            next(filename)
        for line in filename:
            if line!="\n":
                if lineList:
                    list.append(line.strip())
                else:
                    splits=line.split("\t")
                    value=splits[index].strip()
                    if value!="":
                        list.append(value)
    return list


def CreateDicWithAllColAsVal(file1,key,header,sep="\t",checkCol=False,CheckcolNumValue=[0,0],checkList=False):
    dic={}
    dublicate=0
    notfoundColumn=0
    columnChecked=False
    with open(file1) as filename:
        if header:
            next(filename)
        for line in filename:
            splits=line.split(sep)
            name=splits[key].strip()
            if checkCol:
                if checkList:
                    if splits[CheckcolNumValue[0]].strip() in CheckcolNumValue[1]:
                        columnChecked=True
                else:
                    if splits[CheckcolNumValue[0]].strip() == CheckcolNumValue[1]:
                        columnChecked=True
            else:
                columnChecked=True
            if columnChecked:
                if name not in dic:
                    dic[name]=[]
                    for index in range(0,len(splits)):
                        # if index!=key:
                            dic[name].append(splits[index].strip())
                else:
                    dublicate+=1
            else:
                notfoundColumn+=1
    # print "total dublicate keys found are ",dublicate
    if checkCol:
        print "total lines where ",CheckcolNumValue[1], " was not found are ", notfoundColumn
    print
    return dic

