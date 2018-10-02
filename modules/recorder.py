import csv
from modules import ldapConnect
from modules.dbModels import records, importedUsers
import datetime
from modules.api.schoology import connectionCheck # To see if we can get names from schoology.



def signOut(idNumber):
    if connectionCheck() == True:
        # Cool, schoology is connected, meaning we have should have names in the database.
        # Also, TODO: Do we need to worry about storing student names in the database? Probably.
        try:
            studentIDQuery = importedUsers.query.filter_by(studentID="s" + str(idNumber))
            studentName = studentIDQuery[0].studentName
        except:
            # They must not be in the group.
            studentName = "Unknown"
    elif ldapConnect.ldapAvailable == True:
        try:
            studentName = ldapConnect.getStudentName(idNumber)
        except:
            studentName = "Unknown"
    else:
        studentName = "Unknown"
    newRecord = records(studentID="s" + idNumber, studentName=studentName,
                        timeOut=datetime.datetime.today())
    return newRecord

def signIn(record, db, override):
    record.timeIn = datetime.datetime.today()
    record.overridden = override
    db.session.add(record)
    db.session.commit()

# If we aren't signing back in (i.e for a club meeting or something)
def signInNoOut(idNumber, db):
    if connectionCheck() == True:
        # Cool, schoology is connected, meaning we have should have names in the database.
        # Also, TODO: Do we need to worry about storing student names in the database? Probably.
        try:
            studentIDQuery = importedUsers.query.filter_by(studentID="s" + str(idNumber))
            studentName = studentIDQuery[0].studentName
        except:
            # They must not be in the group.
            if ldapConnect.ldapAvailable == True:
                try:
                    studentName = ldapConnect.getStudentName(idNumber)
                except:
                    studentName = "Unknown"
            else:
                studentName = "Unknown"
    elif ldapConnect.ldapAvailable == True:
        try:
            studentName = ldapConnect.getStudentName(idNumber)
        except:
            studentName = "Unknown"
    else:
        studentName = "Unknown"
    newRecord = records(studentID="s" + idNumber, studentName=studentName,
                        timeOut=datetime.date.today(), overridden=False)
    db.session.add(newRecord)
    db.session.commit()
    return studentName






