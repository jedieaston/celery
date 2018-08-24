from modules import recorder, settings
from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, DataRequired
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from modules.dbModels import db

app = Flask(__name__)
# Change this in prod...
app.config['SECRET_KEY'] = '84328weyrs78sa78asd76f76sdf56asd75632472y8huiasdfh347924h174y43792hg23r4y77y73247bc'

app.config["SQLALCHEMY_DATABASE_URI"] = settings.db["url"]
#Don't ask why I had to do this....

# Setup flask plugins....
db.init_app(app)
Bootstrap(app)
nav = Nav(app)


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
            global record
            record = recorder.signOut(form.idNumber.data)
            return redirect(url_for('signin'))
        else:
            try:
                recorder.signInNoOut(form.idNumber.data, db)
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


if __name__ == '__main__':
    app.run(Debug=True, use_reloader=True)
