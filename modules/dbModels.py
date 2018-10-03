# This should be database agnostic, since I'm not doing anything crazy.
# Which reminds me, please use Postgres or MySQL in the real world. It's easier to scale than SQLite.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# The session table is made in app.py when Flask-Session gets set up.

# The table where the sign in records go.
class attendanceRecords(db.Model):
    recordNumber = db.Column(db.Integer, primary_key=True, nullable=False)
    studentID = db.Column(db.String(7), unique=False, nullable=False)
    studentName = db.Column(db.String(100), unique=False, nullable=False)
    timeOut = db.Column(db.DateTime(), unique=False, nullable=False)
    timeIn = db.Column(db.DateTime(), unique=False, nullable=True)
    overridden = db.Column(db.Boolean(), unique=False, nullable=False)
    nameFrom = db.Column(db.String(10), unique=False, nullable=False)

# Where student names and ID numbers are stored if they come from Schoology or a csv import (soon).
# The student username column should be the letter "s", followed by a six digit student identifier. This is for
# compatibility with SJCSD systems, and therefore is another case of TODO: Make username column configurable somehow.
class importedUsers(db.Model):
    recordNumber = db.Column(db.Integer, primary_key=True, nullable=False)
    studentID = db.Column(db.String(7), unique=True, nullable=False)
    studentName = db.Column(db.String(100), unique=False, nullable=False)



