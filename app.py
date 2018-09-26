from modules import settings, recorder, reports
from flask import Flask, render_template, redirect, url_for, session, request, Response
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from modules.dbModels import db, importedUsers
from modules.forms import signInForm, signOutForm, general, ldap, getSettings, schoologyGroupSelector, getAllReports
from modules.forms import schoology as schoologySettings
import modules.api.schoology as schoology
from flask_session import Session
app = Flask(__name__)
# Change this in prod...
app.config['SECRET_KEY'] = '84328weyrs78sa78asd76f76sdf56asd75632472y8huiasdfh347924h174y43792hg23r4y77y73247bc'

# Flask-SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = settings.db["url"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disables Flask-SQLAlchemy's event system.

# Flask Session, for server-side sessions. (ooh, alliteration!)
app.config["SESSION_TYPE"] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db

Session(app)

# Setup flask plugins....
try:
    with app.app_context():
        db.init_app(app)
        db.create_all()
except:
    print("Can't connect to the database! Check to make sure your settings are correct.")
    exit()
# Flask Bootstrap and Flask Nav.
Bootstrap(app)
nav = Nav(app)

nav.register_element('celeryNav', Navbar('Celery', View('Sign in', 'home'),
                                         View("Admin Page", 'admin')))


#TODO: Move the routes into another file, to make life easier.


@app.route('/', methods=["GET", "POST"])

def home():
    try:
        #Are we coming here from another page?
        alertState = session.get("alertState", None)
    except:
        # Guess we are not.
        alertState == "0"
    if alertState == "0":
        pass
    form = signOutForm()
    if form.validate_on_submit():
        lastCheckedUser = form.idNumber.data
        # If this is a hall-pass type scenario, we need to have them sign back in.
        if settings.general["signIn"] == True:
            global record
            record = recorder.signOut(form.idNumber.data)
            return redirect(url_for('signin'))
        else:
            try:
                lastCheckedUser = recorder.signInNoOut(form.idNumber.data, db)
                alertState = "1"
                # Clears out the form since it was successful.
                form.idNumber.data = ""
            except:
                alertState = "2" #TODO: Make it more clear here what this means.
    else:
        alertState == "0"
        lastCheckedUser= None
    return render_template("index.html", form=form, alertState=alertState, lastCheckedUser=lastCheckedUser)

@app.route('/admin')
def admin():
    return render_template("admin/admin.html")

@app.route('/signin', methods=["GET", "POST"])
def signin():
    alertState = "0"
    form = signInForm()
    if form.validate_on_submit():
        if form.idNumber.data == "override":
            override = True
            recorder.signIn(record, db, override)
            session["alertState"] = "4" #TODO: Clarify this in a comment, so future Easton can remember what this means.
            return redirect(url_for('home'))
        elif form.idNumber.data == record.studentID:
            override = False
            recorder.signIn(record, db, override)
            session["alertState"] = "1"
            return redirect(url_for('home'))
        else:
            alertState = "2"
    return render_template("signin.html", form=form, record=record, alertState=alertState)

@app.route('/admin/reporting', methods=["GET"])
def reporting():
    return render_template("admin/reporting.html", schoology=schoology, settings=settings, reports=reports,
                           getAllReports=getAllReports)

@app.route('/admin/schoologyconnect', methods=["GET", "POST"])
def schoologyConnect():
    urlForCelery = request.base_url
    schoologyConnectionCheck = schoology.connectionCheck()
    schoologyConnectUrl = schoology.authUrl(urlForCelery)
    schoologyDefaultGroupForm = schoologyGroupSelector()
    if schoologyConnectionCheck == True:
        # Sets up the group selector once we know Schoology is connected properly.
        schoologyDefaultGroupForm.groupList.choices = schoology.schoolGroups().items()
        while True:
            if schoologyDefaultGroupForm.validate_on_submit():
                settings.schoology["reportingGroupID"] = schoologyDefaultGroupForm.groupList.data
                settings.writeSettings()
                # Drop the importedUsers table because we changed groups.
                importedUsers.query.delete()
                db.session.commit()
                # It is recreated when the next group is imported.
                try:
                    schoology.importGroupEnrollmentsToDatabase(settings.schoology["reportingGroupID"], db)
                except KeyError:
                    # The user doesn't have the required amount of access to the Schoology group they selected.
                    alertState = "5"
                    return render_template("admin/schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                                           schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology,
                                           schoologyGroupSelector=schoologyDefaultGroupForm, alertState=alertState,
                                           reportingGroupID=settings.schoology["reportingGroupID"])
                return render_template("admin/schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                                       schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology,
                                       schoologyGroupSelector=schoologyDefaultGroupForm, alertState="3",
                                       reportingGroupID=settings.schoology["reportingGroupID"])
            elif "reportingGroupID" in settings.schoology:
                # IF we already have a group ID saved in settings, we'll use that.
                schoologyDefaultGroupForm.groupList.default = settings.schoology["reportingGroupID"]
                # Lets put the members into the database to make reporting easier....
                try:
                    schoology.importGroupEnrollmentsToDatabase(settings.schoology["reportingGroupID"], db)
                except KeyError:
                    # The user doesn't have the required amount of access to the Schoology group they selected.
                    alertState = "5"
                    return render_template("admin/schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                                           schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology,
                                           schoologyGroupSelector=schoologyDefaultGroupForm, alertState=alertState,
                                           reportingGroupID=settings.schoology["reportingGroupID"])
                # alertState 3 means we are ready to go on reporting!
                return render_template("admin/schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                                       schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology,
                                       schoologyGroupSelector=schoologyDefaultGroupForm, alertState="3",
                                       reportingGroupID=settings.schoology["reportingGroupID"])
            else:
                # alertState 2 means we're authorized, but you need to select a group from your school to continue.
                return render_template("admin/schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                                       schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology,
                                       schoologyGroupSelector=schoologyDefaultGroupForm, alertState="2")
    else:
        # We need authorization. Let's get it!
        return render_template("admin/schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                               schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology)

@app.route('/admin/settings', methods=["GET", "POST"])
def settingsEditor():
    currentGeneralSettings = getSettings(general)
    genSet = general(**currentGeneralSettings)
    ldapCurrentSettings = getSettings(ldap)
    ldapSet = ldap(**ldapCurrentSettings)
    schoologyCurrentSettings = getSettings(schoologySettings)
    schoologySet = schoologySettings(**schoologyCurrentSettings)

    # TODO: Find a better way to do this. Maybe it's just to make one form. I don't know.
    if genSet.generalSubmitButton.data and genSet.validate():
        try:
            settings.updateSettingsDicts(general = genSet.data)
            settingsLastSaved = "General"
            settingsSaved = True
        except:
            settingsSaved = False
    elif ldapSet.ldapSubmitButton.data and ldapSet.validate():
        try:
            settings.updateSettingsDicts(ldap = ldapSet.data)
            settingsLastSaved = "LDAP"
            settingsSaved = True
        except:
            settingsSaved = False
    elif schoologySet.schoologySubmitButton.data and schoologySet.validate():
        try:
            settings.updateSettingsDicts(schoology = schoologySet.data)
            settingsLastSaved = "Schoology"
            settingsSaved = True
        except:
            settingsSaved = False
    else:
        # They didn't submit anything.
        settingsSaved = None
        settingsLastSaved = None
    return render_template("admin/settings.html", generalSettings=genSet, ldapSettings=ldapSet,
                           schoologySettings=schoologySet, settingsSaved=settingsSaved,
                           settingsLastSaved=settingsLastSaved)

if settings.dev["debug"] == True:
    import pprint
    @app.route('/debug')
    def debug():
        requestvar = pprint.pformat(request.environ, depth=5)
        return Response(requestvar, mimetype="text/text")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
