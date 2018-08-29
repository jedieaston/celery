# This should be database agnostic, but if it isn't, I BLAAAAAAMMMMMMMMMEEEEEEEE ZOIDBERGGGGG
# Which reminds me, don't use sqlite in prod. It can't do multiple sessions well.
from flask_sqlalchemy import SQLAlchemy
import pymysql
db = SQLAlchemy()

class record(db.Model):
    recordNumber = db.Column(db.Integer, primary_key=True, nullable=False)
    studentID = db.Column(db.String(6), unique=False, nullable=False)
    studentName = db.Column(db.String(100), unique=False, nullable=False)
    timeOut = db.Column(db.DateTime(), unique=False, nullable=False)
    timeIn = db.Column(db.DateTime(), unique=False, nullable=True)
    overridden = db.Column(db.Boolean(), unique=False, nullable=False)
# Ha! This is a one table database. Why a database?

# Because I'm not losing these hecking records.


