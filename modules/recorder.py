import csv
from modules import ldapConnect
from modules.dbModels import records
import datetime
import random
import string


def signOut(idNumber):
    if ldapConnect.ldapAvailable == True:
        try:
            studentName = ldapConnect.getStudentName(idNumber)
        except:
            studentName = "Couldn't find name."
    elif ldapConnect.ldapAvailable == False:
        studentName = "LDAP not available."
    newRecord = records(studentID=idNumber, studentName=studentName,
                        timeOut=datetime.datetime.today())
    return newRecord

def signIn(record, db, override):
    record.timeIn = datetime.datetime.today()
    record.overridden = override
    db.session.add(record)
    db.session.commit()

def signInNoOut(idNumber, db):
    if ldapConnect.ldapAvailable == True:
        try:
            studentName = ldapConnect.getStudentName(idNumber)
        except:
            studentName = "Couldn't find name."
    elif ldapConnect.ldapAvailable == False:
        studentName = "LDAP not available."
    newRecord = records(studentID=idNumber, studentName=studentName,
                        timeOut=datetime.datetime.today(), overridden=False)
    db.session.add(newRecord)
    db.session.commit()
    return studentName






