import yaml

with open("config/settings.yaml", "r") as settings:
    settings = yaml.load(settings)
ldap = settings["ldap"]
general = settings["general"]
db = settings["db"]
