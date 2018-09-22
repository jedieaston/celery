import yaml

# The default settings, which should get it running presuming its using the usual
# docker setup.

defaultSettings = {'ldap': {'ldapAvailable': True, 'ldapServer': 'example.com', 'ldapAccessDomain': 'example',
                            'ldapAccessUserName': 'Unprivileged', 'ldapAccessPassword': 'Passw0rd!',
                            'ldapSearchBase': 'DC=example, DC=com', 'ldapAuthenticationStandard': 'NTLM'},
                   'general': {'signIn': True}, 'db': {'url': 'postgres+psycopg2://postgres:celery@db:5432/celerydb'},
                   'schoology': {'instanceUrl': 'xaviersschool.schoology.com', 'apiKey': 'buymeatendiesub',
                                 'apiSecret': 'skdfjlasfaslaksdlaslasfasflkasdkf3e4rijowejrf', 'requestLimit': '5000'},
                   'dev': {'debug': True}}


def updateSettingsDicts(**kwargs):
    # updates settings before writing them to file.
    for key, value in kwargs.items():
        value.pop('csrf_token')
        settings[key] = value
    with open("config/settings.yaml", "w") as settingsYaml:
        yaml.safe_dump(settings, settingsYaml, default_flow_style=False)

def writeSettings():
    # Write new settings if we need to for some other reason outside of the webui
    with open("config/settings.yaml", "w") as settingsYaml:
        yaml.safe_dump(settings, settingsYaml, default_flow_style=False)


while True:
    try:
        with open("config/settings.yaml", "r+") as settingsFile:
            settings = yaml.safe_load(settingsFile)
            if settings == None:
                raise Exception("Woah, there's nothing in the settings file. Restoring defaults.")
        break
    except:
        try:
        # If settings don't exist, create new settings file.
            with open('config/settings.yaml', 'a+') as newSettings:
                yaml.safe_dump(defaultSettings, newSettings, default_flow_style=False)
            with open("config/settings.yaml") as settings:
                settings = yaml.safe_load(settings)
        except:
            print("We're having issues interacting with your filesystem, and cannot "
                  "save a configuration file. Exiting.")
            exit()

ldap = settings["ldap"]
general = settings["general"]
db = settings["db"]
schoology = settings["schoology"]
dev = settings["dev"]