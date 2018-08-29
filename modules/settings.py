import yaml
defaultSettings = {'db': {'url': 'postgres+psycopg2://postgres:celery@db:5432/celerydb'},
 'general': {'signIn': True},
 'ldap': {'ldapAccessDomain': 'example',
  'ldapAccessPassword': 'Passw0rd!',
  'ldapAccessUserName': 'Unprivileged',
  'ldapAuthenticationStandard': 'NTLM',
  'ldapAvailable': True,
  'ldapSearchBase': 'DC=example, DC=com',
  'ldapServer': 'ad.celery.internal'},
 'schoology': {'apiKey': 'buymeatendiesub',
  'apiSecret': 'skdfjlasfaslaksdlaslasfasflkasdkf3e4rijowejrf',
  'instanceUrl': 'hogwarts.schoology.com',
  'requestLimit': '5000'}}

def updateSettingsDicts(**kwargs):
    # updates settings before writing them to file.
    #print(kwargs.items())
    for key, value in kwargs.items():
        value.pop('csrf_token')
        settings[key] = value
    #currentSettingsYaml = yaml.safe_dump(settings, default_flow_style=False)
    #print(currentSettingsYaml)
    #writeSettings()
    with open("config/settings.yaml", "w") as settingsYaml:
        #print(yaml.dump(settings))
        yaml.safe_dump(settings, settingsYaml, default_flow_style=False)

def writeSettings():
    # Write new settings if we need to for some other reason outside of the webui
    with open("config/settings.yaml", "w") as settingsYaml:
        print(yaml.dump(settings))
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
            break
        except:
            print("We're having issues interacting with your file system, meaning we can't create a settings file. Exiting.")
            exit()
        continue

# with open("config/settings.yaml", "r") as settings:
#     settings = yaml.load(settings)


ldap = settings["ldap"]
general = settings["general"]
db = settings["db"]
schoology = settings["schoology"]
