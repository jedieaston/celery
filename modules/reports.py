from modules.api import schoology
from modules.dbModels import db, records
import datetime
import random
import csv
import string
def exportAll():
    # Exports the records table from the db to a csv in static, then spits out the link.
    filePath = 'static/reports/exportAll-' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9)) + ".csv"
    dbQuery = records.query.all()
    with open(filePath, 'w') as csvFile:
        outcsv = csv.writer(csvFile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
        header = records.__table__.columns.keys()
        outcsv.writerow(header)
        for record in dbQuery:
            outcsv.writerow([getattr(record, c) for c in header])
    return filePath
