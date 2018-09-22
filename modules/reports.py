from modules.api import schoology
from modules.dbModels import db, records
import datetime
import random
import csv
import string
import pytz
import tzlocal
import time
import os

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
