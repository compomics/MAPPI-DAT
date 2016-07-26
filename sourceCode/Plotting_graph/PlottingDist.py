__author__ = 'surya'


# plot each IntegralInteraction S values and save a plot in the end for the respective plate

def plot(file,nslen,slen):
    import matplotlib.pyplot as plt
    start=5
    list=[]
    with open(file+"_IntegralIntensity.txt") as files:
        next(files)
        for lines in files:
            splits=lines.split("\t")
            for i in range(start+nslen,start+nslen+slen):
                list.append(float(splits[i].strip()))

    plt.hist(list,50)
    plt.xlabel('intensity')
    plt.ylabel('frequency')
    plt.title('Histogram distribution of S integral intesity')

    plt.subplots_adjust(left=0.2)
    plt.savefig(file+'.png')
    plt.clf()
    return file+'.png'



# gives a final plot for the number of positives found before and after the filtration of annotated entries that could
# be SD+; control+ or control- for example

def plotFinalPlt(path):
    import matplotlib.pyplot as pltt
    x=[]
    y=[]
    ys=[]
    with open(path+".txt") as file:
        next (file)
        for line in file:
            splits=line.split("\t")
            x.append(splits[1].strip())
            y.append(splits[4].strip())
            ys.append(splits[2].strip())
    pltt.plot(y,"ro-",ys,"bs-")
    pltt.title('Significant interaction found for each plate')
    pltt.xlabel('interaction')
    pltt.ylabel('interactions')
    pltt.xlim(-1,len(x))
    mi=int(min(y))-2
    ma=int(max(ys))+10
#    pltt.ylim(mi,ma)
    for i in range(0,len(x)):
        pltt.annotate(x[i]+", " +y[i], xy=(i,y[i]),
            arrowprops=dict(facecolor='green'),
            )

    pltt.savefig(path+'.png')
    pltt.clf()

    return file



##################################################################
## create a plot from the list of the values

def create_plot(x_list,nx_list,var):
    import random
    ## select random numbers of the same length of NS
    s_list=random.sample(x_list,len(nx_list))
    num_bins=50
    import matplotlib.pyplot as plt
    plt.figure("Histogram distribution for "+var)
    plt.subplot(211)
    plt.title("Stimulating Integral Intensity")
    plt.ylabel('frequency')
    plt.hist(s_list, num_bins,facecolor='green')
    plt.subplot(212)
    plt.title("Non-Stimulating Integral Intensity")
    plt.hist(nx_list, num_bins,facecolor='red')
    plt.xlabel('intensity')
    plt.ylabel('frequency')

    # # Tweak spacing to prevent clipping of ylabel
    # plt.subplots_adjust(left=0.15)
    plt.show()


################################################################
### create a box plot
