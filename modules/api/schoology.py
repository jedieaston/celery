# Requires Schoolopy. Could I had used requests? yes, but this guy already did it.
import schoolopy
from modules.settings import schoology as settings

#auth = False
auth = schoolopy.Auth(settings['apiKey'], settings['apiSecret'], three_legged=True, domain=settings['instanceUrl'])
def authUrl(baseUrl):
    # Makes the URL to give to the user to authorize Celery to access Schoology.

    try:
        # Creates the URL that redirects back to celery
        url = "https://" + auth.request_authorization()
        urlsep = "oauth_callback="
        url = url.split(urlsep)[0] + 'oauth_callback=' + baseUrl
        return url
    except:
        #If we are authorized or something is wrong.
        return connectionCheck()

def connectionCheck():
    # Checks to make sure we have authorization

    try:
        check = auth.authorize()
        if check == True:
            global sc
            sc = schoolopy.Schoology(auth)
            sc.limit = 5000         # TODO: This needs to be configurable!!!
            return True
        elif check == False:
            return False
    except:
        return False
# def devConnect():
#     # Uses two-leg authentication and the keys we have in settings to connect a REPL to schoology.
#     global sc
#     sc = schoolopy.Schoology(schoolopy.Auth(settings['apiKey'], settings['apiSecret']))
def showMe():
    # More of a test, gives information about the user logged in,
    sc.limit = 5
    me = sc.get_me()
    me = me.name_display
    return me
def schoolGroups():
    # Gets you a dictionary of school-wide groups and their schoology IDs.
    groups = {}
    for group in sc.get_groups():
        groups[group.id] = group.title
    return groups
