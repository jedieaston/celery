from modules import settings, recorder
from flask import Flask, render_template, redirect, url_for, session, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from modules.dbModels import db, record
from modules.forms import signInForm, signOutForm, general, ldap, getSettings
from modules.forms import schoology as schoologySettings
import modules.api.schoology as schoology

app = Flask(__name__)
# Change this in prod...
app.config['SECRET_KEY'] = '84328weyrs78sa78asd76f76sdf56asd75632472y8huiasdfh347924h174y43792hg23r4y77y73247bc'

app.config["SQLALCHEMY_DATABASE_URI"] = settings.db["url"]
#Don't ask why I had to do this....

# Setup flask plugins....
try:
    with app.app_context():
        db.init_app(app)
        db.create_all()
except:
    print("Can't connect to the database! Check to make sure your settings are correct.")
    exit()


Bootstrap(app)
nav = Nav(app)


nav.register_element('celeryNav', Navbar('Celery', View('Sign in', 'home'),
                                         View("Admin Page", 'admin')))


@app.route('/', methods=["GET", "POST"])

def home():
    try:
        alertState = session.get("alertState", None)
    except:
        alertState == "0"

    if alertState == "0":
        pass
    form = signOutForm()
    if form.validate_on_submit():
        session["lastCheckedUser"] = form.idNumber.data
        if settings.general["signIn"] == True:
            global record
            record = recorder.signOut(form.idNumber.data)
            return redirect(url_for('signin'))
        else:
            try:
                session["lastCheckedUser"] = recorder.signInNoOut(form.idNumber.data, db)
                alertState = "1"
            except:
                alertState = "2"
    return render_template("index.html", form=form, alertState=alertState)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/signin', methods=["GET", "POST"])
def signin():
    alertState = "0"
    form = signInForm()
    if form.validate_on_submit():
        if form.idNumber.data == "override":
            override = True
            recorder.signIn(record, db, override)
            session["alertState"] = "4"
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
    return render_template("reporting.html")

@app.route('/admin/schoologyconnect', methods=["GET", "POST"])
def schoologyConnect():
    urlForCelery = request.base_url
    schoologyConnectionCheck = schoology.connectionCheck()
    schoologyConnectUrl = schoology.authUrl(urlForCelery)
    return render_template("schoologySetup.html", schoologyConnectUrl=schoologyConnectUrl,
                           schoologyConnectionCheck=schoologyConnectionCheck, schoology=schoology)

@app.route('/admin/settings', methods=["GET", "POST"])
def settingsEditor():
    currentGeneralSettings = getSettings(general)
    genSet = general(**currentGeneralSettings)
    ldapCurrentSettings = getSettings(ldap)
    ldapSet = ldap(**ldapCurrentSettings)
    schoologyCurrentSettings = getSettings(schoologySettings)
    schoologySet = schoologySettings(**schoologyCurrentSettings)
    if schoologySet.is_submitted():
        settings.updateSettingsDicts(schoology=schoologySet.data, ldap=ldapSet.data, general=genSet.data)
        return ("Saved!")
        # try:
        #     settings.updateSettingsDicts(schoology=schoologySet.data, ldap=ldap, general=general)
        #     return("Saved!")
        # except:
        #     settingsSaved = False
    return render_template("settings.html", generalSettings=genSet, ldapSettings=ldapSet, schoologySettings=schoologySet)
if __name__ == '__main__':
    app.run()
