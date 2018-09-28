from modules.api import schoology
from modules.dbModels import db, records, importedUsers
import datetime
import random
import csv
import string
import pytz
import tzlocal
import time
import os
import modules.settings as settings


# Get the timezone!!1!

localTz = tzlocal.get_localzone()


def exportAll():
    # Exports the records table from the db to a csv in static, then spits out the link.
    filePath = 'static/reports/exportAll-' + ''.join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(9)) + ".csv"
    dbQuery = records.query.all()
    with open(filePath, 'w') as csvFile:
        outcsv = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = records.__table__.columns.keys()
        outcsv.writerow(header)
        for record in dbQuery:
            row = []
            for c in header:
                if c == "timeOut" or c == "timeIn":
                    try:
                        # convert timezone to server local time, and make it human-friendly
                        dbTime = pytz.utc.localize(getattr(record, c)).astimezone(localTz)
                        dbTime = dbTime.date.strftime("%D %r")
                        row.append(dbTime)
                    except:
                        # If it's blank for some reason, we need to keep going.
                        row.append(getattr(record, c))
                else:
                    row.append(getattr(record, c))
            outcsv.writerow(row)
    return filePath

def attendedEvent(eventID):
    # Returns a CSV of whether people were there or not on a certain date.
    # TODO: Make this also be able to use start/end times so it is more accurate.
    reportResult = []
    eventDate = datetime.datetime.strptime(schoology.sc.get_event(eventID, group_id=settings.schoology[
        "reportingGroupID"]).start, "%Y-%m-%d %H:%M:%S").date()
    for user in importedUsers.query.all():
        print(user.studentID)
        recordQuery = records.query.filter_by(studentID=user.studentID)
        print(recordQuery.count())
        for result in recordQuery:
            print(result.timeOut.date())
            if result.timeOut.date() == eventDate:
                queryResult = {"studentID": result.studentID, "studentName": result.studentName, "studentAttended": True}
                break
            else:
                continue
        if queryResult["studentID"] != user.studentID:
            # variable wasn't overwritten, therefore they were not there on that date.
            queryResult = {"studentID": user.studentID, "studentName": user.studentName, "studentAttended": False}
            reportResult.append(queryResult)
        else:
            # they were there because it was overwritten.
            reportResult.append(queryResult)
    filePath = 'static/reports/attendanceReport-' + datetime.datetime.strftime(eventDate, "%m-%d-%Y") + ".csv"
    with open(filePath, "w") as reportCSV:
        writeDict = csv.DictWriter(reportCSV, reportResult[0].keys(), lineterminator='\n')
        writeDict.writeheader()
        writeDict.writerows(reportResult)
    return (filePath)
def clearFolder():
    # Thanks, https://stackoverflow.com/a/185941 !
    folder = "static/reports/"
    for file in os.listdir(folder):
        filePath = os.path.join(folder, file)
        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
        except:
            print("Uhh, we couldn't clear the reports folder. Something may be up with the filesystem...")


# Runs on import to make sure we keep the folder tidy, since the reports can be regenerated as long as the database is
# intact.
clearFolder()
