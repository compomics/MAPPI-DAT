__author__ = 'surya'

## need py2exe as a parameter


# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3)
from distutils.core import setup
import py2exe
import glob
# for console program use 'console = [{"script" : "scriptname.py"}]
setup(console=[{"script": "Art_Database_InputGui.py"}])#, options=opts) #data_files=data_files)
