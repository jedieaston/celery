# This uses csv files without a database. You probably shouldn't use it, since it doesn't work.


import csv
import ldapConnect
import random
import string
import datetime
logFile = "logs-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9)) + ".csv"
recordsForExport = []

def buildCSV():
    with open("static/logs/" + logFile, "w") as logCSV:
        writeDict = csv.DictWriter(logCSV, recordsForExport[0].keys(), lineterminator='\n')
        writeDict.writeheader()
        writeDict.writerows(recordsForExport)

def signOut(idNumber):
    record = {}
    record["idNumber"] = idNumber
    record["Name"] = ldapConnect.getStudentName(idNumber)
    #record["Name"] = "Mr. Placeholder!"
    timeNow = datetime.datetime.now()
    record["Time Out"] = timeNow.strftime("%m-%d-%Y %H:%M")
    return record
def signIn(record, override):
    timeNow = datetime.datetime.now()
    record["Time in"] = timeNow.strftime("%m-%d-%Y %H:%M")
    if override == True:
        record["Overridden"] = "Yes"
    else:
        record["Overridden"] = "No"

def signInNoOut(idNumber):
    record = {}
    record["idNumber"] = idNumber
    record["Name"] = ldapConnect.getStudentName(idNumber)
    #record["Name"] = "Mr. Placeholder!"
    timeNow = datetime.datetime.now()
    record["Signed in at"] = timeNow.strftime("%m-%d-%Y %H:%M")
    recordsForExport.append(record)