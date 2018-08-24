import yaml
from shutil import copyfile

while True:
    try:
        with open("config/settings.yaml", "r") as settings:
            settings = yaml.load(settings)
        break
    except:
        try:
            copyfile("config/demo-settings.yaml", "config/settings.yaml")
            print("Configure config\settings.yaml with your settings, then restart the app. Stopping.... ")
            exit()
        except:
            print("demo-settings.yaml is missing! We can't setup your settings without it. Stopping application.")
            exit()
        continue

ldap = settings["ldap"]
general = settings["general"]
db = settings["db"]
