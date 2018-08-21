import csv
import ldapConnect
import datetime
import random
import string
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
    #record["Name"] = ldapConnect.getStudentName(idNumber)
    record["Name"] = "Mr. Placeholder!"
    timeNow = datetime.datetime.now()
    record["Time Out"] = timeNow.strftime("%m-%d-%Y %H:%M")
    return record

def signInNoOut(idNumber):
    record = {}
    record["idNumber"] = idNumber
    # record["Name"] = ldapConnect.getStudentName(idNumber)
    record["Name"] = "Mr. Placeholder!"
    timeNow = datetime.datetime.now()
    record["Signed in at"] = timeNow.strftime("%m-%d-%Y %H:%M")
    recordsForExport.append(record)
    buildCSV()

def signIn(record, override):
    timeNow = datetime.datetime.now()
    record["Time in"] = timeNow.strftime("%m-%d-%Y %H:%M")
    if override == "yes":
        record["Overridden"] = "Yes"
    else:
        record["Overridden"] = "No"
    recordsForExport.append(record)
    buildCSV()


