import settings
import recorder
from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import Length, DataRequired, AnyOf
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link
app = Flask(__name__)
Bootstrap(app)
nav = Nav(app)
#session.clear()
logFile = recorder.logFile
# Change this in prod...
app.config['SECRET_KEY'] = '84328weyrs78sa78asd76f76sdf56asd75632472y8huiasdfh347924h174y43792hg23r4y77y73247bc'

nav.register_element('celeryNav', Navbar('Celery', View('Sign in', 'home'),
                                         View("Admin Page", 'admin')))

class signOutForm(FlaskForm):
    idNumber = StringField('ID Number: ', validators=[Length(min=6, max=6, message="That's the wrong length! It should be six characters"),
                                                     DataRequired(message="This field is required!")], )
class signInForm(FlaskForm):
    idNumber = StringField('ID Number: ', validators=[Length(min=6, max=8, message="That's the wrong length! It should be six characters unless you are overriding."),
                                                     DataRequired(message="This field is required!")], render_kw={'autofocus': True})

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
        session["currentOutUser"] = form.idNumber.data
        if settings.general["signIn"] == "yes":
            currentWorkingRecord = recorder.signOut(form.idNumber.data)
            session['currentWorkingRecord'] = currentWorkingRecord
            return redirect(url_for('signin'))
        else:
            try:
                recorder.signInNoOut(form.idNumber.data)
                alertState = "1"
            except:
                alertState = "2"
    return render_template("index.html", form=form, alertState=alertState)

@app.route('/admin')
def admin():
    return render_template("admin.html", logFile=logFile)

@app.route('/signin', methods=["GET", "POST"])
def signin():
    alertState = "0"
    currentWorkingRecord = session.get('currentWorkingRecord', None)
    form = signInForm()
    if form.validate_on_submit():
        if form.idNumber.data == "override":
            override = True
            recorder.signIn(currentWorkingRecord, override)
            session["alertState"] = "4"
            return redirect(url_for('home'))
        elif form.idNumber.data == currentWorkingRecord["idNumber"]:
            override = False
            recorder.signIn(currentWorkingRecord, override)
            session["alertState"] = "1"
            return redirect(url_for('home'))
        else:
            alertState = "2"
    return render_template("signin.html", form=form, currentWorkingRecord=currentWorkingRecord, alertState=alertState)


if __name__ == '__main__':
    app.run(Debug=True, use_reloader=True)
