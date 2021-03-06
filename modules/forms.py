from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, URL
from wtforms.fields.html5 import DateField
from modules import settings


def getSettings(form):
    # get settings from settings module and their current values to be injected into a form later.
    currentValues = {}
    formreqs = form.__dict__
    for key in formreqs:
        try:
            value = settings.settings[str(form.__name__)][key]
            currentValues[key] = value
        except:
            currentValues[key] = ""
    #print(currentValues)
    return currentValues
class signOutForm(FlaskForm):
    # TODO: Validators for the ID Number need to be user-configurable.
    idNumber = StringField('ID Number: ', validators=[Length(min=6, max=6, message="That's the wrong length! It "
                                                                                   "should be six characters."),
                                                     DataRequired(message="This field is required!")], render_kw={'autofocus': True})
class signInForm(FlaskForm):
    idNumber = StringField('ID Number: ', validators=[Length(min=6, max=8, message="That's the wrong length! It should be six characters unless you are overriding."),
                                                     DataRequired(message="This field is required!")], render_kw={'autofocus': True})
class general(FlaskForm):
    signIn = BooleanField('Do you want to ask for a sign in after someone scans their badge? This is most useful for hall-pass scenarios.')
    generalSubmitButton = SubmitField("Submit")

# TODO: Why is the CSRF Token missing under Chrome on the settings page? Gotta figure this one out.
class ldap(FlaskForm):
    ldapAvailable = BooleanField('LDAP Enabled')
    ldapServer = StringField('Active Directory Server: ', description="i.e. ad.celery.net")
    ldapAccessDomain = StringField('Active Directory upn suffix/NETBIOS name', description="i.e. CELERY")
    ldapAccessUserName = StringField('Username for an unprivileged AD account, for name queries.')
    ldapAccessPassword = PasswordField('Password for the account.', description="warning: this is stored in plaintext at the moment.")
    ldapSearchBase = StringField('The search base for the name searches.',
                                 description="Usually something like DC=example, DC=com")
    ldapSubmitButton = SubmitField("Submit")
class schoology(FlaskForm):
    instanceUrl = StringField('Schoology Instance URL', description="where you log into schoology, i.e. hogwarts.schoology.com")
    apiKey = StringField('Schoology API Key', description="Your API key for Schoology. Available from your Schoology admin or schoology.com/api")
    apiSecret = StringField('Schoology API Secret', description="By the way, the API uses the users credentials, so the keys don't need any permissions.")
    schoologySubmitButton = SubmitField("Submit")

class schoologyGroupSelector(FlaskForm):
    groupList = SelectField('Default Schoology Group') #Choices are created when the form is instantiated.
    schoologyGroupSelectorSubmit = SubmitField('Submit')

class getAllReports(FlaskForm):
    getAllReportsSubmit = SubmitField('Submit')

class attendedEventSelector(FlaskForm):
    eventList = SelectField('Event to run report against.', validators=[DataRequired(message="Pick an event.")])
    attendedEventSelectorSubmit = SubmitField('Submit')
