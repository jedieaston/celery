# This builds the database, presuming your settings are correct in config/settings.yaml

from app import db, app, record
with app.app_context():
   db.init_app(app)
   db.create_all()
   #if you want to see what happened:
   #print(db.metadata.tables)
