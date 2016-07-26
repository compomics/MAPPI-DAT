__author__ = 'surya'

def directWeb(UniqueCurser,All_uniqueName,NameCol):
    import webbrowser
    try:
#        print All_uniqueName
        secondIndex=UniqueCurser.curselection()[0]
#        print secondIndex
        uniqueName=All_uniqueName[int(secondIndex)-2]
#        print uniqueName
        web_name=uniqueName.split()[NameCol].strip()
        webbrowser.open("http://www.genecards.org/index.php?path=/Search/keyword/"+web_name)

    except:
        print "unique name doesnot exist"
