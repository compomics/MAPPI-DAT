__author__ = 'surya'

""" check for the plate names in the database """

import os

from Mysql_queries import MySqlConnection,GetExistingDataFromDatabase, mysql_smallMethods
from Error_handle import ErrorHandling

def checkExistingInfo(plate2subfolder,cnx):
    platDic=GetExistingDataFromDatabase.getAlldata_fromDatabase("""SELECT plate_id,p_name From plates """, cnx)
    for plate in plate2subfolder:
        if plate not in platDic:
            ErrorHandling.IO_prob(plate+" is not present in the database, cannot add data in database")
            return False
    return True
